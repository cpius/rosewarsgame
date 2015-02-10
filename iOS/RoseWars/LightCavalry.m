//
//  LightCavalry.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "LightCavalry.h"

@implementation LightCavalry

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kCavalry;
        self.unitName = kLightCavalry;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:2];
        self.defence = [[HKAttribute alloc] initWithStartingValue:2];

        self.range = 1;
        self.move = 4;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";
        self.frontImageSmall = @"lightcavalry_icon";
        self.frontImageLarge = [NSString stringWithFormat:@"lightcavalry_%d", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ card {
    
    return [[LightCavalry alloc] init];
}

@end
