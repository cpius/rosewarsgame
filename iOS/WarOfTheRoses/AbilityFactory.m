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

@interface AbilityFactory()

//+ (void)addAbilityOfType:(AbilityTypes)abilityType onCard:(Card *)card forNumberOfTurns:(NSUInteger)numberOfTurns;

@end

@implementation AbilityFactory

+ (void)reapplyExistingAbilityOfType:(AbilityTypes)abilityType onCard:(Card *)card withAbilityData:(NSDictionary*)abilityData {
    
    TimedAbility *ability;
    
    switch (abilityType) {
        case kAbilityImprovedWeapons:
            ability = [[ImproveWeapons alloc] initExistingAbilityWithAbilityData:abilityData onCard:card];
            break;
            
        case kAbilityCoolDown:
            ability = [[CoolDown alloc] initExistingAbilityWithAbilityData:abilityData onCard:card];
            break;
            
        case kAbilityBribe:
            ability = [[Bribe alloc] initExistingAbilityWithAbilityData:abilityData onCard:card];
            break;
            
        default:
            break;
    }
    
    if (ability.numberOfTurns > 0) {
        [card addTimedAbility:ability];
    }
}

+ (TimedAbility*)addAbilityOfType:(AbilityTypes)abilityType onCard:(Card *)card {
    
    TimedAbility *timedAbility;
    
    switch (abilityType) {
        case kAbilityImprovedWeapons:
            timedAbility = [[ImproveWeapons alloc] initForNumberOfTurns:2 onCard:card];
            break;
            
        case kAbilityCoolDown:
            timedAbility = [[CoolDown alloc] initForNumberOfTurns:2 onCard:card];
            break;
            
        case kAbilityBribe:
            timedAbility = [[Bribe alloc] initForNumberOfTurns:1 onCard:card];
            break;
            
        default:
            break;
    }
    
    [card addTimedAbility:timedAbility];
    
    return timedAbility;
}

@end
