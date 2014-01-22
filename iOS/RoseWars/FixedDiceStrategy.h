//
//  FixedDiceStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/26/13.
//
//

#import <Foundation/Foundation.h>
#import "DiceStrategy.h"

@interface FixedDiceStrategy : NSObject <DiceStrategy>

- (NSUInteger)rollDiceWithDie:(NSUInteger)die;
+ (id)strategyWithFixedValue:(NSUInteger)fixedValue;

@property (nonatomic, assign) NSUInteger fixedDieValue;

@end
