//
//  AbilityFactory.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/20/13.
//
//

#import "AbilityFactory.h"
#import "ImproveWeapons.h"
#import "CoolDown.h"
#import "Bribe.h"

@implementation AbilityFactory

+ (TimedAbility *)addAbilityOfType:(AbilityTypes)abilityType onCard:(Card *)card {
    
    switch (abilityType) {
        case kAbilityImprovedWeapons:
            [card addTimedAbility:[[ImproveWeapons alloc] initOnCard:card]];
            break;
            
        case kAbilityCoolDown:
            [card addTimedAbility:[[CoolDown alloc] initOnCard:card]];
            break;
            
        case kAbilityBribe:
            [card addTimedAbility:[[Bribe alloc] initOnCard:card]];
            break;
            
        default:
            break;
    }
    
    return nil;
}

@end
