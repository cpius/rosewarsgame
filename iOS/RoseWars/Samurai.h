//
//  Samurai.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "Card.h"

@interface Samurai : Card {
    
    NSUInteger _numberOfAttacksUsed;
    BOOL _hasPerformedMove;
}

+ (id)card;

@end
