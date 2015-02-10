//
//  Catapult.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "Catapult.h"

@implementation Catapult

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kSiege;
        self.unitName = kCatapult;
        self.unitAttackType = kUnitAttackTypeRanged;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:6];
        self.defence = [[HKAttribute alloc] initWithStartingValue:2];

        self.range = 3;
        self.move = 1;
        self.attackActionCost = 2;
        self.moveActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"catapult_attacksound.wav";
        self.defeatSound = @"defeat.mp3";
        
        self.frontImageSmall = @"catapult_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"catapult_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    return [[Catapult alloc] init];
}

@end
