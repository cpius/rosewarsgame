//
//  AbilityFactory.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/20/13.
//
//

#import <Foundation/Foundation.h>
#import "TimedAbility.h"

@interface AbilityFactory : NSObject

+ (TimedAbility*)addAbilityOfType:(AbilityTypes)abilityType onCard:(Card*)card;

@end
