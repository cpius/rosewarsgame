//
//  FinalBonus.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//
#import "BaseBonus.h"

@class RangeAttribute;
@class GameManager;
@interface TimedBonus : BaseBonus {
    
    RangeAttribute *_parent;
    
    NSUInteger bonusValueStartedInTurn;
}

@property (nonatomic, readonly) GameManager *gamemanager;
@property (nonatomic, readonly) NSUInteger numberOfTurns;

- (id)initWithValue:(NSUInteger)bonusValue gamemanager:(GameManager*)gamemanager;
- (id)initWithValue:(NSUInteger)bonusValue forNumberOfTurns:(NSUInteger)numberOfTurns gamemanager:(GameManager*)gamemanager;

- (void)startTimedBonus:(RangeAttribute*)parent;

@end
