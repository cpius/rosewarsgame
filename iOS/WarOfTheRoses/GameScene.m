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

- (void)performMeleeAction:(Action*)action targetNode:(GameBoardNode*)targetNode onCompletion:(void (^)())completion;
- (void)performRangedAction:(Action*)action targetNode:(GameBoardNode*)targetNode onCompletion:(void (^)())completion;

- (void)updateRemainingActions:(NSUInteger)remainingActions;

- (void)showCardDetail;
- (void)hideCardDetail;

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
        
        _leftPanel = [[LeftPanel alloc] init];
        _leftPanel.delegate = self;
        _leftPanel.position = ccp(-_leftPanel.contentSize.width, _winSize.height / 2);
        [self addChild:_leftPanel];
        
        _actionCountLabel = [CCLabelTTF labelWithString:[NSString stringWithFormat:@"%d", _gameManager.currentGame.numberOfAvailableActions] fontName:APP_FONT fontSize:32];
        _actionCountLabel.position = ccp(_winSize.width - 40, _winSize.height - 50);
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
        
        _battlePlan = [[BattlePlan alloc] init];
        
        [[CCDirector sharedDirector].touchDispatcher addTargetedDelegate:self priority:0 swallowsTouches:YES];
        
        [self turnChangedToPlayerWithColor:_gameManager.currentPlayersTurn];
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
    
    if (_gameManager.currentPlayersTurn != _gameManager.currentGame.myColor) {
        return;
    }
    
    if (_gameboard.isMoving) {
        return;
    }
    
    if (_gameover) {
        return;
    }
        
    UITouch *touch = [touches anyObject];
    
    if (CGRectContainsPoint(_backButton.boundingBox, [self convertTouchToNodeSpace:touch])) {
        
        [[CCDirector sharedDirector] replaceScene:[MainMenuScene scene]];
        return;
    }
    
    if (_showingDetailOfNode != nil) {
        return;
    }
    
    GameBoardNode *targetNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertTouchToNodeSpace:touch]];
    
    if (targetNode != nil) {
        
        if ([_gameboard nodeIsActive]) {
            
            Action *action = [_gameboard getActionsToGameBoardNode:targetNode allLocations:_gameManager.currentGame.unitLayout];
            
            if (action == nil || ![action isWithinRange]) {
                
                [self resetUserInterface];
                _actionInQueue = nil;
                return;
            }
            
            if (_actionInQueue != nil) {
                return;
            }
            
            action.delegate = self;
            
            // TODO: Isolate in actions
            if ([action isKindOfClass:[MeleeAttackAction class]]) {
                [_gameboard highlightCardAtLocation:action.enemyCard.cardLocation withColor:ccc3(235, 0, 0) actionType:kActionTypeMelee];
                
                if (_battlePlan.meleeActions.count > 0) {
                    _leftPanel.selectedCard = action.cardInAction;
                }

                _actionInQueue = action;
            }
            
            else if ([action isKindOfClass:[RangedAttackAction class]]) {
                [self performRangedAction:action targetNode:targetNode onCompletion:^{
                    [action.cardInAction performedAction:action];
                }];
            }
            
            else if ([action isKindOfClass:[MoveAction class]]){
                [action performActionWithCompletion:^{
                    [action.cardInAction performedAction:action];
                }];
            }

        }
        else {
            if (targetNode.hasCard && [targetNode.card.model isOwnedByPlayerWithColor:_gameManager.currentGame.myColor]) {
                [_gameboard selectCardInGameBoardNode:targetNode useHighlighting:NO];

                _battlePlan = [[BattlePlan alloc] init];
                [_battlePlan createBattlePlanForCard:targetNode.card.model enemyUnits:_gameManager.currentGame.enemyDeck.cards unitLayout:_gameManager.currentGame.unitLayout];
                
                for (Action *moveAction in _battlePlan.moveActions) {
                    [_gameboard highlightNodeAtLocation:[moveAction getLastLocationInPath] withColor:ccc3(0, 235, 0)];
                }

                for (Action *meleeAction in _battlePlan.meleeActions) {
                    [_gameboard highlightCardAtLocation:[meleeAction getLastLocationInPath] withColor:ccc3(235, 0, 0) actionType:kActionTypeMove];
                }

                for (Action *rangeAction in _battlePlan.rangeActions) {
                    [_gameboard highlightCardAtLocation:[rangeAction getLastLocationInPath] withColor:ccc3(235, 0, 0) actionType:kActionTypeRanged];
                }
                
                [self showToolsPanel];
            }
        }
    }
}

