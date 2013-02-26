//
//  FixedDeckStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import "FixedDeckStrategy.h"
#import "CardPool.h"
#import "Deck.h"

@implementation FixedDeckStrategy

@synthesize fixedCards = _fixedCards;

- (id)init {
    
    self = [super init];
    
    if (self) {
        _fixedCards = [NSMutableArray array];
    }
    
    return self;
}

+ (id)strategy {
    
    return [[FixedDeckStrategy alloc] init];
}

- (Deck*)generateNewDeckWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType cardColor:(CardColors)cardColor {
    
    return [[Deck alloc] initWithCards:_fixedCards];
}

- (void)placeCardsInDeck:(Deck *)deck inGameBoardSide:(GameBoardSides)gameBoardSide {
    
    NSUInteger offset = 0;
    
    for (Card *card in deck.cards) {
        
        BOOL cardInValidPosition = NO;
        
        while (!cardInValidPosition) {
            
            GridLocation *location = [GridLocation gridLocationWithRow:(arc4random() % 4) + 1 + offset column:(arc4random() % 5) + 1];
            
            if (![self deck:deck containsCardInLocation:location]) {
                
                card.cardLocation = location;
                cardInValidPosition = YES;
            }
        }
    }
}

@end
