//
//  FixedLevelIncreaseStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/22/13.
//
//

#import "FixedLevelIncreaseStrategy.h"

@implementation FixedLevelIncreaseStrategy

- (LevelIncreaseAbilities)cardIncreasedInLevel:(Card *)card {
    
    LevelIncreaseAbilities ability;

    switch (_levelIncreaseAbility) {
        case kLevelIncreaseAbilityAttack:
            [card.attack addRawBonus:[[RawBonus alloc] initWithValue:1]];
            ability = kLevelIncreaseAbilityAttack;
            break;
            
        case kLevelIncreaseAbilityDefense:
            [card.defence addRawBonus:[[RawBonus alloc] initWithValue:1]];
            ability = kLevelIncreaseAbilityDefense;
            break;
            
        default:
            break;
    }
    
    return ability;
}

@end
