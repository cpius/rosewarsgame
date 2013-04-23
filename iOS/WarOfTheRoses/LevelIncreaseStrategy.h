//
//  LevelIncreaseStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/22/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"

@protocol LevelIncreaseStrategy <NSObject>

- (LevelIncreaseAbilities)cardIncreasedInLevel:(Card*)card;

@end
