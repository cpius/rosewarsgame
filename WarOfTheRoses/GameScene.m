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
#import "MainMenuScene.h"
#import "BattlePlan.h"

@interface GameScene()

- (void)addDeckToScene:(Deck*)deck;

- (void)showToolsPanel;
- (void)hideToolsPanel;
- (void)resetUserInterface;

- (void)checkForEndTurn;
- (void)doEnemyPlayerTurn;

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
        _gameManager.delegate = self;

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
        
        _backButton = [CCSprite spriteWithFile:@"backbutton.png"];
        _backButton.position = ccp(10, _winSize.height - _backButton.contentSize.height - 10);
        _backButton.anchorPoint = ccp(0, 0);
        [self addChild:_backButton];
                
        [self addChild:_gameboard];
        
        _myCards = [[NSMutableArray alloc] initWithCapacity:_gameManager.currentGame.myDeck.cards.count];
        _enemyCards = [[NSMutableArray alloc] initWithCapacity:_gameManager.currentGame.enemyDeck.cards.count];
       
        [self addDeckToScene:[GameManager sharedManager].currentGame.myDeck];
        [self addDeckToScene:[GameManager sharedManager].currentGame.enemyDeck];

        [_gameboard layoutBoard];
        [_gameboard layoutDeck:_myCards forPlayerWithColor:_gameManager.currentGame.myColor];
        [_gameboard layoutDeck:_enemyCards forPlayerWithColor:_gameManager.currentGame.enemyColor];
        
        [self populateUnitLayout];

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

- (void)populateUnitLayout {
    
    Game *currentGame = [GameManager sharedManager].currentGame;
    
    for (Card *card in currentGame.myDeck.cards) {
        [currentGame.unitLayout setObject:card forKey:card.cardLocation];
    }
    
    for (Card *card in currentGame.enemyDeck.cards) {
        [currentGame.unitLayout setObject:card forKey:card.cardLocation];
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
    
    if (CGRectContainsPoint(_backButton.boundingBox, [self convertTouchToNodeSpace:touch])) {
        
        [[CCDirector sharedDirector] replaceScene:[MainMenuScene scene]];
        return;
    }
    
    GameBoardNode *targetNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertTouchToNodeSpace:touch]];
    
    if (targetNode != nil) {
        
        if ([_gameboard nodeIsActive]) {
            
            Action *action = [_gameboard getActionsToGameBoardNode:targetNode allLocations:_gameManager.currentGame.unitLayout];
            
            if (action == nil || ![action isWithinRange]) {
                
                [self resetUserInterface];
                return;
            }
            
            // TODO: Isolate in actions
            
            if ([action isKindOfClass:[MeleeAttackAction class]]) {
                
                [_gameboard moveActiveGameBoardNodeFollowingPath:action.path onCompletion:^{
                    
                    CombatOutcome outcome = [self engageCombatBetweenMyCard:[_gameboard activeNode].card.model andEnemyCard:targetNode.card.model];
                    
                    if (outcome == kCombatOutcomeDefendSuccessful) {
                        
                        PathFinderStep *retreatToLocation = [action.path objectAtIndex:action.path.count - 2];
                        
                        [_gameboard moveActiveGameBoardNodeFollowingPath:[NSArray arrayWithObject:retreatToLocation] onCompletion:^{
                            
                            if (![[_gameboard activeNode].locationInGrid isEqual:retreatToLocation.location]) {
                                [_gameManager card:[_gameboard activeNode].card.model movedToGridLocation:retreatToLocation.location];
                                [_gameboard swapCardFromNode:[_gameboard activeNode] toNode:[_gameboard getGameBoardNodeForGridLocation:retreatToLocation.location]];
                            }
                            
                            [_gameboard deselectActiveNode];
                            [_gameboard deHighlightAllNodes];
                        }];
                    }
                    else {
                        [ParticleHelper applyBurstToNode:targetNode];
                        
                        [_gameManager cardHasBeenDefeated:targetNode.card.model];
                        [_gameboard replaceCardAtGameBoardNode:targetNode withCard:[_gameboard activeNode].card];
                        [self resetUserInterface];
                    }
                    
                    NSUInteger remainingActions = [_gameManager actionUsed:action];
                    [self updateRemainingActions:remainingActions];
                    [self checkForEndTurn];
                }];
            }
            
            else if ([action isKindOfClass:[RangedAttackAction class]]) {
                CombatOutcome outcome = [self engageCombatBetweenMyCard:action.cardInAction andEnemyCard:action.enemyCard];
                
                if (outcome == kCombatOutcomeDefendSuccessful) {
                    [self resetUserInterface];
                }
                else {
                    [ParticleHelper applyBurstToNode:targetNode];
                    
                    [_gameManager cardHasBeenDefeated:action.enemyCard];
                    [_gameboard removeCardAtGameBoardNode:targetNode];
                    [self resetUserInterface];
                }
                
                NSUInteger remainingActions = [_gameManager actionUsed:action];
                [self updateRemainingActions:remainingActions];
                [self checkForEndTurn];
            }
            
            else if ([action isKindOfClass:[MoveAction class]]){
                [_gameboard moveActiveGameBoardNodeFollowingPath:action.path onCompletion:^{
                    
                    if (![[_gameboard activeNode].locationInGrid isEqual:targetNode.locationInGrid]) {
                        [_gameManager card:[_gameboard activeNode].card.model movedToGridLocation:targetNode.locationInGrid];
                        [_gameboard swapCardFromNode:[_gameboard activeNode] toNode:targetNode];
                    }

                    [_gameboard deselectActiveNode];
                    [_gameboard deHighlightAllNodes];

                    NSUInteger remainingActions = [_gameManager actionUsed:action];
                    [self updateRemainingActions:remainingActions];
                    [self hideToolsPanel];
                    [self checkForEndTurn];
                }];
            }

        }
        else {
            if (targetNode.hasCard && [targetNode.card.model isOwnedByPlayerWithColor:_gameManager.currentGame.myColor]) {
                [_gameboard selectCardInGameBoardNode:targetNode useHighlighting:YES];
                
                BattlePlan *battlePlan = [[BattlePlan alloc] init];
                [battlePlan createBattlePlanForCard:targetNode.card.model enemyUnits:_gameManager.currentGame.enemyDeck.cards unitLayout:_gameManager.currentGame.unitLayout];
                
                for (Action *moveAction in battlePlan.moveActions) {
                    [_gameboard highlightNodeAtLocation:[moveAction getLastLocationInPath] withColor:ccc3(0, 235, 0)];
                }

                for (Action *meleeAction in battlePlan.meleeActions) {
                    [_gameboard highlightCardAtLocation:[meleeAction getLastLocationInPath] withColor:ccc3(235, 0, 0)];
                }
                
                for (Action *rangeAction in battlePlan.rangeActions) {
                    [_gameboard highlightCardAtLocation:[rangeAction getLastLocationInPath] withColor:ccc3(235, 0, 0)];
                }
                
                [self showToolsPanel];
            }
        }
    }
}

