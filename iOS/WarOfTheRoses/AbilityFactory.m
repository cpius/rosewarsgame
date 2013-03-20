//
//  AbilityFactory.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/20/13.
//
//

#import "AbilityFactory.h"
#import "ImproveWeapons.h"

@implementation AbilityFactory

+ (TimedAbility *)createAbilityOfType:(AbilityTypes)abilityType onCard:(Card *)card {
    
    switch (abilityType) {
        case kAbilityImprovedWeapons:
            [card addTimedAbility:[[ImproveWeapons alloc] initWithCard:card]];
            
        default:
            break;
    }
    
    return nil;
}

@end
