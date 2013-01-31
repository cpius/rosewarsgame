//
//  GameBoard.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/7/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameBoard.h"
#import "ParticleHelper.h"

@interface GameBoard()

@end

@implementation GameBoard

@synthesize playerColor = _playerColor;
@synthesize rows, columns;
@synthesize colorOfTopPlayer, colorOfBottomPlayer;

- (id)initWithPlayerColor:(PlayerColors)playerColor {
    
    self = [super init];
    
    if (self) {
        
        self.contentSize = CGSizeMake(320, 375);

        _playerColor = playerColor;
        
        _greenBackgroundImageName = @"greenbackground.png";
        _redBackgroundImageName = @"redbackground.png";
    }
    
    return self;
}

- (void)layoutDeck:(Deck*)deck forPlayerWithColor:(PlayerColors)color {

    NSUInteger rowOffset = 0;
    
    if (color == kPlayerGreen && colorOfBottomPlayer == kPlayerGreen) {
        rowOffset = 4;
    }
    
    if (color == kPlayerRed && colorOfBottomPlayer == kPlayerRed) {
        rowOffset = 4;
    }
    
    for (Card *card in deck.cards) {
        
        GameBoardNode *node = [self getGameBoardNodeForGridLocation:MakeGridLocation(card.cardLocation.row + rowOffset, card.cardLocation.column)];
        
        if (node != nil) {
            [self placeCard:card inGameBoardNode:node useHighLighting:NO];
        }
    }
}

- (void)moveFromActiveNodeToNode:(GameBoardNode *)node {
    
    if ([self nodeIsActive]) {
        
        if (_activeNode == node) {
            return;
        }
        
        [self placeCard:_activeNode.card inGameBoardNode:node useHighLighting:NO];
    }
}

- (void)placeCard:(Card *)card inGameBoardNode:(GameBoardNode *)node useHighLighting:(BOOL)highlighting {

    CGPoint position = [self convertToWorldSpace:node.position];
    
    card.cardLocation = node.locationInGrid;
    [card setZOrder:5];
 
    CCMoveTo *moveAction = [CCMoveTo actionWithDuration:0.2 position:position];
    [card runAction:moveAction];
    
    CCScaleTo *scaleDownAction = [CCScaleTo actionWithDuration:0.2 scale:1.0];
    [node runAction:scaleDownAction];
   
    node.card = card;
    
    if (highlighting) {
        CCParticleSystem *particle = [CCParticleSystemQuad particleWithFile:@"exploding_ring.plist"];
        particle.position = ccp(node.contentSize.width / 2, node.contentSize.height / 2);
        particle.scale = 0.5;
        [node addChild:particle z:10];
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
            
            
            node.locationInGrid = MakeGridLocation(row + 1, column + 1);
            CCLabelTTF *label = [CCLabelTTF labelWithString:[NSString stringWithFormat:@"%d,%d", node.locationInGrid.row, node.locationInGrid.column] fontName:@"AppleGothic" fontSize:10];
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

- (GameBoardNode *)getGameBoardNodeForGridLocation:(GridLocation)gridLocation {
    
    for (GameBoardNode *node in _boardNodes) {
        
        if (node.locationInGrid.row == gridLocation.row &&
            node.locationInGrid.column == gridLocation.column) {
            return node;
        }
    }
    
    return nil;
}

- (void)deselectActiveNode {
    
    if (_activeNode) {
        [_activeNode setZOrder:0];
        [ParticleHelper stopHighlightingNode:_activeNode];
        
        NSArray *adjacentGameBoardNodes = [self getAdjacentGameBoardNodesToCard:_activeNode.card];
        
        for (GameBoardNode *node in adjacentGameBoardNodes) {
            [node runAction:[CCScaleTo actionWithDuration:0.2 scale:1.0]];
        }
        
        CCCallBlock *reset = [CCCallBlock actionWithBlock:^{
            _activeNode = nil;
        }];
        
        [_activeNode.card runAction:[CCSequence actions:[CCTintTo actionWithDuration:0.2 red:255 green:255 blue:255], reset, nil]];
    }
}

- (BOOL)nodeIsActive {
    
    return _activeNode != nil;
}

- (void)selectGameBoardNode:(GameBoardNode *)node useHighlighting:(BOOL)highlight {
    
    [self deselectActiveNode];
    
    NSArray *adjacentGameBoardNodes = [self getAdjacentGameBoardNodesToCard:node.card];
    
    for (GameBoardNode *node in adjacentGameBoardNodes) {
        
        [node runAction:[CCScaleTo actionWithDuration:0.2 scale:1.1]];
    }
    
    [node setZOrder:100];
    [node.card runAction:[CCTintTo actionWithDuration:0.2 red:235 green:0 blue:0]];
    [ParticleHelper highlightNode:node forever:YES];
    
    _activeNode = node;
}

- (NSArray*)getAdjacentGameBoardNodesToCard:(Card*)card {
    
    NSMutableArray *adjacentGameBoards = [NSMutableArray array];
    
    // Card to the left?
    if (card.cardLocation.column > 1) {
        GameBoardNode *node = [self getGameBoardNodeForGridLocation:MakeGridLocation(card.cardLocation.row, card.cardLocation.column - 1)];
        
        if (!node.hasCard) {
            [adjacentGameBoards addObject:node];
        }
    }
    
    // Card to the right?
    if (card.cardLocation.column < self.columns) {
        GameBoardNode *node = [self getGameBoardNodeForGridLocation:MakeGridLocation(card.cardLocation.row, card.cardLocation.column + 1)];
        
        if (!node.hasCard) {
            [adjacentGameBoards addObject:node];
        }
    }
    
    // Card above?
    if (card.cardLocation.row > 1) {
        GameBoardNode *node = [self getGameBoardNodeForGridLocation:MakeGridLocation(card.cardLocation.row - 1, card.cardLocation.column)];
        
        if (!node.hasCard) {
            [adjacentGameBoards addObject:node];
        }
    }
    
    // Card below?
    if (card.cardLocation.row < self.rows) {
        GameBoardNode *node = [self getGameBoardNodeForGridLocation:MakeGridLocation(card.cardLocation.row + 1, card.cardLocation.column)];
        
        if (!node.hasCard) {
            [adjacentGameBoards addObject:node];
        }
    }
    
    return [NSArray arrayWithArray:adjacentGameBoards];
}

@end
