//
//  Chariot.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/23/13.
//
//

#import "Hobelar.h"
#import "Action.h"
#import "ActionCostLess.h"

@implementation Hobelar

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kCavalry;
        self.unitName = kHobelar;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        
        self.range = 1;
        self.move = 3;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"defeat.mp3";
        
        self.frontImageSmall = @"chariot_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"chariot_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Hobelar alloc] init];
}

- (void)didPerformedAction:(Action *)action {
    
    if (action.isAttack) {
        self.hasPerformedAttackThisRound = YES;
        
        [self addTimedAbility:[[ActionCostLess alloc] initForNumberOfTurns:1 onCard:self]];
        
        NSLog(@"Hobelar has attacked but moves are not consumed");
    }
}
@end
