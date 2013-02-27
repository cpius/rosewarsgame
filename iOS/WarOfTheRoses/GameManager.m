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

#import "AIStrategyAdvancer.h"
#import "AIStrategyCatapulter.h"

@implementation GameManager

@synthesize delegate = _delegate;
@synthesize currentGame = _currentGame;
@synthesize currentPlayersTurn = _currentPlayersTurn;
@synthesize attackerDiceStrategy = _attackerDiceStrategy;
@synthesize defenderDiceStrategy = _defenderDiceStrategy;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        _currentGame = [[Game alloc] init];
        
        self.attackerDiceStrategy = [RandomDiceStrategy strategy];
        self.defenderDiceStrategy = [RandomDiceStrategy strategy];
        
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
    
    // Only 1 action in first round
    _currentGame.numberOfAvailableActions = 1;
    _currentGame.myDeck = [_deckStrategy generateNewDeckWithNumberOfBasicType:7 andSpecialType:0 cardColor:_currentGame.myColor];
    
    if (gameType == kGameTypeSinglePlayer) {
        
        _enemyPlayer = [[AIPlayer alloc] initWithStrategy:[[AIStrategyAdvancer alloc] init]];
        _enemyPlayer.deckStrategy = [[RandomDeckStrategy alloc] init];
        
        _currentGame.enemyDeck = [_deckStrategy generateNewDeckWithNumberOfBasicType:7 andSpecialType:0 cardColor:_currentGame.enemyColor];
        [_enemyPlayer placeCardsInDeck:_currentGame.enemyDeck];
    }
    
    // TODO: Random starter
    _currentPlayersTurn = kPlayerGreen;
}

- (void)card:(Card *)card movedToGridLocation:(GridLocation *)location {
    
    NSLog(@"Card: %@ moved to location: %@", card, location);
    
    [_currentGame.unitLayout removeObjectForKey:card.cardLocation];
    
    card.cardLocation = location;
    [_currentGame.unitLayout setObject:card forKey:location];
}

- (void)cardHasBeenDefeated:(Card *)card {
    
    NSLog(@"Card: %@ has been defeated - remove from game", card);
    
    card.dead = YES;
    
    [_currentGame.unitLayout removeObjectForKey:card.cardLocation];
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

- (CombatOutcome)resolveCombatBetween:(Card *)attacker defender:(Card *)defender {
    
    [_delegate combatHasStartedBetweenAttacker:attacker andDefender:defender];
        
    CCLOG(@"Resolving combat between attacker: %@ and defender: %@", attacker, defender);
    
    if ([attacker specialAbilityTriggersVersus:defender]) {
        
        // Attacker has special against defender
        [attacker addSpecialAbilityVersusOpponent:defender];
    }
    
    if ([defender specialAbilityTriggersVersus:attacker]) {
        
        // Defender has special against attacker
        [defender addSpecialAbilityVersusOpponent:attacker];
    }
    
    AttributeRange attackValue = [attacker.attack calculateValue];
    AttributeRange defendValue = [defender.defence calculateValue];
    
    CCLOG(@"Attack value: %@", AttributeRangeToNSString(attackValue));
    CCLOG(@"Defend value: %@", AttributeRangeToNSString(defendValue));
    
    NSUInteger attackRoll = [_attackerDiceStrategy rollDiceWithDie:6];
    NSUInteger defenceRoll = [_defenderDiceStrategy rollDiceWithDie:6];
    
    CCLOG(@"Attack roll: %d", attackRoll);
    CCLOG(@"Defence roll: %d", defenceRoll);
    
    CombatOutcome outcome;
    
    // Check attackroll
    if (attackRoll >= attackValue.lowerValue && attackRoll <= attackValue.upperValue) {
        // Check defenceroll
        if (defenceRoll >= defendValue.lowerValue && defenceRoll <= defendValue.upperValue) {
            outcome = kCombatOutcomeDefendSuccessful;
        }
        else {
            outcome = kCombatOutcomeAttackSuccessful;
        }
    }
    else {
        outcome = kCombatOutcomeDefendSuccessful;
    }
    
    if (outcome == kCombatOutcomeAttackSuccessful) {
        CCLOG(@"Attack successful");
        [self cardHasBeenDefeated:defender];
        [_delegate cardHasBeenDefeatedInCombat:defender];
    }
    else {
        CCLOG(@"Defend successful");
    }
    
    [attacker combatFinishedAgainstDefender:defender withOutcome:outcome];
    [defender combatFinishedAgainstAttacker:attacker withOutcome:outcome];
    
    return outcome;
}

- (void)endTurn {
    
    _currentGame.currentRound++;

    // Reset actioncount
    if (_currentGame.currentRound > 1) {
        _currentGame.numberOfAvailableActions = 2;
    }
    
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
