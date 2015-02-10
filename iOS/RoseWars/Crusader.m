//
//  Crusader.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/13/13.
//
//

#import "Crusader.h"
#import "GameManager.h"
#import "TimedBonus.h"

@implementation Crusader

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kCavalry;
        self.unitName = kCrusader;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:3];
        self.defence = [[HKAttribute alloc] initWithStartingValue:3];
        
        self.range = 1;
        self.move = 3;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"crusader_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"crusader_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Crusader alloc] init];
}

- (void)applyAoeEffectIfApplicableWhilePerformingAction:(Action *)action {
    
    // Can't apply AOE when dead
    if (self.dead) return;
    // Can't apply AOE to self
    if (action.cardInAction == self) return;
    // Only apply when action is move or melee
    if (action.actionType != kActionTypeMelee && action.actionType != kActionTypeMove) return;
    // Only affects melee units
    if (!action.cardInAction.isMelee) return;
    // Only affect cards of same color
    if (action.cardInAction.cardColor != self.cardColor) return;

    // When they start movement in one of the 8 nodes surrounding Crusader
    if ([[self.cardLocation surroundingEightGridLocations] containsObject:action.cardInAction.cardLocation]) {
        [action.cardInAction.attack addTimedBonus:[[TimedBonus alloc] initWithValue:1 forNumberOfTurns:2 gamemanager:self.gamemanager]];
        NSLog(@"Crusader bonus added to %@", action.cardInAction);
    }
}

@end
