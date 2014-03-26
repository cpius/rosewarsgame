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
    
    if (card.isRanged) {
        // Ranged units always get attackbonus
        ability = [self addAttackBonusToCard:card];
    }
    else {
        BOOL attributeSwitch = arc4random() % 2;
        
        if (attributeSwitch) {
            ability = [self addAttackBonusToCard:card];
        }
        else {
            ability = [self addDefenseBonusToCard:card];
        }
    }
    
    return ability;
}

- (LevelIncreaseAbilities)addDefenseBonusToCard:(Card*)card {
    [card.defence addRawBonus:[[RawBonus alloc] initWithValue:1]];
    return kLevelIncreaseAbilityDefense;
}

- (LevelIncreaseAbilities)addAttackBonusToCard:(Card*)card {
    [card.attack addRawBonus:[[RawBonus alloc] initWithValue:1]];
    return kLevelIncreaseAbilityAttack;
}

@end
