//
//  RandomLevelIncreaseStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/22/13.
//
//

#import "RandomLevelIncreaseStrategy.h"

@implementation RandomLevelIncreaseStrategy

- (LevelIncreaseAbilities)cardIncreasedInLevel:(Card *)card {
    
    LevelIncreaseAbilities ability;
    
    BOOL attributeSwitch = arc4random() % 2;
    
    if (attributeSwitch) {
        [card.attack addRawBonus:[[RawBonus alloc] initWithValue:1]];
        ability = kLevelIncreaseAbilityAttack;
    }
    else {
        [card.defence addRawBonus:[[RawBonus alloc] initWithValue:1]];
        ability = kLevelIncreaseAbilityDefense;
    }
    
    return ability;
}

@end
