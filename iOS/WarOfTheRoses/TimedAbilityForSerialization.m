//
//  TimedAbilityForSerialization.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/25/13.
//
//

#import "TimedAbilityForSerialization.h"

@implementation TimedAbilityForSerialization

- (id)initWithTimedAbility:(TimedAbility *)timedAbility {
    
    self = [super init];
    
    if (self) {
        
        _abilityType = @(timedAbility.abilityType);
        _startedInRound = @(timedAbility.abilityStartedInRound);
        _numberOfRounds = @(timedAbility.numberOfRounds);
    }
    
    return self;
}

- (NSDictionary *)asDictionary {
    
    NSMutableDictionary *abilities = [NSMutableDictionary dictionaryWithObjectsAndKeys:_abilityType, @"abilitytype",
                                     _startedInRound, @"startedinround",
                                     _numberOfRounds, @"numberofrounds",
                                     nil];
    
    
    return abilities;
}

@end
