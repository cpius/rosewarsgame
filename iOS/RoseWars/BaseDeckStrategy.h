//
//  BaseDeckStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import <Foundation/Foundation.h>

@class GridLocation;
@class Card;
@class Deck;
@interface BaseDeckStrategy : NSObject {
    
    NSMutableArray *_cards;
}

- (BOOL)cardIsAllowedInDeck:(Card *)card;
- (BOOL)deck:(Deck *)deck containsCardInLocation:(GridLocation*)location;

@end
