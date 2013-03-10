//
//  Card.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "Card.h"
#import "Action.h"

@interface Card()


@end

@implementation Card

@synthesize frontImageSmall = _frontImageSmall;
@synthesize frontImageLarge = _frontImageLarge;
@synthesize backImage = _backImage;
@synthesize cardColor = _cardColor;
@synthesize cardLocation = _cardLocation;
@synthesize isShowingDetail;
@synthesize attack = _attack, defence = _defence;
@synthesize movesConsumed;
@synthesize move;
@synthesize experience;
@synthesize range;
@synthesize isRanged;
@synthesize dead;
@synthesize moveActionCost;
@synthesize attackActionCost;
@synthesize hasReceivedExperiencePointsThisRound;
@synthesize numberOfLevelsIncreased;
@synthesize delegate = _delegate;
@synthesize attackSound = _attackSound, defenceSound = _defenceSound, moveSound = _moveSound;
@synthesize timedAbilities = _timedAbilities;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        _cardColor = kCardColorGreen;
        self.isShowingDetail = NO;
        
        _timedAbilities = [NSMutableArray array];
    }
    
    return self;
}

- (void)commonInit {
    
    self.attack.attributeAbbreviation = @"A";
    self.attack.valueAffectedByBonuses = kRangedAttributeLowerValue;
    
    self.defence.attributeAbbreviation = @"D";
    self.defence.valueAffectedByBonuses = kRangedAttributeUpperValue;
    
    self.numberOfLevelsIncreased = 0;
    self.experience = 0;
}

- (BOOL)isRanged {
    
    return self.range > 1;
}

- (NSString *)description {
    
    NSString *description = [NSString stringWithFormat:@"CardType: %d - UnitType: %d - UnitName: %d - Boardlocation: row %d column %d",
                             self.cardType,
                             self.unitType,
                             self.unitName,
                             self.cardLocation.row,
                             self.cardLocation.column];
    
    return description;
}

- (void)addTimedAbility:(TimedAbility*)timedAbility {
    
    timedAbility.delegate = self;
    
    [_timedAbilities addObject:timedAbility];
}

- (void)timedAbilityDidStop:(TimedAbility *)timedAbility {
    
    if ([_timedAbilities containsObject:timedAbility]) {
        [_timedAbilities removeObject:timedAbility];
    }
}

// Must be overloaded in subclasses
- (BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return NO;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
}

- (BOOL)zoneOfControlAgainst:(Card *)opponent {
    
    return NO;
}

- (void)combatStartingAgainstDefender:(Card *)defender {
    
}

- (void)combatStartingAgainstAttacker:(Card *)attacker {
    
}

- (void)combatFinishedAgainstAttacker:(Card *)attacker withOutcome:(CombatOutcome)combatOutcome {
    
    if (IsAttackSuccessful(combatOutcome)) {
        self.dead = YES;
    }
}

- (void)combatFinishedAgainstDefender:(Card *)defender withOutcome:(CombatOutcome)combatOutcome {
    
    if (IsAttackSuccessful(combatOutcome)) {
        // Attack succcessfull - assign experience if applicable
        if (!self.hasReceivedExperiencePointsThisRound && self.experience < 4) {
            self.experience++;
            
            // Unit can only receive experience point once every round
            self.hasReceivedExperiencePointsThisRound = YES;
            
            // Unit can only increase in level twice
            if (self.numberOfLevelsIncreased < 2 && (self.experience % 2) == 0) {
                [self levelIncreased];
            }
        }
    }
}

- (void)levelIncreased {
    
    NSLog(@"Card: %@ advanced in level", self);
    
    self.numberOfLevelsIncreased++;
    
    BOOL attributeSwitch = arc4random() % 2;
    
    if (attributeSwitch) {
        [self.attack addRawBonus:[[RawBonus alloc] initWithValue:1]];
    }
    else {
        [self.defence addRawBonus:[[RawBonus alloc] initWithValue:1]];
    }
    
    if ([_delegate respondsToSelector:@selector(cardIncreasedInLevel:)]) {
        [_delegate cardIncreasedInLevel:self];
    }
}

- (void)willPerformAction:(Action *)action {
    
}

- (void)didPerformedAction:(Action *)action {

    self.hasPerformedActionThisRound = YES;
    
    // An attack consumes all remaining moves of an unit
    if (action.isAttack) {
        self.hasPerformedAttackThisRound = YES;
        [self consumeAllMoves];
    }
}

- (BOOL)allowPath:(NSArray *)path forActionType:(ActionTypes)actionType allLocations:(NSDictionary *)allLocations {
    
    BOOL allowPath = NO;
    
    if (actionType == kActionTypeMove) {
        if (path != nil && path.count > 0 && path.count <= self.movesRemaining) {
            allowPath = YES;
        }
    }
    else if (actionType == kActionTypeMelee) {
        if ((path != nil && path.count > 0) && path.count <= self.movesRemaining) {
            allowPath = YES;
        }
    }
    else if (actionType == kActionTypeRanged) {
        if ((path != nil && path.count > 0) && path.count <= self.range) {
            allowPath = YES;
        }
    }
    
    return allowPath;
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    if (self.hasPerformedActionThisRound) {
        return NO;
    }
    
    switch (actionType) {
            
        case kActionTypeMove:
            return self.moveActionCost <= remainingActionCount && self.movesRemaining > 0;
            
        case kActionTypeAbility:
            return self.moveActionCost <= remainingActionCount;
            
        case kActionTypeMelee:
            if (self.movesRemaining == 0 || self.hasPerformedAttackThisRound) {
                return NO;
            }
            else {
                // Unit cannot move and attack the same round
                return (self.attackActionCost <= remainingActionCount) && !self.isRanged;
            }
            
        case kActionTypeRanged:
            
            if (self.movesRemaining == 0 || self.hasPerformedAttackThisRound) {
                return NO;
            }
            else {
                // Unit cannot move and attack the same round
                return (self.attackActionCost <= remainingActionCount) && self.isRanged;
            }
    }
}

- (void)consumeAllMoves {
    
    movesConsumed = move;
}

- (void)consumeMove {
    
    [self consumeMoves:1];
}

- (void)consumeMoves:(NSUInteger)moves {
    
    movesConsumed += moves;
}

- (NSInteger)movesRemaining {
    
    return move - movesConsumed;
}

- (BOOL)isOwnedByPlayerWithColor:(PlayerColors)playerColor {
    
    return (self.cardColor == kCardColorGreen && playerColor == kPlayerGreen) ||
    (self.cardColor == kCardColorRed && playerColor == kPlayerRed);
}

@end
