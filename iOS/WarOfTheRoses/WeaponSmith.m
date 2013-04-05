//
//  WeaponSmith.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/19/13.
//
//

#import "WeaponSmith.h"
#import "ImproveWeapons.h"

@implementation WeaponSmith

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kInfantry;
        self.unitName = kWeaponSmith;
        self.unitAttackType = kUnitAttackTypeCaster;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(0, 0)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 2)];
        
        self.range = 3;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"weaponsmith_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"weaponsmith_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[WeaponSmith alloc] init];
}

- (NSArray *)abilities {
    
    return @[@(kAbilityImprovedWeapons)];
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    BOOL canPerformAction = [super canPerformActionOfType:actionType withRemainingActionCount:remainingActionCount];
    
    // Weaponsmith can't attack
    if (actionType == kActionTypeMelee || actionType == kActionTypeRanged) {
        canPerformAction = NO;
    }
    
    return canPerformAction;
}

- (BOOL)isValidTarget:(Card*)targetCard {
    
    return [targetCard isOwnedByMe] && targetCard.isMelee;
    
}

@end
