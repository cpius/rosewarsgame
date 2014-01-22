//
//  TimedAbilityForSerialization.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/25/13.
//
//

#import <Foundation/Foundation.h>
#import "TimedAbility.h"

@interface TimedAbilityForSerialization : NSObject {
    
    TimedAbility *_timedAbility;
}

@property (nonatomic, strong) NSNumber *abilityType;
@property (nonatomic, strong) NSNumber *numberOfTurns;
@property (nonatomic, strong) NSNumber *startedInTurn;

- (id)initWithTimedAbility:(TimedAbility*)timedAbility currentTurn:(NSUInteger)currentTurn;

- (NSDictionary *)asDictionary;

@end
