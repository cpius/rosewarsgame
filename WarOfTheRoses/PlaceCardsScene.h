//
//  PlaceCardsScene.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/17/12.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "cocos2d.h"
#import "Deck.h"
#import "GameBoard.h"
#import "GridlLayoutManager.h"
#import "CardSprite.h"

#define NEXT_ARROW_TAG 1000
#define AUTO_TAG 1001

@interface PlaceCardsScene : CCLayer {

    CardSprite * _selectedCard;
    CardSprite *_detailCard;
    BOOL _isMovingCard;
    
    GameBoard *_gameboard;
    GameBoardNode *_hoveringOverGameBoardNode;
    
    GridlLayoutManager *_gridLayoutManager;
    
    NSMutableArray *_placedCards;
    NSMutableArray *_cardSprites;
}

@property (nonatomic, strong) Deck *currentDeck;

+ (id)scene;

@end
