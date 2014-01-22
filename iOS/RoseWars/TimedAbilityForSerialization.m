//
//  TimedAbilityForSerialization.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/25/13.
//
//

#import "TimedAbilityForSerialization.h"

@implementation TimedAbilityForSerialization

- (id)initWithTimedAbility:(TimedAbility *)timedAbility currentTurn:(NSUInteger)currentTurn {
    
    self = [super init];
    
    if (self) {
        
        _timedAbility = timedAbility;
        
        _abilityType = @(timedAbility.abilityType);
        _startedInTurn = @(timedAbility.abilityStartedInTurn);
        
        _numberOfTurns = @(_timedAbility.numberOfTurns - 1);
    }
    
    return self;
}

- (NSDictionary *)asDictionary {
    
    NSMutableDictionary *abilities = [NSMutableDictionary dictionaryWithObjectsAndKeys:_abilityType, @"abilitytype",
                                     _numberOfTurns, @"numberofturns",
                                     _startedInTurn, @"started_in_turn",
                                     nil];
    
    [abilities addEntriesFromDictionary:[_timedAbility asDictionary]];
    
    return abilities;
}

@end
