//
//  HeavyCavalry.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "Knight.h"

@implementation Knight

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kCavalry;
        self.unitName = kKnight;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        self.range = 1;
        self.move = 2;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"heavycavalry_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"heavycavalry_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ card {
    
    return [[Knight alloc] init];
}

@end