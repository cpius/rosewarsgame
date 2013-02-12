//
//  GameScene.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameScene.h"
#import "ParticleHelper.h"
#import "Card.h"
#import "Magnifier.h"
#import "EndTurnLayer.h"

@interface GameScene()

- (void)addDeckToScene:(Deck*)deck;

- (void)showToolsPanel;
- (void)hideToolsPanel;

- (void)checkForEndTurn;

- (void)updateRemainingActions:(NSUInteger)remainingActions;

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
        
        _winSize = [CCDirector sharedDirector].winSize;

        _gameManager = [GameManager sharedManager];

        CCSprite *background = [CCSprite spriteWithFile:@"woddenbackground2.png"];
        background.anchorPoint = ccp(0, 0);
        [self addChild:background z:-1];

        _gameboard = [[GameBoard alloc] init];
        
        _gameboard.contentSize = CGSizeMake(320, 480);
        _gameboard.rows = 8;
        _gameboard.columns = 5;
        _gameboard.anchorPoint = ccp(0.5, 0.5);
        _gameboard.colorOfTopPlayer = _gameManager.currentGame.enemyColor;
        _gameboard.colorOfBottomPlayer = _gameManager.currentGame.myColor;
        _gameboard.position = ccp(_winSize.width / 2, (_winSize.height / 2) + 75);
        _gameboard.scale = 0.65;
        _gameboard.delegate = self;
        
        _leftPanel = [CCSprite spriteWithFile:@"leftpanel.png"];
        _leftPanel.position = ccp(-_leftPanel.contentSize.width, _winSize.height / 2);
        [self addChild:_leftPanel];
        
        _actionCountLabel = [CCLabelTTF labelWithString:[NSString stringWithFormat:@"%d", _gameManager.currentGame.numberOfAvailableActions] fontName:APP_FONT fontSize:32];
        _actionCountLabel.position = ccp(_winSize.width - 50, _winSize.height - 50);
        _actionCountLabel.anchorPoint = ccp(0, 0);
        [self addChild:_actionCountLabel];
                
        [self addChild:_gameboard];
        
        _myCards = [[NSMutableArray alloc] initWithCapacity:_gameManager.currentGame.myDeck.cards.count];
        _enemyCards = [[NSMutableArray alloc] initWithCapacity:_gameManager.currentGame.enemyDeck.cards.count];
       
        [self addDeckToScene:[GameManager sharedManager].currentGame.myDeck];
        [self addDeckToScene:[GameManager sharedManager].currentGame.enemyDeck];

        [_gameboard layoutBoard];
        [_gameboard layoutDeck:_myCards forPlayerWithColor:_gameManager.currentGame.myColor];
        [_gameboard layoutDeck:_enemyCards forPlayerWithColor:_gameManager.currentGame.enemyColor];

        _originalPos = self.position;
        self.isTouchEnabled = YES;

        [[CCDirector sharedDirector].touchDispatcher addTargetedDelegate:self priority:0 swallowsTouches:YES];
    }
    
    return self;
}

- (void)addDeckToScene:(Deck *)deck {
    
    CGSize screenSize = [CCDirector sharedDirector].winSize;

    for (Card *card in deck.cards) {
        
        CardSprite *cardSprite = [[CardSprite alloc] initWithCard:card];
        
        cardSprite.position = ccp(screenSize.width / 2, screenSize.height + 50);
        cardSprite.scale = 0.40;
        
        [self addChild:cardSprite];
        
        if ([card isOwnedByPlayerWithColor:_gameManager.currentGame.myColor]) {
            [_myCards addObject:cardSprite];
        }
        else {
            [_enemyCards addObject:cardSprite];
        }
    }
}

- (BOOL)ccTouchBegan:(UITouch *)touch withEvent:(UIEvent *)event {
    
    return NO;
}

