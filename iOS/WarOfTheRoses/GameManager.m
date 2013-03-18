//
//  GameManager.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import "GameManager.h"
#import "RandomDiceStrategy.h"
#import "RandomDeckStrategy.h"
#import "MinimumRequirementDeckStrategy.h"

#import "AIStrategyAdvancer.h"
#import "AIStrategyCatapulter.h"

@implementation GameManager

@synthesize delegate = _delegate;
@synthesize currentGame = _currentGame;
@synthesize currentPlayersTurn = _currentPlayersTurn;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        _currentGame = [[Game alloc] init];
                
        self.deckStrategy = [RandomDeckStrategy strategy];
    }
    
    return self;
}

+ (GameManager*)sharedManager {
    
    static GameManager* _instance = nil;

    @synchronized(self) {
        
        if (_instance == nil) {
            _instance = [[GameManager alloc] init];
        }
    }
    
    return _instance;
}

- (void)startNewGameOfType:(GameTypes)gameType {
    
    _currentGame = [[Game alloc] init];
    _currentGame.gametype = gameType;
    _currentGame.state = kGameStateInitialState;
    _currentGame.currentRound = 1;
    _turnCounter = 0;
    
    // Only 1 action in first round
    _currentGame.numberOfAvailableActions = 1;
    _currentGame.myDeck = [_deckStrategy generateNewDeckWithNumberOfBasicType:6 andSpecialType:1 cardColor:_currentGame.myColor];
    
    if (gameType == kGameTypeSinglePlayer) {
        
        _enemyPlayer = [[AIPlayer alloc] initWithStrategy:[[AIStrategyAdvancer alloc] init]];
        _enemyPlayer.deckStrategy = [MinimumRequirementDeckStrategy strategy];
        
        BOOL setupComplete = NO;
        NSUInteger retries = 0;
        
        while (!setupComplete) {
            
            retries++;
            _currentGame.enemyDeck = [_enemyPlayer.deckStrategy generateNewDeckWithNumberOfBasicType:6 andSpecialType:1 cardColor:_currentGame.enemyColor];
            [_enemyPlayer placeCardsInDeck:_currentGame.enemyDeck];
        
            if ([_enemyPlayer.deckStrategy respondsToSelector:@selector(deckSetupMatchesRequirements)]) {
                setupComplete = [_enemyPlayer.deckStrategy deckSetupMatchesRequirements];
            }
            else {
                setupComplete = YES;
            }
        }
        
        NSLog(@"Number of retries before deck met requirements: %d", retries);
    }
    
    // TODO: Random starter
    _currentPlayersTurn = kPlayerGreen;
}

- (Card*)cardLocatedAtGridLocation:(GridLocation*)gridLocation {
    
    return [_currentGame.unitLayout objectForKey:gridLocation];
}

- (void)card:(Card *)card movedToGridLocation:(GridLocation *)location {
    
    NSLog(@"Card: %@ moved to location: %@", card, location);
    
    [_currentGame.unitLayout removeObjectForKey:card.cardLocation];
    
    card.cardLocation = location;
    [_currentGame.unitLayout setObject:card forKey:location];
}

- (void)attackSuccessfulAgainstCard:(Card *)card {
    
    card.hitpoints--;
    
    if (card.hitpoints == 0) {
        CCLOG(@"Card: %@ has been defeated - remove from game", card);
        
        card.dead = YES;
        
        [_currentGame.unitLayout removeObjectForKey:card.cardLocation];

        if ([_delegate respondsToSelector:@selector(cardHasBeenDefeatedInCombat:)]) {
            [_delegate cardHasBeenDefeatedInCombat:card];
        }
    }
    else {
        CCLOG(@"Card: %@ has lost in combat...Remaining hitpoints: %d", card, card.hitpoints);
    }
}

- (NSUInteger)actionUsed:(Action*)action {
    
    if (action.isAttack) {
        _currentGame.numberOfAvailableActions -= action.cardInAction.attackActionCost;
    }
    else {
        _currentGame.numberOfAvailableActions -= action.cardInAction.moveActionCost;
    }
    
    return _currentGame.numberOfAvailableActions;
}

- (BOOL)shouldEndTurn {
    
    if (_currentGame.numberOfAvailableActions == 0) {
        return YES;
    }
    
    // Check if any units has remaining actions
    NSArray *unitsToCheck;
    
    if (_currentPlayersTurn == _currentGame.myColor) {
        unitsToCheck = _currentGame.myDeck.cards;
    }
    else {
        unitsToCheck = _currentGame.enemyDeck.cards;
    }
    
    for (Card *card in unitsToCheck) {
        
        if (!card.dead && !card.hasPerformedActionThisRound) {
            if ((card.moveActionCost <= _currentGame.numberOfAvailableActions && card.movesRemaining > 0) ||
                (card.attackActionCost <= _currentGame.numberOfAvailableActions) ) {
                return NO;
            }
        }
    }
    
    return YES;
}

- (CombatOutcome)resolveCombatBetween:(Card*)attacker defender:(Card*)defender battleStrategy:(id<BattleStrategy>)battleStrategy {
    
    CombatOutcome outcome = [battleStrategy resolveCombatBetweenAttacker:attacker defender:defender gameManager:self];
    
    return outcome;
}

- (void)endTurn {
    
    _turnCounter++;
    
    if ((_turnCounter % 2) == 0) {
        _currentGame.currentRound++;
        
        CCLOG(@"Round increased to %d", _currentGame.currentRound);
    }

    // Reset actioncount
    _currentGame.numberOfAvailableActions = 2;
    
    // Reset movecounters på kort
    [_currentGame.myDeck resetMoveCounters];
    
    if (_currentGame.gametype == kGameTypeSinglePlayer) {
        [_currentGame.enemyDeck resetMoveCounters];
    }
    
    _currentPlayersTurn = !_currentPlayersTurn;
    
    if ([_delegate respondsToSelector:@selector(turnChangedToPlayerWithColor:)]) {
        [_delegate turnChangedToPlayerWithColor:_currentPlayersTurn];
    }
}

- (Action *)getActionForEnemeyPlayer {
    
    [_enemyPlayer createBattlePlansForUnits:_currentGame.enemyDeck.cards sgainstEnemyUnits:_currentGame.myDeck.cards fromUnitLayout:_currentGame.unitLayout];
    
    Action *action = [_enemyPlayer decideNextAction];
    
    return action;
}

- (GameResults)checkForEndGame {
    
    BOOL allUnitsDead = YES;
    
    _currentGame.gameOver = YES;
    
    for (Card *myCard in _currentGame.myDeck.cards) {
        if (!myCard.dead) {
            allUnitsDead = NO;
        }
    }
    
    if (allUnitsDead) {
        return kGameResultDefeat;
    }
    
    allUnitsDead = YES;
    
    for (Card *enemyCard in _currentGame.enemyDeck.cards) {
        if (!enemyCard.dead) {
            allUnitsDead = NO;
        }
    }
    
    if (allUnitsDead) {
        return kGameResultVictory;
    }
    
    for (GridLocation *location in _currentGame.unitLayout.allKeys) {
        
        Card *card = [_currentGame.unitLayout objectForKey:location];
        
        if ([card isOwnedByPlayerWithColor:_currentGame.enemyColor] && location.row == 8) {
            return kGameResultDefeat;
        }

        if ([card isOwnedByPlayerWithColor:_currentGame.myColor] && location.row == 1) {
            return kGameResultVictory;
        }
    }
    

    _currentGame.gameOver = NO;
    
    return kGameResultInProgress;
}

@end
