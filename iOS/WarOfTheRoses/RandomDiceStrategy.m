//
//  Dice.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/3/13.
//
//

#import "RandomDiceStrategy.h"

@implementation RandomDiceStrategy

+ (id)strategy {
    
    return [[RandomDiceStrategy alloc] init];
}

- (NSUInteger)rollDiceWithDie:(NSUInteger)die {
    
    return (arc4random() % die) + 1;
}

@end
