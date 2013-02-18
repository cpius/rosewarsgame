//
//  GameBoard.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/7/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameBoard.h"
#import "ParticleHelper.h"
#import "MovePathFinderStrategy.h"
#import "MeleeAttackPathFinderStrategy.h"
#import "RangedAttackAction.h"
#import "PathFinderStrategyFactory.h"

@interface GameBoard()

@end

@implementation GameBoard

@synthesize rows, columns;
@synthesize colorOfTopPlayer, colorOfBottomPlayer;
@synthesize delegate = _delegate;
@synthesize isMoving = _isMoving;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        self.contentSize = CGSizeMake(320, 375);
        
        _greenBackgroundImageName = @"greenbackground.png";
        _redBackgroundImageName = @"redbackground.png";
        
        _highlightedNodes = [NSMutableArray array];
    }
    
    return self;
}

- (void)layoutDeck:(NSMutableArray*)deck forPlayerWithColor:(PlayerColors)color {

    NSUInteger rowOffset = 0;
    
    if (color == kPlayerGreen && colorOfBottomPlayer == kPlayerGreen) {
        rowOffset = 4;
    }
    
    if (color == kPlayerRed && colorOfBottomPlayer == kPlayerRed) {
        rowOffset = 4;
    }
    
    for (CardSprite *cardSprite in deck) {
        
        GameBoardNode *node = [self getGameBoardNodeForGridLocation:[GridLocation gridLocationWithRow:cardSprite.model.cardLocation.row + rowOffset column:cardSprite.model.cardLocation.column]];
        
        if (node != nil) {
            
            [self placeCard:cardSprite inGameBoardNode:node useHighLighting:NO onCompletion:nil];
        }
    }
}

- (void)removeCardAtGameBoardNode:(GameBoardNode *)node {
    
    if (node.card != nil) {
        [node.card removeFromParentAndCleanup:YES];
    }
}

- (void)replaceCardAtGameBoardNode:(GameBoardNode *)node withCard:(CardSprite *)card {
    
    [node.card removeFromParentAndCleanup:YES];
    node.card = card;
}

- (void)swapCardFromNode:(GameBoardNode *)fromNode toNode:(GameBoardNode *)toNode {
    
    toNode.card = fromNode.card;
    fromNode.card = nil;
}

- (Action*)getActionsToGameBoardNode:(GameBoardNode *)toNode allLocations:(NSMutableDictionary*)allLocations {
    
    return [self getActionsfromGameBoardNode:_activeNode toGameBoardNode:toNode allLocations:allLocations];
}

- (Action*)getActionsfromGameBoardNode:(GameBoardNode *)fromNode toGameBoardNode:(GameBoardNode *)toNode allLocations:(NSMutableDictionary*)allLocations {
        
    GridLocation *fromLocation = fromNode.locationInGrid;
    GridLocation *toLocation = toNode.locationInGrid;
    
    if ([fromLocation isEqual:toLocation]) {
        CCLOG(@"Can't move to current location");
        return nil;
    }
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    Action *action = nil;
    id<PathFinderStrategy> strategy = [PathFinderStrategyFactory getStrategyFromCard:fromNode.card.model toCard:toNode.card.model myColor:colorOfBottomPlayer];
    
    NSArray *path = [pathFinder getPathForCard:fromNode.card.model fromGridLocation:fromLocation toGridLocation:toLocation usingStrategy:strategy allLocations:allLocations];
    
    if (toNode.hasCard && [toNode.card.model isOwnedByPlayerWithColor:colorOfTopPlayer]) {
        if ((path.count - 1) > 1 && fromNode.card.model.isRanged) {
            action = [[RangedAttackAction alloc] initWithPath:path andCardInAction:fromNode.card.model enemyCard:toNode.card.model];
        }
        else {
            action = [[MeleeAttackAction alloc] initWithPath:path andCardInAction:fromNode.card.model enemyCard:toNode.card.model];
        }
    }
    else {
        action = [[MoveAction alloc] initWithPath:path andCardInAction:fromNode.card.model];
    }
        
    return action;
}

- (void)moveActiveGameBoardNodeFollowingPath:(NSArray *)path onCompletion:(void (^)())completion {
    
    NSMutableArray *tempPath = [NSMutableArray arrayWithArray:path];
    
    if (tempPath.count == 0) {
        return;
    }
    else {
        _isMoving = YES;
    }
        
    PathFinderStep *step = [tempPath objectAtIndex:0];
    
    GameBoardNode *nextNode = [self getGameBoardNodeForGridLocation:step.location];
    
    CGPoint position = [self convertToWorldSpace:nextNode.position];
    CCMoveTo *moveAction = [CCMoveTo actionWithDuration:0.2 position:position];
    CCCallBlock *popStep = [CCCallBlock actionWithBlock:^{
        
        if ([_delegate respondsToSelector:@selector(card:movedToNode:)]) {
            [_delegate card:_activeNode.card movedToNode:nextNode];
        }
        
        if (tempPath.count == 0) {
            
            _isMoving = NO;
            completion();
        }
        else {
            [self moveActiveGameBoardNodeFollowingPath:[NSArray arrayWithArray:tempPath] onCompletion:completion];
        }
    }];
    
    [tempPath removeObject:step];

    [_activeNode.card runAction:[CCSequence actions:moveAction, popStep, nil]];
}