- (void)action:(Action *)action wantsToMoveCard:(Card *)card fromLocation:(GridLocation *)fromLocation toLocation:(GridLocation *)toLocation {
    
    [_gameboard swapCardFromNode:[_gameboard getGameBoardNodeForGridLocation:fromLocation]
                          toNode:[_gameboard getGameBoardNodeForGridLocation:toLocation]];
}

- (void)action:(Action *)action wantsToMoveFollowingPath:(NSArray *)path withCompletion:(void (^)(GridLocation *))completion {
    
    [_gameboard moveActiveGameBoardNodeFollowingPath:path onCompletion:^{
        
        PathFinderStep *lastStep = path.lastObject;
        
        completion(lastStep.location);
    }];
}

- (void)beforePerformAction:(Action *)action {
    
}

- (void)afterPerformAction:(Action *)action {
    
    _actionInQueue = nil;
    
    NSUInteger remainingActions = [_gameManager actionUsed:action];
    [self updateRemainingActions:remainingActions];
    [self resetUserInterface];
    [self checkForEndTurn];
}

- (void)performMeleeAction:(Action *)action targetNode:(GameBoardNode *)targetNode onCompletion:(void (^)())completion {
    
    MeleeAttackAction *meleeAction = (MeleeAttackAction*)action;
    
    GridLocation *retreatLocation = action.cardInAction.cardLocation;

    if (action.path.count > 1) {
        retreatLocation = [[action.path objectAtIndex:action.path.count - 2] location];
    }
    
    [_gameboard moveActiveGameBoardNodeFollowingPath:action.path onCompletion:^{
        
        CombatOutcome outcome = [[GameManager sharedManager] resolveCombatBetween:action.cardInAction defender:action.enemyCard];
        
        if (outcome == kCombatOutcomeDefendSuccessful) {
            
            PathFinderStep *retreatToLocation = [[PathFinderStep alloc] initWithLocation:retreatLocation];
            
            [_gameboard moveActiveGameBoardNodeFollowingPath:[NSArray arrayWithObject:retreatToLocation] onCompletion:^{
                
                if (![[_gameboard activeNode].locationInGrid isEqual:retreatToLocation.location]) {
                    [_gameManager card:[_gameboard activeNode].card.model movedToGridLocation:retreatToLocation.location];
                    [_gameboard swapCardFromNode:[_gameboard activeNode] toNode:[_gameboard getGameBoardNodeForGridLocation:retreatToLocation.location]];
                }
                
                NSUInteger remainingActions = [_gameManager actionUsed:action];
                [self updateRemainingActions:remainingActions];
                [self resetUserInterface];
                [self checkForEndTurn];
                
                if (completion != nil) {
                    completion();
                }
            }];
        }
        else {
            [ParticleHelper applyBurstToNode:targetNode];
                        
            if (meleeAction.meleeAttackType == kMeleeAttackTypeNormal) {
                [_gameboard moveActiveGameBoardNodeFollowingPath:[NSArray arrayWithObject:[[PathFinderStep alloc] initWithLocation:retreatLocation]] onCompletion:^{
                    
                    [_gameManager cardHasBeenDefeated:targetNode.card.model];
                    [_gameManager card:action.cardInAction movedToGridLocation:retreatLocation];
                    [_gameboard removeCardAtGameBoardNode:targetNode];
                    [_gameboard swapCardFromNode:[_gameboard activeNode] toNode:[_gameboard getGameBoardNodeForGridLocation:retreatLocation]];
                    
                    NSUInteger remainingActions = [_gameManager actionUsed:action];
                    [self updateRemainingActions:remainingActions];
                    [self resetUserInterface];
                    [self checkForEndTurn];
                    
                    if (completion != nil) {
                        completion();
                    }
                }];
            }
            else {
                [_gameManager cardHasBeenDefeated:targetNode.card.model];
                [_gameManager card:[_gameboard activeNode].card.model movedToGridLocation:targetNode.locationInGrid];
                [_gameboard replaceCardAtGameBoardNode:targetNode withCard:[_gameboard activeNode].card];
                
                NSUInteger remainingActions = [_gameManager actionUsed:action];
                [self updateRemainingActions:remainingActions];
                [self resetUserInterface];
                [self checkForEndTurn];
                
                if (completion != nil) {
                    completion();
                }
            }
        }
    }];
}

