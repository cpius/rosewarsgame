//
//  GameBoard.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/7/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameBoard.h"
//#import "ParticleHelper.h"
#import "RangedAttackAction.h"
#import "PathFinderStrategyFactory.h"

static NSString* const kConquerNodeName = @"conquer_smoke";

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
        
        self.size = CGSizeMake(320, 375);
        
        _greenBackgroundImageName = @"greenbackground.png";
        _redBackgroundImageName = @"redbackground.png";
        
        _highlightedNodes = [NSMutableArray array];
        _highlightedCards = [NSMutableArray array];
    }
    
    return self;
}

- (void)layoutDeck:(NSMutableArray*)deck withCardScale:(float)cardScale forPlayerWithColor:(PlayerColors)color {

    NSUInteger rowOffset = 0;
    
    for (CardSprite *cardSprite in deck) {
        
        GameBoardNode *node = [self getGameBoardNodeForGridLocation:[GridLocation gridLocationWithRow:cardSprite.model.cardLocation.row + rowOffset column:cardSprite.model.cardLocation.column]];
        
        if (node != nil) {
            [cardSprite setScale:cardScale];
            
            [self placeCard:cardSprite withCardScale:cardScale inGameBoardNode:node useHighLighting:NO onCompletion:nil];
        }
    }
}

- (void)removeCard:(CardSprite *)card {
    
    [card removeFromParent];
}

- (void)removeCardAtGameBoardNode:(GameBoardNode *)node {
    
    if (node.card != nil) {
        [node.card removeFromParent];
        node.card = nil;
    }
}

- (void)replaceCardAtGameBoardNode:(GameBoardNode *)node withCardInGameBoardNode:(GameBoardNode *)replaceWithNode {
    
    [node.card removeFromParent];
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
    
    node.card.zPosition = kAttackingCardSpriteZOrder;
    CGPoint position = [self convertPoint:nextNode.position toNode:self.parent];
    SKAction *moveAction = [SKAction moveTo:position duration:0.2];
    SKAction *popStep = [SKAction runBlock:^{
        if ([_delegate respondsToSelector:@selector(card:movedToNode:)]) {
            [_delegate card:node.card movedToNode:nextNode];
        }
        
        if (tempPath.count == 0) {
            
            _isMoving = NO;
            node.card.zPosition = kCardSpriteZOrder;
            completion();
        }
        else {
            [self moveCardAtLocation:location followingPath:[NSArray arrayWithArray:tempPath] onCompletion:completion];
        }
    }];
    
    [tempPath removeObject:step];
    
    [node.card runAction:[SKAction sequence:@[moveAction, popStep]]];
}

- (void)moveActiveGameBoardNodeFollowingPath:(NSArray *)path onCompletion:(void (^)())completion {
    
    [self moveCardAtLocation:_activeCard.model.cardLocation followingPath:path onCompletion:completion];
}

- (void)placeCard:(CardSprite *)cardSprite withCardScale:(float)cardScale inGameBoardNode:(GameBoardNode *)node useHighLighting:(BOOL)highlighting onCompletion:(void (^)())completion {

    CGPoint position = [self convertPoint:node.position toNode:self.parent];
    
    cardSprite.model.cardLocation = node.locationInGrid;
    [cardSprite setZPosition:kCardSpriteZOrder];
 
    SKAction *moveAction = [SKAction moveTo:position duration:0.2];
    SKAction *scaleAction = [SKAction scaleTo:cardScale duration:0.2];
    [cardSprite runAction:[SKAction group:@[moveAction, scaleAction]]];

    SKAction *scaleDownAction = [SKAction scaleTo:1.0 duration:0.2];
    SKAction *complete = [SKAction runBlock:^{
        if (completion != nil) {
            completion();
        }
    }];
    
    [node runAction:[SKAction sequence:@[scaleDownAction, complete]]];
   
    node.card = cardSprite;
    
    if (highlighting) {
//        [ParticleHelper applyBurstToNode:node];
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
            
            GameBoardNode *node = [[GameBoardNode alloc] initWithSprite:spriteName];
            
            node.locationInGrid = [GridLocation gridLocationWithRow:row + 1 column:column + 1];
            node.position = CGPointMake((column * node.size.width) + node.size.width / 2, self.size.height - ((row * node.size.height) +node.size.height / 2));
            [self addChild:node];
            [_boardNodes addObject:node];
        }
    }
}

