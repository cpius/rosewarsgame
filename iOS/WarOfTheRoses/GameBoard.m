//
//  GameBoard.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/7/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameBoard.h"
#import "ParticleHelper.h"
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
        _highlightedCards = [NSMutableArray array];
    }
    
    return self;
}

- (void)layoutDeck:(NSMutableArray*)deck forPlayerWithColor:(PlayerColors)color {

    NSUInteger rowOffset = 0;
    
    for (CardSprite *cardSprite in deck) {
        
        GameBoardNode *node = [self getGameBoardNodeForGridLocation:[GridLocation gridLocationWithRow:cardSprite.model.cardLocation.row + rowOffset column:cardSprite.model.cardLocation.column]];
        
        if (node != nil) {
            
            [self placeCard:cardSprite inGameBoardNode:node useHighLighting:NO onCompletion:nil];
        }
    }
}

- (void)removeCard:(CardSprite *)card {
    
    [card removeFromParentAndCleanup:YES];
}

- (void)removeCardAtGameBoardNode:(GameBoardNode *)node {
    
    if (node.card != nil) {
        [node.card removeFromParentAndCleanup:YES];
        node.card = nil;
    }
}

- (void)replaceCardAtGameBoardNode:(GameBoardNode *)node withCardInGameBoardNode:(GameBoardNode *)replaceWithNode {
    
    [node.card removeFromParentAndCleanup:YES];
    node.card = replaceWithNode.card;
}

- (void)swapCardFromNode:(GameBoardNode *)fromNode toNode:(GameBoardNode *)toNode {
    
    toNode.card = fromNode.card;
    fromNode.card = nil;
}

- (void)moveCardAtLocation:(GridLocation *)location followingPath:(NSArray *)path onCompletion:(void (^)())completion {

    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
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
            [_delegate card:node.card movedToNode:nextNode];
        }
        
        if (tempPath.count == 0) {
            
            _isMoving = NO;
            completion();
        }
        else {
            [self moveCardAtLocation:location followingPath:[NSArray arrayWithArray:tempPath] onCompletion:completion];//[self moveActiveGameBoardNodeFollowingPath:[NSArray arrayWithArray:tempPath] onCompletion:completion];
        }
    }];
    
    [tempPath removeObject:step];
    
    [node.card runAction:[CCSequence actions:moveAction, popStep, nil]];
}

- (void)moveActiveGameBoardNodeFollowingPath:(NSArray *)path onCompletion:(void (^)())completion {
    
    [self moveCardAtLocation:_activeCard.model.cardLocation followingPath:path onCompletion:completion];
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
        [node.nodeSprite setColor:color];
        
        if (![_highlightedNodes containsObject:node]) {
            [_highlightedNodes addObject:node];
        }
    }
}

- (void)highlightNodesForAttackDirectionAtLocations:(NSArray *)locations {
    
    for (GridLocation *location in locations) {

        GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
        
        if (node != nil) {

            [node highlightForType:kHighlightTypeAttackDirection];
            
            if (![_highlightedNodes containsObject:node]) {
                [_highlightedNodes addObject:node];
            }
        }
    }
}

- (void)highlightSelectedAttackDirectionAtLocation:(GridLocation *)location {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    if (node != nil && node.highlightedAs == kHighlightTypeAttackDirection) {
        
        [node focusType:kHighlightTypeAttackDirection];
    }
}

- (void)deHighlightSelectedAttackDirectionAtLocation:(GridLocation *)location {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    if (node != nil && node.highlightedAs == kHighlightTypeAttackDirection) {
        
        [node unFocusType:kHighlightTypeAttackDirection];
    }
}

- (void)highlightCardAtLocation:(GridLocation *)location withColor:(ccColor3B)color {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    if (node != nil && node.card != nil) {
        [node.card setColor:color];
        
        if (![_highlightedNodes containsObject:node]) {
            [_highlightedNodes addObject:node];
        }
    }
}

- (void)highlightCardAtLocation:(GridLocation *)location withColor:(ccColor3B)color actionType:(ActionTypes)actionType {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    if (node != nil && node.card != nil) {
        
        if (actionType == kActionTypeRanged) {
            
            [node highlightCardForType:kHighlightTypeRangedTarget];
        }
        else if (actionType == kActionTypeMelee) {
            
            [node highlightCardForType:kHighlightTypeMeleeTarget];
        }
        else {
            [node.card setColor:color];
        }
        
        if (![_highlightedNodes containsObject:node]) {
            [_highlightedNodes addObject:node];
        }
    }
}

- (void)deHighlightNodeAtLocation:(GridLocation *)location {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    [self deHighlightNode:node];
}

- (void)deHighlightNode:(GameBoardNode*)node {
    
    [node.nodeSprite setColor:ccc3(255, 255, 255)];

    if (node.card != nil) {
        [node.card setColor:ccc3(255, 255, 255)];
    }
    
    [node deHighlight];
    
    [_highlightedNodes removeObject:node];
}

- (void)deHighlightAllNodes {
    
    NSArray *nodes = [NSArray arrayWithArray:_highlightedNodes];
    
    for (GameBoardNode *node in nodes) {
        
        [self deHighlightNode:node];
    }
}

- (void)selectCardInGameBoardNode:(GameBoardNode *)node useHighlighting:(BOOL)highlight {
    
    [self deselectActiveNode];
        
    [node setZOrder:500];
    [node.card setZOrder:501];
    [node.card setColor:ccc3(0, 0, 235.0)];
    
    if (highlight) {
        [ParticleHelper highlightNode:node.card forever:YES];
    }
    
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
