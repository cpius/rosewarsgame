//
//  Canon.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/28/13.
//
//

#import "Canon.h"
#import "Action.h"
#import "GameManager.h"

@implementation Canon

@synthesize isQuarantined = _isQuarantined;

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kSpecialUnit;
        self.unitName = kCannon;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(2, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 1)];
        
        self.range = 4;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        
        _lastAttackInRound = 0;
        
        self.attackSound = @"sword_sound.wav";
        self.frontImageSmall = @"chariot_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"chariot_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Canon alloc] init];
}

- (void)performedAction:(Action *)action {
    
    [super performedAction:action];

    if (action.isAttack) {
        _isQuarantined = YES;
        _lastAttackInRound = [GameManager sharedManager].currentGame.currentRound;
    }
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    BOOL canPerformAction = [super canPerformActionOfType:actionType withRemainingActionCount:remainingActionCount];
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return NO;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
}

@end
