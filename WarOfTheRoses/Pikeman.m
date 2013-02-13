//
//  Pikeman.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "Pikeman.h"

@implementation Pikeman

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kInfantry;
        self.unitName = kPikeman;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(5, 6)];
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        range = 1;
        self.move = 1;
        actionCost = 1;
        
        hasSpecialAbility = YES;
        
        self.frontImageSmall = @"pikeman_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"pikeman_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Pikeman alloc]init];
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return opponent.unitType == kCavalry;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
    
}

@end
