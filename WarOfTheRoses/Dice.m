//
//  Dice.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/3/13.
//
//

#import "Dice.h"

@implementation Dice

+ (NSUInteger)rollDiceWithDie:(NSUInteger)die {
    
    return (arc4random() % (die - 1)) + 1;
}

@end
