//
//  ConstructDeckScene.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "CCLayer.h"
#import "Deck.h"

@interface ConstructDeckScene : CCLayer {
    
    CCNode *_movingNode;
    GridLocation selectedCard;
    
    CCSprite *_deckOfCards;
    
}

@property (nonatomic, strong) Deck *currentDeck;

+ (id)scene;

@end
