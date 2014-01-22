//
//  HKPlaceCardsScene.h
//  RoseWars
//
//  Created by Heine Skov Kristensen on 9/27/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>
#import "Deck.h"
#import "GameBoard.h"
#import "GridlLayoutManager.h"
#import "CardSprite.h"

@interface HKPlaceCardsScene : SKScene {
    
    CardSprite * _selectedCard;
    CardSprite *_detailCard;
    BOOL _isMovingCard;
    
    GameBoard *_gameboard;
    GameBoardNode *_hoveringOverGameBoardNode;
    
    GridlLayoutManager *_gridLayoutManager;
    
    NSMutableArray *_placedCards;
    NSMutableArray *_cardSprites;
    
    NSMutableDictionary *_homePositions;
}

@property (nonatomic, strong) Deck *currentDeck;

@end
