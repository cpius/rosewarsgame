//
//  Viking.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "Viking.h"
#import "Action.h"

@implementation Viking

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kInfantry;
        self.unitName = kViking;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 2)];
        
        self.range = 1;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 2;
        
        self.attackSound = @"sword_sound.wav";
        self.frontImageSmall = @"viking_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"viking_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Viking alloc] init];
}

- (void)resetAfterNewRound {
    
    [super resetAfterNewRound];
    
    self.attackActionCost = 1;
}

- (void)combatStartingAgainstAttacker:(Card *)attacker {
    
    if (attacker.unitType == kSiege) {
        
        CCLOG(@"Viking gets +1D against siege");
        
        // +1D against siege
        _bonusAgainstSiege = [[RawBonus alloc] initWithValue:1];
        [self.defence addRawBonus:_bonusAgainstSiege];
    }
}

- (void)combatFinishedAgainstAttacker:(Card *)attacker withOutcome:(CombatOutcome)combatOutcome {
    
    if (attacker.unitType == kSiege) {
        
        [self.defence removeRawBonus:_bonusAgainstSiege];
    }
}

- (BOOL)allowPath:(NSArray *)path forActionType:(ActionTypes)actionType allLocations:(NSDictionary *)allLocations {
    
    BOOL allowPath = [super allowPath:path forActionType:actionType allLocations:allLocations];
    
    if (actionType == kActionTypeMelee) {
        if ((path != nil && path.count <= 2)) {
            allowPath = YES;
        }
    }
    
    return allowPath;
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    BOOL canPerformAction = [super canPerformActionOfType:actionType withRemainingActionCount:remainingActionCount];
    
    if (actionType == kActionTypeMelee && !self.hasPerformedAttackThisRound) {
        canPerformAction = YES;
    }
    
    return canPerformAction;
}

- (void)didPerformedAction:(Action *)action {
    
    [super didPerformedAction:action];
    
    if (action.isMove) {
        
        self.attackActionCost = 0;
    }
}

@end
