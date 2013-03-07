//
//  FlagBearer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/5/13.
//
//

#import "FlagBearer.h"

@implementation FlagBearer

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kSpecialUnit;
        self.unitName = kFlagBearer;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(5, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        
        self.range = 0;
        self.move = 3;
        self.moveActionCost = self.attackActionCost = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.frontImageSmall = @"flagbearer_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"flagbearer_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[FlagBearer alloc] init];
}

@end
