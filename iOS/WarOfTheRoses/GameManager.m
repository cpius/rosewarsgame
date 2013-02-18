//
//  GameManager.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import "GameManager.h"
#import "Dice.h"
#import "RandomDeckStrategy.h"
#import "AIStrategyAdvancer.h"

@implementation GameManager

@synthesize delegate = _delegate;
@synthesize currentGame = _currentGame;
@synthesize currentPlayersTurn = _currentPlayersTurn;

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
    
    // Only 1 action in first round
    _currentGame.numberOfAvailableActions = 1;
    _currentGame.myDeck = [[Deck alloc] initWithNumberOfBasicType:7 andSpecialType:0 cardColor:_currentGame.myColor];
        
    if (gameType == kGameTypeSinglePlayer) {
        
        _enemyPlayer = [[AIPlayer alloc] initWithStrategy:[[AIStrategyAdvancer alloc] init]];
        _enemyPlayer.deckStrategy = [[RandomDeckStrategy alloc] init];
        
        _currentGame.enemyDeck = [[Deck alloc] initWithNumberOfBasicType:7 andSpecialType:0 cardColor:_currentGame.enemyColor];
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
    
    _currentGame.numberOfAvailableActions--;
    
    return _currentGame.numberOfAvailableActions;
}

- (CombatOutcome)resolveCombatBetween:(Card *)attacker defender:(Card *)defender {
    
    [_delegate combatHasStartedBetweenAttacker:attacker andDefender:defender];
    
    // An attack consumes all moves
    attacker.movesConsumed = attacker.move;
    
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
    
    NSUInteger attackRoll = [Dice rollDiceWithDie:6];
    NSUInteger defenceRoll = [Dice rollDiceWithDie:6];
    
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
        [attacker attackSuccessfulAgainstDefender:defender];
    }
    else {
        CCLOG(@"Defence successful");
        [defender defenceSuccessfulAgainstAttacker:attacker];
    }
    
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
    [_delegate turnChangedToPlayerWithColor:_currentPlayersTurn];
}

- (Action *)getActionForEnemeyPlayer {
    
    [_enemyPlayer createBattlePlansForUnits:_currentGame.enemyDeck.cards sgainstEnemyUnits:_currentGame.myDeck.cards fromUnitLayout:_currentGame.unitLayout];
    
    Action *action = [_enemyPlayer decideNextAction];
    
    return action;
}

- (GameResults)checkForEndGame {
    
    BOOL allUnitsDead = YES;
    
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

    return kGameResultInProgress;
}

@end
