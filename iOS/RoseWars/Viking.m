//
//  Viking.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "Viking.h"
#import "Action.h"
#import "MeleeAttackAction.h"

@interface Viking()

@property (nonatomic, strong) RawBonus *bonusAgainstSiege;

@end

@implementation Viking

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kInfantry;
        self.unitName = kViking;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:3];
        self.defence = [[HKAttribute alloc] initWithStartingValue:2];
        
        self.range = 1;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 2;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"viking_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"viking_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Viking alloc] init];
}

- (NSUInteger)meleeRange {
    
    return 2;
}

- (void)resetAfterNewRound {
    
    [super resetAfterNewRound];
    
    self.attackActionCost = 1;
}

- (void)combatStartingAgainstAttacker:(Card *)attacker {
    
    if (attacker.unitType == kSiege) {
        
        NSLog(@"Viking gets +1D against siege");
        
        // +1D against siege
        self.bonusAgainstSiege = [[RawBonus alloc] initWithValue:1];
        [self.defence addRawBonus:self.bonusAgainstSiege];
    }
}

- (void)combatFinishedAgainstAttacker:(Card *)attacker withOutcome:(CombatOutcome)combatOutcome {
    
    if (attacker.unitType == kSiege) {
        
        [self.defence removeRawBonus:self.bonusAgainstSiege];
    }
}

- (BOOL)allowAction:(Action *)action allLocations:(NSDictionary*)allLocations {
    
    BOOL allowAction = [super allowAction:action allLocations:allLocations];

    if (action.actionType == kActionTypeMelee) {
        
        MeleeAttackAction *meleeAction = (MeleeAttackAction*)action;
        
        if ((meleeAction.path != nil && meleeAction.path.count <= 2 && meleeAction.meleeAttackType == kMeleeAttackTypeNormal)) {
            allowAction = YES;
        }
    }
    
    return allowAction;
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