- (void)placeCard:(CardSprite *)cardSprite inGameBoardNode:(GameBoardNode *)node useHighLighting:(BOOL)highlighting onCompletion:(void (^)())completion {

    CGPoint position = [self convertToWorldSpace:node.position];
    
    cardSprite.model.cardLocation = node.locationInGrid;
    [cardSprite setZOrder:5];
 
    CCMoveTo *moveAction = [CCMoveTo actionWithDuration:0.2 position:position];
    CCScaleTo *scaleAction = [CCScaleTo actionWithDuration:0.2 scale:0.40];
    [cardSprite runAction:[CCSpawn actions:moveAction, scaleAction, nil]];
    
    CCScaleTo *scaleDownAction = [CCScaleTo actionWithDuration:0.2 scale:1.0];
    
    CCCallBlock *complete = [CCCallBlock actionWithBlock:^{
        
        if (completion != nil) {
            completion();
        }
    }];
    
    [node runAction:[CCSequence actions:scaleDownAction, complete, nil]];
   
    node.card = cardSprite;
    
    if (highlighting) {
        [ParticleHelper applyBurstToNode:node];
    }
}


- (void)layoutBoard {
    
    _boardNodes = [NSMutableArray arrayWithCapacity:rows*columns];
    NSString *spriteName;
    
    for (int row = 0; row < rows; row++) {
        for (int column = 0; column < columns; column++) {
            
            if (row < (rows / 2)) {
                if (colorOfTopPlayer == kPlayerGreen) {
                    spriteName = _greenBackgroundImageName;
                }
                else {
                    spriteName = _redBackgroundImageName;
                }
            }
            else {
                if (colorOfBottomPlayer == kPlayerGreen) {
                    spriteName = _greenBackgroundImageName;
                }
                else {
                    spriteName = _redBackgroundImageName;
                }
            }
            
            GameBoardNode *node = [[GameBoardNode alloc] initWithSprite:[CCSprite spriteWithFile:spriteName]];
            
            
            node.locationInGrid = [GridLocation gridLocationWithRow:row + 1 column:column + 1];
            CCLabelTTF *label = [CCLabelTTF labelWithString:[NSString stringWithFormat:@"%d,%d", node.locationInGrid.row, node.locationInGrid.column] fontName:APP_FONT fontSize:10];
            node.position = ccp((column * node.contentSize.width) + node.contentSize.width / 2, self.contentSize.height - ((row * node.contentSize.height) +node.contentSize.height / 2));
            label.anchorPoint = ccp(0.5, 0.5);
            label.position = ccp(node.contentSize.width / 2, node.contentSize.height / 2);
            label.color = ccc3(0, 0, 0);
            
            [self addChild:node];
            [node addChild:label z:10];
            [_boardNodes addObject:node];
        }
    }
}

- (GameBoardNode*)getGameBoardNodeForPosition:(CGPoint)position {

    for (GameBoardNode *node in self.children) {
        
        if (CGRectContainsPoint(node.boundingBox, position)) {
            return node;
        }
    }
    
    return nil;
}

- (GameBoardNode *)getGameBoardNodeForGridLocation:(GridLocation*)gridLocation {
    
    for (GameBoardNode *node in _boardNodes) {
        
        if ([node.locationInGrid isEqual:gridLocation]) {
            return node;
        }
    }
    
    return nil;
}

- (BOOL)nodeIsActive {
    
    return _activeNode != nil;
}

- (GameBoardNode *)activeNode {
    
    return _activeNode;
}

- (void)highlightNodeAtLocation:(GridLocation*)location withColor:(ccColor3B)color {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    if (node != nil) {
        [node.nodeSprite runAction:[CCTintTo actionWithDuration:0.2 red:color.r green:color.g blue:color.b]];
        
        if (![_highlightedNodes containsObject:node.nodeSprite]) {
            [_highlightedNodes addObject:node.nodeSprite];
        }
    }
}

- (void)highlightCardAtLocation:(GridLocation *)location withColor:(ccColor3B)color {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    if (node != nil && node.card != nil) {
        [node.card runAction:[CCTintTo actionWithDuration:0.2 red:color.r green:color.g blue:color.b]];
        
        if (![_highlightedNodes containsObject:node.card]) {
            [_highlightedNodes addObject:node.card];
        }
    }
}

- (void)deHighlightAllNodes {
    
    for (CCSprite *sprite in _highlightedNodes) {
        [sprite runAction:[CCTintTo actionWithDuration:0.2 red:255 green:255 blue:255]];
    }
}

- (void)selectCardInGameBoardNode:(GameBoardNode *)node useHighlighting:(BOOL)highlight {
    
    [self deselectActiveNode];
        
    [node setZOrder:500];
    [node.card setZOrder:501];
    [node.card runAction:[CCTintTo actionWithDuration:0.2 red:0 green:0 blue:235]];
    [ParticleHelper highlightNode:node.card forever:YES];
    
    _activeNode = node;
    _activeCard = node.card;
}

- (void)deselectActiveNode {
    
    if ([self nodeIsActive]) {
        [_activeNode setZOrder:0];
        [_activeNode.card setZOrder:1];
        [ParticleHelper stopHighlightingNode:_activeCard];
        
        [_activeCard setColor:ccc3(255, 255, 255)];
        
        _activeCard = nil;
        _activeNode = nil;
    }
}

@end
