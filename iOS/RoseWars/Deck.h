//
//  Deck.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"

@interface Deck : NSObject {
}

@property (nonatomic, strong) NSArray *cards;

- (id)initWithCards:(NSArray*)cards;

- (void)resetMoveCounters;

@end
