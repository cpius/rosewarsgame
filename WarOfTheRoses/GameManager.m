//
//  GameManager.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import "GameManager.h"
#import "Dice.h"

@implementation GameManager

@synthesize currentGame = _currentGame;

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
        
        _enemyPlayer = [[AIPlayer alloc] init];
        
        _currentGame.enemyDeck = [[Deck alloc] initWithNumberOfBasicType:7 andSpecialType:0 cardColor:_currentGame.enemyColor];
        [_enemyPlayer placeCardsInDeck:_currentGame.enemyDeck];
    }
}

- (NSUInteger)actionUsed {
    
    _currentGame.numberOfAvailableActions--;
    
    return _currentGame.numberOfAvailableActions;
}

- (CombatOutcome)resolveCombatBetween:(Card *)attacker defender:(Card *)defender {
    
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
    
    NSUInteger attackRoll = [Dice rollDiceWithDie:6];
    NSUInteger defenceRoll = [Dice rollDiceWithDie:6];
    
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
    
    if (kCombatOutcomeAttackSuccessful) {
        [attacker attackSuccessfulAgainstDefender:defender];
    }
    else {
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
}

@end
