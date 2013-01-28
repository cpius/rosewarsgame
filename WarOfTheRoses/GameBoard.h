//
//  GameBoard.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/7/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "cocos2d.h"
#import "Deck.h"
#import "GameBoardNode.h"


@interface GameBoard : CCSprite {
    
    NSString *_redBackgroundImageName;
    NSString *_greenBackgroundImageName;
    NSMutableArray *_boardNodes;
    
    BOOL _isZooming;
    GameBoardNode *_zoomInOnNode;
}

@property (nonatomic, readonly) PlayerColors playerColor;
@property (nonatomic, assign) NSUInteger rows;
@property (nonatomic, assign) NSUInteger columns;
@property (nonatomic, assign) PlayerColors colorOfTopPlayer;
@property (nonatomic, assign) PlayerColors colorOfBottomPlayer;

- (id)initWithPlayerColor:(PlayerColors)playerColor;

- (void)layoutBoard;
- (void)layoutDeck:(Deck*)deck forPlayerWithColor:(PlayerColors)color;

- (void)placeCard:(Card *)card inGameBoardNode:(GameBoardNode *)node;

- (GameBoardNode*)getGameBoardNodeForPosition:(CGPoint)position;
- (GameBoardNode*)getGameBoardNodeForGridLocation:(GridLocation)gridLocation;
- (NSArray*)getAdjacentGameBoardNodesToCard:(Card*)card;

-(void) zoomInOnGameBoardNode:(GameBoardNode*)node;

@end
