//
//  DiceStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/26/13.
//
//

#import <Foundation/Foundation.h>

@protocol DiceStrategy <NSObject>

@required
- (NSUInteger)rollDiceWithDie:(NSUInteger)die;
+ (id)strategy;

@end
