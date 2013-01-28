//
//  Archer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "Archer.h"

@implementation Archer

-(id)init {
    self = [super init];
    
    if (self) {
                
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kInfantry;
        self.unitName = kArcher;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(5, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 2)];
        
        range = 4;
        move = 1;
        experience = 0;
        actionCost = 1;
        
        hasSpecialAbility = YES;
        
        self.frontImageSmall = @"archer_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"archer_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Archer alloc] init];
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return opponent.unitType == kInfantry;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
}

@end
