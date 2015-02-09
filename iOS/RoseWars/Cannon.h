//
//  Canon.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/28/13.
//
//

#import "Card.h"

@interface Cannon : Card {
    
    NSUInteger _lastAttackInRound;
}

@property (nonatomic, readonly) BOOL isQuarantined;

+ (id)card;

@end