- (GameBoardNode*)getGameBoardNodeForPosition:(CGPoint)position {

    for (GameBoardNode *node in self.children) {
        
        if (CGRectContainsPoint(node.frame, position)) {
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

- (void)highlightNodeAtLocation:(GridLocation*)location withColor:(SKColor*)color {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    if (node != nil) {
        [node setColor:[SKColor greenColor]];
        node.colorBlendFactor = 0.5;
        
        if (![_highlightedNodes containsObject:node]) {
            [_highlightedNodes addObject:node];
        }
    }
}

- (BOOL)isNodeHighlightedForConquer {
    
    return [self nodeHighlightedForConquer] != nil;
}

- (GameBoardNode*)nodeHighlightedForConquer {
    
    __block GameBoardNode *conquerNode = nil;
    [_boardNodes enumerateObjectsUsingBlock:^(id obj, NSUInteger idx, BOOL *stop) {
        GameBoardNode *node = obj;
        [node.children enumerateObjectsUsingBlock:^(id obj, NSUInteger idx, BOOL *stop) {
            SKNode *child = obj;
            if ([child.name isEqualToString:kConquerNodeName]) {
                conquerNode = node;
                *stop = YES;
            }
        }];
    }];
    
    return conquerNode;
}

- (void)highlightNodeAtLocation:(GridLocation*)location forConquer:(BOOL)canConquer {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    if (node != nil) {
        if (canConquer) {
            [node setColor:[SKColor greenColor]];
            node.colorBlendFactor = 0.5;
            
            NSString *smokeEmitterPath = [[NSBundle mainBundle] pathForResource:@"ConquerSmoke" ofType:@"sks"];
            SKEmitterNode *smokeEmitter = [NSKeyedUnarchiver unarchiveObjectWithFile:smokeEmitterPath];
            smokeEmitter.name = kConquerNodeName;
            [smokeEmitter setScale:0.5];
            
            [node addChild:smokeEmitter];
        }
        else {
            [self deHighlightNode:node];
            [[node childNodeWithName:kConquerNodeName] removeFromParent];
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

- (void)highlightCardAtLocation:(GridLocation *)location withColor:(SKColor*)color {
    
    GameBoardNode *node = [self getGameBoardNodeForGridLocation:location];
    
    if (node != nil && node.card != nil) {
        [node.card setColor:color];
        
        if (![_highlightedNodes containsObject:node]) {
            [_highlightedNodes addObject:node];
        }
    }
}

- (void)highlightCardAtLocation:(GridLocation *)location withColor:(SKColor*)color actionType:(ActionTypes)actionType {
    
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
    
    [node setColor:[SKColor colorWithRed:1.0 green:1.0 blue:1.0 alpha:1.0]];

    if (node.card != nil) {
        [node.card setColor:[SKColor colorWithRed:1.0 green:1.0 blue:1.0 alpha:1.0]];
    }
    
    [node deHighlight];
    
    [_highlightedNodes removeObject:node];
}

- (void)deHighlightAllNodes {
    
    NSArray *nodes = [NSArray arrayWithArray:_boardNodes];
    
    for (GameBoardNode *node in nodes) {
        
        [self deHighlightNode:node];
    }
}

- (void)selectCardInGameBoardNode:(GameBoardNode *)node useHighlighting:(BOOL)highlight {
    
    [self deselectActiveNode];
        
    [node setZPosition:kGameBoardnodeZOrder];
    [node.card setZPosition:kCardSpriteZOrder];
    [node.card setColor:[SKColor colorWithRed:0.0 green:0.0 blue:1 / 235.0 alpha:1.0]];
    
    if (highlight) {
//        [ParticleHelper highlightNode:node.card forever:YES];
    }
    
    _activeNode = node;
    _activeCard = node.card;
}

- (void)deselectActiveNode {
    
    if ([self nodeIsActive]) {
        [_activeNode setZPosition:kGameBoardnodeZOrder];
        [_activeNode.card setZPosition:kCardSpriteZOrder];
        //[ParticleHelper stopHighlightingNode:_activeCard];
        
        [_activeCard setColor:[SKColor colorWithRed:1.0 green:1.0 blue:1.0 alpha:1.0]];
        
        _activeCard = nil;
        _activeNode = nil;
    }
}

@end
