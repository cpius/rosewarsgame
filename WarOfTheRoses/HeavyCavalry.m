//
//  HeavyCavalry.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "HeavyCavalry.h"

@implementation HeavyCavalry

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kCavalry;
        self.unitName = kHeavyCalavry;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        self.range = 1;
        self.move = 2;
        actionCost = 1;
        
        hasSpecialAbility = NO;
        
        self.frontImageSmall = @"heavycavalry_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"heavycavalry_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ card {
    
    return [[HeavyCavalry alloc] init];
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return NO;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
    
}

@end
