//
//  GameManager.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import "GameManager.h"
#import "RandomDiceStrategy.h"
#import "MinimumRequirementDeckStrategy.h"
#import "MinimumRequirementDeckStrategy.h"

#import "AIStrategyAdvancer.h"
#import "AIStrategyCatapulter.h"
#import "GCTurnBasedMatchHelper.h"

@implementation GameManager

@synthesize delegate = _delegate;
@synthesize currentGame = _currentGame;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        _currentGame = [[Game alloc] init];
                
        self.deckStrategy = [MinimumRequirementDeckStrategy strategy];
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

- (void)continueExistingGame {
    
    _currentGame = [[Game alloc] init];
    _currentGame.gametype = kGameTypeMultiPlayer;
}

- (void)startNewGameOfType:(GameTypes)gameType {
    
    _currentGame = [[Game alloc] init];
    _currentGame.gametype = gameType;
    _currentGame.state = kGameStateInitialState;
    _currentGame.currentRound = 1;
    _currentGame.turnCounter = 0;
    
    // Random color (green or red)
    _currentGame.currentPlayersTurn = arc4random() % 2;;

    // Only 1 action in first round
    _currentGame.numberOfAvailableActions = 1;
    _currentGame.myDeck = [_deckStrategy generateNewDeckWithNumberOfBasicType:NUMBER_OF_BASICUNITS andSpecialType:NUMBER_OF_SPECIALUNITS cardColor:_currentGame.myColor];
    
    if (gameType == kGameTypeMultiPlayer) {
        
        _currentGame.enemyDeck = [_deckStrategy generateNewDeckWithNumberOfBasicType:NUMBER_OF_BASICUNITS andSpecialType:NUMBER_OF_SPECIALUNITS cardColor:_currentGame.enemyColor];
    }
    
    if (gameType == kGameTypeSinglePlayer) {
        
        _enemyPlayer = [[AIPlayer alloc] initWithStrategy:[[AIStrategyAdvancer alloc] init]];
        _enemyPlayer.deckStrategy = [MinimumRequirementDeckStrategy strategy];
        
        _currentGame.enemyDeck = [_enemyPlayer.deckStrategy generateNewDeckWithNumberOfBasicType:6 andSpecialType:1 cardColor:_currentGame.enemyColor];
        [_enemyPlayer placeCardsInDeck:_currentGame.enemyDeck];
    }
}

- (PlayerColors)currentPlayersTurn {
    
    return _currentGame.currentPlayersTurn;
}

- (void)setCurrentPlayersTurn:(PlayerColors)currentPlayersTurn {
    
    _currentGame.currentPlayersTurn = currentPlayersTurn;
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
    
    if (card.dead) return;
    
    card.hitpoints--;
    
    if (card.hitpoints == 0) {
        NSLog(@"Card: %@ has been defeated - remove from game", card);
        
        card.dead = YES;
        
        [_currentGame.unitLayout removeObjectForKey:card.cardLocation];

        if ([_delegate respondsToSelector:@selector(cardHasBeenDefeatedInCombat:)]) {
            [_delegate cardHasBeenDefeatedInCombat:card];
        }
    }
    else {
        NSLog(@"Card: %@ has lost in combat...Remaining hitpoints: %d", card, card.hitpoints);
    }
}

- (void)willUseAction:(Action*)action {
    
}

- (NSUInteger)actionUsed:(Action*)action {
    
    if (!action.playback) {
        _currentGame.numberOfAvailableActions -= action.cost;
    }
    
    return _currentGame.numberOfAvailableActions;
}

- (BOOL)cardIsAbleToMove:(Card*)card {
    
    return card.moveActionCost <= _currentGame.numberOfAvailableActions && card.movesRemaining > 0 && ![card isAffectedByAbility:kAbilityCoolDown];
}

- (BOOL)cardIsAbleToAttack:(Card*)card {
    
    return card.attackActionCost <= _currentGame.numberOfAvailableActions && ![card isAffectedByAbility:kAbilityCoolDown];
}

- (BOOL)shouldEndTurn {
    
    if (_currentGame.numberOfAvailableActions == 0) {
        return YES;
    }
    
    // Check if any units has remaining actions
    NSArray *unitsToCheck;
    
    if (_currentGame.currentPlayersTurn == _currentGame.myColor) {
        unitsToCheck = _currentGame.myDeck.cards;
    }
    else {
        unitsToCheck = _currentGame.enemyDeck.cards;
    }
    
    for (Card *card in unitsToCheck) {
        
        if (!card.dead && !card.hasPerformedActionThisRound) {
            if ([self cardIsAbleToMove:card] ||
                ([self cardIsAbleToAttack:card]) ) {
                return NO;
            }
        }
    }
    
    return YES;
}

- (BattleResult*)resolveCombatBetween:(Card*)attacker defender:(Card*)defender battleStrategy:(id<BattleStrategy>)battleStrategy {
    
    BattleResult *battleResult = [battleStrategy resolveCombatBetweenAttacker:attacker defender:defender gameManager:self];
    
    return battleResult;
}

- (void)endTurn {

    _currentGame.turnCounter++;
    
    if ((_currentGame.turnCounter % 2) == 0) {
        _currentGame.currentRound++;
        
        NSLog(@"Round increased to %d", _currentGame.currentRound);
    }

    // Reset actioncount
    _currentGame.numberOfAvailableActions = 2;
    
    // Reset movecounters på kort
    [_currentGame.myDeck resetMoveCounters];
    
    if (_currentGame.gametype == kGameTypeSinglePlayer) {
        [_currentGame.enemyDeck resetMoveCounters];
    }
    
    _currentGame.currentPlayersTurn = !_currentGame.currentPlayersTurn;
    
    if (_currentGame.gametype == kGameTypeMultiPlayer) {
        [[GCTurnBasedMatchHelper sharedInstance] endTurnWithData:[_currentGame serializeCurrentGameForPlayerWithId:[GKLocalPlayer localPlayer].playerID]];
    }
}

- (void)endGameWithGameResult:(GameResults)gameResult {
    
    _currentGame.turnCounter++;
    
    if ((_currentGame.turnCounter % 2) == 0) {
        _currentGame.currentRound++;
        
        NSLog(@"Round increased to %d", _currentGame.currentRound);
    }

    _currentGame.currentPlayersTurn = !_currentGame.currentPlayersTurn;

    if (_currentGame.gametype == kGameTypeMultiPlayer) {
        [[GCTurnBasedMatchHelper sharedInstance] endMatchWithData:[_currentGame serializeCurrentGameForPlayerWithId:[GKLocalPlayer localPlayer].playerID] gameResult:gameResult];
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
        
        if ([card isOwnedByPlayerWithColor:_currentGame.enemyColor] &&
            location.row == LOWER_BACKLINE &&
            ![card isAffectedByAbility:kAbilityBribe]) {
            
            return kGameResultDefeat;
        }

        if ([card isOwnedByPlayerWithColor:_currentGame.myColor] &&
            location.row == UPPER_BACKLINE &&
            ![card isAffectedByAbility:kAbilityBribe]) {
            return kGameResultVictory;
        }
    }

    _currentGame.gameOver = NO;
    
    return kGameResultInProgress;
}

@end
