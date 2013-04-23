//
//  FixedLevelIncreaseStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/22/13.
//
//

#import <Foundation/Foundation.h>
#import "LevelIncreaseStrategy.h"

@interface FixedLevelIncreaseStrategy : NSObject <LevelIncreaseStrategy>

@property (nonatomic, assign) LevelIncreaseAbilities levelIncreaseAbility;

@end
