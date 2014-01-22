//
//  RoyalGuard.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "RoyalGuard.h"
#import "Action.h"
#import "PathFinderStep.h"

@implementation RoyalGuard

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kInfantry;
        self.unitName = kRoyalGuard;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        
        self.range = 1;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"royalguard_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"royalguard_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[RoyalGuard alloc] init];
}

- (BOOL)allowPath:(NSArray *)path forActionType:(ActionTypes)actionType allLocations:(NSDictionary *)allLocations {
    
    BOOL allowPath = [super allowPath:path forActionType:actionType allLocations:allLocations];
    
    BOOL isSideways = NO;
    // Check if one of the moves is sideways
    for (PathFinderStep *step in path) {
        if (step.location.column > self.cardLocation.column ||
            step.location.column < self.cardLocation.column) {
            isSideways = YES;
        }
    }
    
    if (isSideways) {
        if (actionType == kActionTypeMove) {
            if (path != nil && path.count > 0 && path.count <= 2) {
                allowPath = YES;
            }
        }
        else if (actionType == kActionTypeMelee) {
            if ((path != nil && path.count > 0) && path.count <= 2) {
                allowPath = YES;
            }
        }
    }
    
    return allowPath;
}

- (BOOL)zoneOfControlAgainst:(Card *)opponent {

    // Opponents units can't move past royal guard
    return (self.cardColor != opponent.cardColor) && opponent.unitName != kScout;
}

- (void)combatStartingAgainstAttacker:(Card *)attacker {
    
    if (!attacker.isRanged) {
        
        NSLog(@"Royal Guard gets +1D against melee");
        
        // +1D against melee
        _bonusAgainstMelee = [[RawBonus alloc] initWithValue:1];
        [self.defence addRawBonus:_bonusAgainstMelee];
    }
}

- (void)combatFinishedAgainstAttacker:(Card *)attacker withOutcome:(CombatOutcome)combatOutcome {
    
    if (!attacker.isRanged) {
        
        [self.defence removeRawBonus:_bonusAgainstMelee];
    }
}

@end
