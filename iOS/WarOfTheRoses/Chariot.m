//
//  Chariot.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/23/13.
//
//

#import "Chariot.h"
#import "Action.h"

@implementation Chariot

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kInfantry;
        self.unitName = kArcher;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        
        self.range = 1;
        self.move = 3;
        self.moveActionCost = self.attackActionCost = 1;
        
        hasSpecialAbility = YES;
        
        self.attackSound = @"sword_sound.wav";
        self.frontImageSmall = @"chariot_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"chariot_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Chariot alloc] init];
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return opponent.unitType == kInfantry;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
}

- (void)performedAction:(Action *)action {
    
    if (action.isAttack) {
        CCLOG(@"Chariot has attacked but moves are not consumed");
    }
}
@end
