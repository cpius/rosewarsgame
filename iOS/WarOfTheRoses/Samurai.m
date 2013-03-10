//
//  Samurai.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "Samurai.h"
#import "Action.h"

@implementation Samurai

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kInfantry;
        self.unitName = kSamurai;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        
        self.range = 1;
        self.move = 1;
        self.moveActionCost = 1;
        self.attackActionCost = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.frontImageSmall = @"samurai_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"samurai_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Samurai alloc] init];
}

- (void)resetAfterNewRound {
    
    [super resetAfterNewRound];
    
    _numberOfAttacksUsed = 0;
    self.attackActionCost = 1;
}

- (BOOL)allowPath:(NSArray *)path forActionType:(ActionTypes)actionType allLocations:(NSDictionary *)allLocations {
    
    BOOL allowPath = [super allowPath:path forActionType:actionType allLocations:allLocations];
    
    if (actionType == kActionTypeMelee) {
        if ((path != nil && path.count == 1) && _numberOfAttacksUsed < 2) {
            allowPath = YES;
        }
    }
    
    return allowPath;
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    BOOL canPerformAction = [super canPerformActionOfType:actionType withRemainingActionCount:remainingActionCount];
    
    if (actionType == kActionTypeMelee && _numberOfAttacksUsed < 2) {
        canPerformAction = YES;
    }
    
    return canPerformAction;
}

- (void)didPerformedAction:(Action *)action {
    
    [super didPerformedAction:action];
    
    if (action.isAttack) {
        if (_numberOfAttacksUsed < 2) {
            _numberOfAttacksUsed++;
            self.hasPerformedAttackThisRound = NO;
            self.attackActionCost = 0;
            
            CCLOG(@"Samurais first attack");
        }
    }
}

@end
