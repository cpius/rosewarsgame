//
//  Ballista.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "Ballista.h"

@implementation Ballista

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kSiege;
        self.unitName = kBallista;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(3, 6)];
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 1)];
        self.range = 3;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        
        hasSpecialAbility = NO;
        
        self.attackSound = @"bow_fired.wav";

        self.frontImageSmall = @"ballista_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"ballista_%d.png", self.cardColor];

        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Ballista alloc] init];
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return NO;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
    
}

@end