- (void)performRangedAction:(Action *)action targetNode:(GameBoardNode *)targetNode onCompletion:(void (^)())completion {
    
    CombatOutcome combatOutcome = [[GameManager sharedManager] resolveCombatBetween:action.cardInAction defender:action.enemyCard];
    
    if (combatOutcome == kCombatOutcomeAttackSuccessful) {
        [ParticleHelper applyBurstToNode:targetNode];
        
        [_gameManager cardHasBeenDefeated:action.enemyCard];

        // TODO: Possible bug here - card not always removed
        [_gameboard removeCardAtGameBoardNode:targetNode];
    }

    [self resetUserInterface];
    
    NSUInteger remainingActions = [_gameManager actionUsed:action];
    [self updateRemainingActions:remainingActions];
    [self checkForEndTurn];

    if (completion != nil) {
        completion();
    }
}

- (void)turnChangedToPlayerWithColor:(PlayerColors)player {
    
    if (_turnIndicator != nil) {
        [_turnIndicator removeFromParentAndCleanup:YES];
    }
    
    _turnIndicator = [CCSprite spriteWithFile:player == kPlayerGreen ? @"green_indicator.png" : @"red_indicator.png"];
    _turnIndicator.position = ccp(_winSize.width - _turnIndicator.contentSize.width, _winSize.height - _turnIndicator.contentSize.height - 50);
    [self addChild:_turnIndicator];
    
    [self updateRemainingActions:_gameManager.currentGame.numberOfAvailableActions];

    if (player == _gameManager.currentGame.enemyColor) {
        
        [self performSelector:@selector(doEnemyPlayerTurn) withObject:nil afterDelay:1.0];
    }
}

- (void)doEnemyPlayerTurn {
    
    if (_gameover) {
        return;
    }
    
    if (_gameManager.currentPlayersTurn != _gameManager.currentGame.enemyColor) {
        return;
    }
    
    Action *nextAction = [_gameManager getActionForEnemeyPlayer];
    
    nextAction.delegate = self;
        
    GridLocation *fromLocation = nextAction.cardInAction.cardLocation;
    GridLocation *toLocation = [[nextAction.path lastObject] location];
    
    GameBoardNode *fromNode = [_gameboard getGameBoardNodeForGridLocation:fromLocation];
    GameBoardNode *toNode = [_gameboard getGameBoardNodeForGridLocation:toLocation];
    
    CCLOG(@"Enemy performing action: %@ - from node: %@ to node: %@", nextAction, fromNode, toNode);
    
    [_gameboard selectCardInGameBoardNode:fromNode useHighlighting:NO];

    if ([nextAction isKindOfClass:[MeleeAttackAction class]]) {
        
        [_gameboard highlightCardAtLocation:toNode.locationInGrid withColor:ccc3(235, 0, 0) actionType:kActionTypeMelee];

        [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallBlock actionWithBlock:^{
            [self performMeleeAction:nextAction targetNode:toNode onCompletion:^{
                
                [nextAction.cardInAction performedAction:nextAction];
                [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallFunc actionWithTarget:self selector:@selector(doEnemyPlayerTurn)], nil]];
            }];
        }],nil]];
    }
    
    else if ([nextAction isKindOfClass:[RangedAttackAction class]]) {
        
        [_gameboard highlightCardAtLocation:toNode.locationInGrid withColor:ccc3(235, 0, 0) actionType:kActionTypeRanged];

        [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallBlock actionWithBlock:^{
            [self performRangedAction:nextAction targetNode:toNode onCompletion:^{
                [nextAction.cardInAction performedAction:nextAction];
                [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallFunc actionWithTarget:self selector:@selector(doEnemyPlayerTurn)], nil]];
            }];
        }], nil]];
    }
    
    else if ([nextAction isKindOfClass:[MoveAction class]]){
        
        [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallBlock actionWithBlock:^{
            [nextAction performActionWithCompletion:^{
                [nextAction.cardInAction performedAction:nextAction];
                [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallFunc actionWithTarget:self selector:@selector(doEnemyPlayerTurn)], nil]];
            }];
        }], nil]];
    }
}

