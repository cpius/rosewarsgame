//
//  FlagBearer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/5/13.
//
//

#import "FlagBearer.h"
#import "MeleeAttackAction.h"
#import "TimedBonus.h"
#import "GameManager.h"

@implementation FlagBearer

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kCavalry;
        self.unitName = kFlagBearer;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:2];
        self.defence = [[HKAttribute alloc] initWithStartingValue:3];
        
        self.range = 1;
        self.move = 3;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"flagbearer_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"flagbearer_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[FlagBearer alloc] init];
}

- (void)applyAoeEffectIfApplicableWhilePerformingAction:(Action *)action {
    
    // Can't apply AOE when dead
    if (self.dead) return;
    if (action.cardInAction == self) return;
    if (!action.cardInAction.isMelee) return;
    // Only affect cards of same color
    if (action.cardInAction.cardColor != self.cardColor) return;
    
    BOOL aoeIsApplicable = NO;
    NSArray *surroundingLocations = [self.cardLocation surroundingEightGridLocations];
    
    if (action.actionType == kActionTypeMelee) {

        if ([surroundingLocations containsObject:[action getEntryLocationInPath]]) {
            aoeIsApplicable = YES;
        }
    }
    else if (action.actionType == kActionTypeMove) {
        
        if ([surroundingLocations containsObject:[action getLastLocationInPath]]) {
            aoeIsApplicable = YES;
        }
    }

    if (aoeIsApplicable) {
        [action.cardInAction.attack addTimedBonus:[[TimedBonus alloc] initWithValue:2 forNumberOfTurns:2 gamemanager:self.gamemanager]];
        
        NSLog(@"Card: %@ received FlagBearers AOE bonus", action.cardInAction);

    }
}

@end
