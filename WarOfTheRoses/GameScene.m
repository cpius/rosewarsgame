//
//  GameScene.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameScene.h"
#import "ParticleHelper.h"
#import "GameManager.h"

@interface GameScene()

- (void)addDeckToScene:(Deck*)deck;

@end

@implementation GameScene

+ (id)scene {
    
    CCScene *scene = [CCScene node];
    
    GameScene *layer = [[GameScene alloc] init];
    
    [scene addChild:layer];
    
    return scene;
}

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        CGSize screenSize = [CCDirector sharedDirector].winSize;

        CCSprite *background = [CCSprite spriteWithFile:@"woddenbackground2.png"];
        background.anchorPoint = ccp(0, 0);
        [self addChild:background z:-1];

        _gameboard = [[GameBoard alloc] initWithPlayerColor:kPlayerGreen];
        
        _gameboard.contentSize = CGSizeMake(320, 480);
        _gameboard.rows = 8;
        _gameboard.columns = 5;
        _gameboard.anchorPoint = ccp(0.5, 0.5);
        _gameboard.colorOfTopPlayer = kPlayerRed;
        _gameboard.colorOfBottomPlayer = kPlayerGreen;
        _gameboard.position = ccp(screenSize.width / 2, (screenSize.height / 2) + 75);
        _gameboard.scale = 0.65;
        
        [self addDeckToScene:[GameManager sharedManager].currentGame.myDeck];
        [self addDeckToScene:[GameManager sharedManager].currentGame.enemyDeck];
        
        [self addChild:_gameboard];
        
        [_gameboard layoutBoard];
        [_gameboard layoutDeck:[GameManager sharedManager].currentGame.myDeck forPlayerWithColor:kPlayerGreen];
        [_gameboard layoutDeck:[GameManager sharedManager].currentGame.enemyDeck forPlayerWithColor:kPlayerRed];

        _originalPos = self.position;
        self.isTouchEnabled = YES;

        [[CCDirector sharedDirector].touchDispatcher addTargetedDelegate:self priority:0 swallowsTouches:YES];
    }
    
    return self;
}

- (void)addDeckToScene:(Deck *)deck {
    
    CGSize screenSize = [CCDirector sharedDirector].winSize;

    for (Card *card in deck.cards) {
        card.position = ccp(screenSize.width / 2, screenSize.height + 50);
        card.scale = 0.4;
        [self addChild:card];
    }
}

- (BOOL)ccTouchBegan:(UITouch *)touch withEvent:(UIEvent *)event {
    
    return NO;
}

- (void)ccTouchesEnded:(NSSet *)touches withEvent:(UIEvent *)event {
    
    UITouch *touch = [touches anyObject];
    
    GameBoardNode *gameboardNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertTouchToNodeSpace:touch]];
    
    if (gameboardNode != nil && gameboardNode.hasCard) {
        
        if (_activeNode) {
            [_activeNode setZOrder:0];
            [ParticleHelper stopHighlightingNode:_activeNode];
            
            NSArray *adjacentGameBoardNodes = [_gameboard getAdjacentGameBoardNodesToCard:_activeNode.card];
            
            for (GameBoardNode *node in adjacentGameBoardNodes) {
                [node runAction:[CCScaleTo actionWithDuration:0.2 scale:1.0]];
            }
            
            [_activeNode.card runAction:[CCTintTo actionWithDuration:0.2 red:255 green:255 blue:255]];
        }
        
        NSArray *adjacentGameBoardNodes = [_gameboard getAdjacentGameBoardNodesToCard:gameboardNode.card];
        
        for (GameBoardNode *node in adjacentGameBoardNodes) {
            
            [node runAction:[CCScaleTo actionWithDuration:0.2 scale:1.1]];
        }
        
        [gameboardNode setZOrder:100];
        [gameboardNode.card runAction:[CCTintTo actionWithDuration:0.2 red:235 green:0 blue:0]];
        [ParticleHelper highlightNode:gameboardNode forever:YES];
       
        _activeNode = gameboardNode;
        
        [self zoomInOnGameBoardNode:gameboardNode];
        _zoomedIn = YES;
    }
    else {
        if (_zoomedIn) {
            [self zoomOut];
            _zoomedIn = NO;
        }
    }
}

- (void)zoomOut {
    
    [self stopAllActions];
    
    [self unscheduleUpdate];
    [self scheduleUpdate];
    
    CGSize winSize = [CCDirector sharedDirector].winSize;
    
    _zoomPosition = ccp(winSize.width / 2, winSize.height / 2);
    _isZooming = YES;
    
    id zoomIn = [CCScaleTo actionWithDuration:0.2f scale:1.0];
    id reset = [CCCallBlock actionWithBlock:^{
        CCLOG(@"zoom out complete");
        
        [self unscheduleUpdate];
        
        _zoomInOnNode = nil;
        _isZooming = NO;
        _zoomPosition = CGPointZero;
    }];
    
    [self runAction:[CCSequence actions:zoomIn, reset, nil]];
}

-(void) zoomInOnGameBoardNode:(GameBoardNode*)node
{
    [self stopAllActions];
    
    [self unscheduleUpdate];
    [self scheduleUpdate];
    
    _zoomPosition = node.card.position;
    _isZooming = YES;
    
    id zoomIn = [CCScaleTo actionWithDuration:0.2f scale:kZoomFactor];
    id reset = [CCCallBlock actionWithBlock:^{
        CCLOG(@"zoom in complete");
        
        [self unscheduleUpdate];
        
        _zoomInOnNode = nil;
        _isZooming = NO;
        _zoomPosition = CGPointZero;
    }];
    
    [self runAction:[CCSequence actions:zoomIn, reset, nil]];
}

-(void) update:(ccTime)delta
{
    if (_isZooming)
    {
        CGSize screenSize = [CCDirector sharedDirector].winSize;
        CGPoint screenCenter = CGPointMake(screenSize.width * 0.5f,
                                           screenSize.height * 0.5f);
        
        CGPoint offsetToCenter = ccpSub(screenCenter, _zoomPosition);
        self.position = ccpMult(offsetToCenter, self.scale);
        self.position = ccpSub(self.position, ccpMult(offsetToCenter,
                                                      (kZoomFactor - self.scale) /
                                                      (kZoomFactor - 1.0f)));
    }
}

@end