- (void)ccTouchesEnded:(NSSet *)touches withEvent:(UIEvent *)event {
    
    if (_gameboard.isMoving) {
        return;
    }
    
    UITouch *touch = [touches anyObject];
    
    GameBoardNode *targetNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertTouchToNodeSpace:touch]];
    
    if (targetNode != nil) {
        
        if ([_gameboard nodeIsActive]) {
            
            NSArray *movePath = [_gameboard getMovePathToGameBoardNode:targetNode];
            
            // -1 because of current node is included
            if (movePath.count - 1 > [_gameboard activeNode].card.model.move) {
                return;
            }
            
            if (targetNode.hasCard && [targetNode.card.model isOwnedByPlayerWithColor:_gameManager.currentGame.enemyColor]) {
                
                [_gameboard moveActiveGameBoardNodeFollowingPath:movePath onCompletion:^{
                    
                    CombatOutcome outcome = [self engageCombatBetweenMyCard:[_gameboard activeNode].card.model andEnemyCard:targetNode.card.model];
                    
                    if (outcome == kCombatOutcomeDefendSuccessful) {
                        [_gameboard moveActiveGameBoardNodeFollowingPath:[NSArray arrayWithObject:[movePath objectAtIndex:movePath.count - 2]] onCompletion:^{
                            [_gameboard deselectActiveNode];
                        }];
                    }
                    else {
                        [ParticleHelper applyBurstToNode:targetNode];
                        
                        [targetNode.card removeFromParentAndCleanup:YES];
                        targetNode.card = [_gameboard activeNode].card;
                        
                        [_gameboard deselectActiveNode];
                    }
                    
                    NSUInteger remainingActions = [_gameManager actionUsed];
                    [self updateRemainingActions:remainingActions];
                    [self hideToolsPanel];
                //    [self checkForEndTurn];
                }];
            }
            else if (!targetNode.hasCard){
                [_gameboard moveActiveGameBoardNodeFollowingPath:movePath onCompletion:^{
                    
                    [_gameboard deselectActiveNode];
                    [_gameboard swapCardFromNode:[_gameboard activeNode] toNode:targetNode];
                    
                    NSUInteger remainingActions = [_gameManager actionUsed];
                    [self updateRemainingActions:remainingActions];
                    [self hideToolsPanel];
                 //   [self checkForEndTurn];
                }];
            }

        }
        else {
            if (targetNode.hasCard && [targetNode.card.model isOwnedByPlayerWithColor:_gameManager.currentGame.myColor]) {
                [_gameboard selectGameBoardNode:targetNode useHighlighting:YES];
                [self showToolsPanel];
            }
        }
    }
}

- (void)card:(CardSprite *)card movedToNode:(GameBoardNode *)node {
    
    if ([node.card.model isOwnedByPlayerWithColor:_gameManager.currentGame.enemyColor]) {
        [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventAttack];
    }
}

- (void)checkForEndTurn {
    
    if (_gameManager.currentGame.numberOfAvailableActions == 0) {
        
        EndTurnLayer *endTurnLayer = [EndTurnLayer getEndTurnLayerWithSize:_winSize];
        endTurnLayer.position = self.position;
        [self addChild:endTurnLayer z:1000];
        
        [_gameManager endTurn];
    }
}

- (void)updateRemainingActions:(NSUInteger)remainingActions {
    
    _actionCountLabel.string = [NSString stringWithFormat:@"%d", remainingActions];
}

- (CombatOutcome)engageCombatBetweenMyCard:(Card *)myCard andEnemyCard:(Card *)enemyCard {
    
    CombatOutcome combatOutcome = [[GameManager sharedManager] resolveCombatBetween:myCard defender:enemyCard];
        
    return combatOutcome;
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
        
        [_leftPanel runAction:[CCMoveTo actionWithDuration:0.5 position:ccp(0, _winSize.height / 2)]];
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

- (void)showToolsPanel {
    
    [_leftPanel runAction:[CCMoveTo actionWithDuration:0.5 position:ccp((_leftPanel.contentSize.width / 2) - 5, _winSize.height / 2)]];
}

- (void)hideToolsPanel {
    
    [_leftPanel runAction:[CCMoveTo actionWithDuration:0.5 position:ccp(-_leftPanel.contentSize.width, _winSize.height / 2)]];
}

@end
