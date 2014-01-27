//
//  Dice.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/3/13.
//
//

#import <Foundation/Foundation.h>
#import "DiceStrategy.h"

@interface RandomDiceStrategy : NSObject <DiceStrategy>

- (NSUInteger)rollDiceWithDie:(NSUInteger)die;

@end