- (void)turnChangedToPlayerWithColor:(PlayerColors)player {
    
    [self updateRemainingActions:_gameManager.currentGame.numberOfAvailableActions];

    if (player == _gameManager.currentGame.enemyColor) {
        
        [self performSelector:@selector(doEnemyPlayerTurn) withObject:nil afterDelay:1.0];
    }
}

- (void)doEnemyPlayerTurn {
    
    __block NSUInteger remainingActions = _gameManager.currentGame.numberOfAvailableActions;
    
    if (remainingActions == 0) {
        [self checkForEndTurn];
        return;
    }
    
    Action *nextAction = [_gameManager getActionForEnemeyPlayer];
        
    GridLocation *fromLocation = nextAction.cardInAction.cardLocation;
    GridLocation *toLocation = [[nextAction.path lastObject] location];
    
    GameBoardNode *fromNode = [_gameboard getGameBoardNodeForGridLocation:fromLocation];
    GameBoardNode *toNode = [_gameboard getGameBoardNodeForGridLocation:toLocation];
    
    CCLOG(@"Enemy unit moving from node: %@ to node: %@", fromNode, toNode);
    
    [_gameboard selectCardInGameBoardNode:fromNode useHighlighting:YES];
    
    [_gameboard moveActiveGameBoardNodeFollowingPath:nextAction.path onCompletion:^{
        
        [_gameManager card:nextAction.cardInAction movedToGridLocation:toLocation];
        [_gameboard swapCardFromNode:fromNode toNode:toNode];
        
        [_gameboard deselectActiveNode];
        [_gameboard deHighlightAllNodes];
        
        remainingActions = [_gameManager actionUsed:nextAction];
        [self updateRemainingActions:remainingActions];
        
        [self performSelector:@selector(doEnemyPlayerTurn) withObject:nil afterDelay:1.0];
    }];
}

- (void)resetUserInterface {
    
    [_gameboard deselectActiveNode];
    [_gameboard deHighlightAllNodes];
    [self hideToolsPanel];
}

- (void)card:(CardSprite *)card movedToNode:(GameBoardNode *)node {
    
    card.model.movesConsumed++;
}

- (void)combatHasStartedBetweenAttacker:(Card *)attacker andDefender:(Card *)defender {
    
    [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventAttack];
}

- (void)checkForEndTurn {
    
    GameResults result = [_gameManager checkForEndGame];
    
    if (result == kGameResultInProgress) {
        if (_gameManager.currentGame.numberOfAvailableActions == 0) {
            
            /*        EndTurnLayer *endTurnLayer = [EndTurnLayer getEndTurnLayerWithSize:_winSize];
             endTurnLayer.position = self.position;
             [self addChild:endTurnLayer z:1000];
             */
            [_gameManager endTurn];
        }
    }
    else {
        [[CCDirector sharedDirector] replaceScene:[MainMenuScene scene]];
        return;
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
