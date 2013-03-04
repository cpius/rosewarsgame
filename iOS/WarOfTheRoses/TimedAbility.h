//
//  TimedAbility.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/4/13.
//
//

#import <Foundation/Foundation.h>

@class Card;
@interface TimedAbility : NSObject {
    
    Card *_card;
    NSUInteger _abilityStartedInRound;
}

@property (nonatomic, readonly) NSUInteger numberOfRounds;

- (id)initForNumberOfRounds:(NSUInteger)numberOfRounds;

- (void)startTimedAbilityOnCard:(Card*)card;
- (void)stopTimedAbility;

@end
