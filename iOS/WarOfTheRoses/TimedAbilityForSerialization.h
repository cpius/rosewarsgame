//
//  TimedAbilityForSerialization.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/25/13.
//
//

#import <Foundation/Foundation.h>
#import "TimedAbility.h"

@interface TimedAbilityForSerialization : NSObject

@property (nonatomic, strong) NSNumber *abilityType;
@property (nonatomic, strong) NSNumber *startedInRound;
@property (nonatomic, strong) NSNumber *numberOfRounds;

- (id)initWithTimedAbility:(TimedAbility*)timedAbility;

- (NSDictionary *)asDictionary;

@end
