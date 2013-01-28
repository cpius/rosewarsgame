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
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 6)];
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 2)];
        range = 3;
        move = 1;
        experience = 0;
        actionCost = 2;
        
        hasSpecialAbility = NO;
        
        self.frontImageSmall = @"catapult_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"catapult_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    return [[Catapult alloc] init];
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return NO;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
    
}

@end
