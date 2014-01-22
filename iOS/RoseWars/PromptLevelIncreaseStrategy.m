//
//  PromptLevelIncreaseStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 6/2/13.
//
//

#import "PromptLevelIncreaseStrategy.h"

@implementation PromptLevelIncreaseStrategy

- (LevelIncreaseAbilities)cardIncreasedInLevel:(Card *)card {
    
    [[NSNotificationCenter defaultCenter] postNotificationName:GAMEEVENT_LEVEL_INCREASED object:card];
    
    return kLevelIncreaseAbilityIndeterminate;
}

@end
