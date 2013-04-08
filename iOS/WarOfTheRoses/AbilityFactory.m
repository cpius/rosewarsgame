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

+ (void)addAbilityOfType:(AbilityTypes)abilityType onCard:(Card *)card {
    
    switch (abilityType) {
        case kAbilityImprovedWeapons:
            [card addTimedAbility:[[ImproveWeapons alloc] initForNumberOfTurns:2 onCard:card]];
            break;
            
        case kAbilityCoolDown:
            [card addTimedAbility:[[CoolDown alloc] initForNumberOfTurns:2 onCard:card]];
            break;
            
        case kAbilityBribe:
            [card addTimedAbility:[[Bribe alloc] initForNumberOfTurns:1 onCard:card]];
            break;
            
        default:
            break;
    }
}

/*+ (void)addAbilityOfType:(AbilityTypes)abilityType onCard:(Card *)card {

    [self addAbilityOfType:abilityType onCard:card forNumberOfTurns:1];
}
*/
@end
