//
//  Scout.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/4/13.
//
//

#import "Scout.h"
#import "GameManager.h"

@implementation Scout

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kSpecialUnit;
        self.unitName = kScout;
        self.unitAttackType = kUnitAttackTypeMelee;
       
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(0, 0)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 2)];
        
        self.range = 0;
        self.move = 4;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.frontImageSmall = @"scout_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"scout_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Scout alloc] init];
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    BOOL canPerformAction = [super canPerformActionOfType:actionType withRemainingActionCount:remainingActionCount];
    
    // Scout can't attack
    if (actionType == kActionTypeMelee) {
        canPerformAction = NO;
    }
    
    // Scout can't move the first round
    if ([GameManager sharedManager].currentGame.currentRound == 1) {
        canPerformAction = NO;
    }

    return canPerformAction;
}

- (BOOL)allowPath:(NSArray *)path forActionType:(ActionTypes)actionType allLocations:(NSDictionary *)allLocations {
    
    BOOL allowPath = [super allowPath:path forActionType:actionType allLocations:allLocations];
        
    return allowPath;
}

@end