- (void)resetUserInterface {
    
    [_gameboard deselectActiveNode];
    [_gameboard deHighlightAllNodes];
    [self hideToolsPanel];
}

- (void)card:(CardSprite *)card movedToNode:(GameBoardNode *)node {
    
    [card.model consumeMove];
}

- (void)combatHasStartedBetweenAttacker:(Card *)attacker andDefender:(Card *)defender {
    
    [[SoundManager sharedManager] playSoundEffectWithName:attacker.attackSound];
}

- (void)cardHasBeenDefeatedInCombat:(Card *)card {
    
    [[SoundManager sharedManager] playSoundEffectWithName:BOOM_SOUND];
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
        _gameover = YES;
        [[CCDirector sharedDirector] replaceScene:[MainMenuScene scene]];
        return;
    }
}

- (void)updateRemainingActions:(NSUInteger)remainingActions {
    
    _actionCountLabel.string = [NSString stringWithFormat:@"%d", remainingActions];
}

- (void)showToolsPanel {
    
    _leftPanel.selectedCard = nil;
    [_leftPanel runAction:[CCMoveTo actionWithDuration:0.5 position:ccp((_leftPanel.contentSize.width / 2) - 5, _winSize.height / 2)]];
}

- (void)hideToolsPanel {
    
    [_leftPanel runAction:[CCSequence actions:[CCMoveTo actionWithDuration:0.5 position:ccp(-_leftPanel.contentSize.width, _winSize.height / 2)],
                           [CCCallBlock actionWithBlock:^{
        [_leftPanel reset];
    }], nil]];
}

- (void)leftPanelInfoButtonPressed:(LeftPanel *)leftPanel {
    
    if (_showingDetailOfNode != nil) {
        [self hideCardDetail];
    }
    else {
        [self showCardDetail];
    }
}

- (void)showCardDetail {
    
    GameBoardNode *activeNode = [_gameboard activeNode];
    
    if (activeNode != nil && activeNode.hasCard) {
        
        activeNode.card.zOrder = 1000;
        _showingDetailOfNode = activeNode;
        
        [_gameboard deselectActiveNode];
        [activeNode.card toggleDetailWithScale:0.4];
        [activeNode.card runAction:[CCMoveTo actionWithDuration:0.50 position:ccp(_winSize.width / 2, _winSize.height / 2)]];
    }
}

- (void)hideCardDetail {
    
    [_showingDetailOfNode.card toggleDetailWithScale:0.4];
    
    [_showingDetailOfNode.card runAction:[CCMoveTo actionWithDuration:0.50 position:[_gameboard convertToWorldSpace:_showingDetailOfNode.position]]];
    
    [_gameboard selectCardInGameBoardNode:_showingDetailOfNode useHighlighting:NO];
    _showingDetailOfNode.card.zOrder = 5;
    _showingDetailOfNode = nil;
}

- (void)leftPanelAttackButtonPressed:(LeftPanel *)leftPanel {
    
    if (_actionInQueue != nil) {
        MeleeAttackAction *action = (MeleeAttackAction*)_actionInQueue;
        action.meleeAttackType = kMeleeAttackTypeNormal;
        
        GameBoardNode *targetNode = [_gameboard getGameBoardNodeForGridLocation:action.enemyCard.cardLocation];
        
        [self performMeleeAction:action targetNode:targetNode onCompletion:^{
            [action.cardInAction performedAction:action];
            _actionInQueue = nil;
        }];
    }
}

- (void)leftPanelAttackAndConquerButtonPressed:(LeftPanel *)leftPanel {

    if (_actionInQueue != nil) {
        MeleeAttackAction *action = (MeleeAttackAction*)_actionInQueue;
        action.meleeAttackType = kMeleeAttackTypeConquer;
        
        GameBoardNode *targetNode = [_gameboard getGameBoardNodeForGridLocation:action.enemyCard.cardLocation];
        
        [self performMeleeAction:action targetNode:targetNode onCompletion:^{
            [action.cardInAction performedAction:action];
            _actionInQueue = nil;
        }];
    }
}

@end
