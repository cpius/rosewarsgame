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
#import "PathFinder.h"
#import "CardSprite.h"
#import "MoveAction.h"
#import "MeleeAttackAction.h"
#import "RangedAttackAction.h"

@protocol GameBoardActionProtocol <NSObject>

@optional
- (void)attackInitiatedBetweenYourCard:(Card*)myCard andEnemyCard:(Card*)enemyCard;
- (void)card:(CardSprite*)card movedToNode:(GameBoardNode*)node;

@end

@interface GameBoard : CCSprite {
    
    NSString *_redBackgroundImageName;
    NSString *_greenBackgroundImageName;
    NSMutableArray *_boardNodes;
    
    BOOL _isZooming;
    
    GameBoardNode *_zoomInOnNode;
    GameBoardNode *_activeNode;
    CardSprite *_activeCard;
    
    NSMutableArray *_highlightedNodes;
    NSMutableArray *_highlightedCards;
}

@property (nonatomic, weak) id<GameBoardActionProtocol> delegate;
@property (nonatomic, assign) NSUInteger rows;
@property (nonatomic, assign) NSUInteger columns;
@property (nonatomic, assign) PlayerColors colorOfTopPlayer;
@property (nonatomic, assign) PlayerColors colorOfBottomPlayer;
@property (nonatomic, readonly) BOOL isMoving;

- (void)layoutBoard;
- (void)layoutDeck:(NSMutableArray*)deck forPlayerWithColor:(PlayerColors)color;

- (void)placeCard:(CardSprite *)cardSprite inGameBoardNode:(GameBoardNode *)node useHighLighting:(BOOL)highlighting onCompletion:(void (^)())completion;

- (void)moveCardAtLocation:(GridLocation*)location followingPath:(NSArray*)path onCompletion:(void (^)())completion;
- (void)moveActiveGameBoardNodeFollowingPath:(NSArray *)path onCompletion:(void (^)())completion;

- (void)selectCardInGameBoardNode:(GameBoardNode*)node useHighlighting:(BOOL)highlight;
- (void)replaceCardAtGameBoardNode:(GameBoardNode *)node withCardInGameBoardNode:(GameBoardNode *)replaceWithNode;
- (void)removeCard:(CardSprite*)card;
- (void)removeCardAtGameBoardNode:(GameBoardNode*)node;
- (void)deselectActiveNode;
- (BOOL)nodeIsActive;
- (GameBoardNode*)activeNode;

- (GameBoardNode*)getGameBoardNodeForPosition:(CGPoint)position;
- (GameBoardNode*)getGameBoardNodeForGridLocation:(GridLocation*)gridLocation;

- (void)swapCardFromNode:(GameBoardNode*)fromNode toNode:(GameBoardNode*)toNode;

- (void)highlightNodesForAttackDirectionAtLocations:(NSArray *)locations;
- (void)highlightSelectedAttackDirectionAtLocation:(GridLocation*)location;
- (void)deHighlightSelectedAttackDirectionAtLocation:(GridLocation*)location;


- (void)highlightNodeAtLocation:(GridLocation*)location withColor:(ccColor3B)color;
- (void)highlightCardAtLocation:(GridLocation *)location withColor:(ccColor3B)color;
- (void)highlightCardAtLocation:(GridLocation*)location withColor:(ccColor3B)color actionType:(ActionTypes)actionType;
- (void)deHighlightAllNodes;
- (void)deHighlightNode:(GameBoardNode*)node;
- (void)deHighlightNodeAtLocation:(GridLocation *)location;

@end
