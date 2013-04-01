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
#import "AbilityAction.h"

@interface GameScene()

- (void)addDeckToScene:(Deck*)deck;

- (void)showToolsPanel;
- (void)hideToolsPanel;

- (void)resetUserInterface;
- (void)resetAttackDirection;

- (void)checkForEndTurn;
- (void)doEnemyPlayerTurn;

- (void)updateRemainingActions:(NSUInteger)remainingActions;

- (void)showCardDetail;
- (void)hideCardDetail;

- (void)performQueuedMeleeActionWithAttackType:(MeleeAttackTypes)attackType;

- (void)displayCombatOutcome:(CombatOutcome)combatOutcome;

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
        
        [_gameboard layoutBoard];

        _myCards = [[NSMutableArray alloc] initWithCapacity:_gameManager.currentGame.myDeck.cards.count];
        [self addDeckToScene:[GameManager sharedManager].currentGame.myDeck];
        [_gameboard layoutDeck:_myCards forPlayerWithColor:_gameManager.currentGame.myColor];

        if (_gameManager.currentGame.state == kGameStateGameStarted) {
            _enemyCards = [[NSMutableArray alloc] initWithCapacity:_gameManager.currentGame.enemyDeck.cards.count];
            [self addDeckToScene:[GameManager sharedManager].currentGame.enemyDeck];
            [_gameboard layoutDeck:_enemyCards forPlayerWithColor:_gameManager.currentGame.enemyColor];
        }
        
        [_gameManager.currentGame populateUnitLayout];

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
        
        if ([card isOwnedByMe]) {
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
    
    UITouch *touch = [touches anyObject];

    if (CGRectContainsPoint(_backButton.boundingBox, [self convertTouchToNodeSpace:touch])) {
        
        [[CCDirector sharedDirector] replaceScene:[MainMenuScene scene]];
        return;
    }

    if (_gameManager.currentGame.state != kGameStateGameStarted) {
        return;
    }
    
    if (_gameManager.currentGame.gameOver) {
        [[CCDirector sharedDirector] replaceScene:[MainMenuScene scene]];
        return;
    }

    if (_gameManager.currentPlayersTurn != _gameManager.currentGame.myColor) {
        return;
    }
    
    if (_gameboard.isMoving) {
        return;
    }
                    
    if (_showingDetailOfNode != nil) {
        return;
    }
    
    GameBoardNode *targetNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertTouchToNodeSpace:touch]];
    
    if (targetNode != nil) {
        
        if ([_gameboard nodeIsActive]) {
            
            Action *action = [_battlePlan getActionToGridLocation:targetNode.locationInGrid];
            
            if (action == nil || ![action isWithinRange]) {
                
                [self resetUserInterface];
                [self resetAttackDirection];
                return;
            }
            
            if (_actionInQueue != nil) {
                
                if (_selectedAttackDirection != nil) {
                    [_gameboard deHighlightSelectedAttackDirectionAtLocation:_selectedAttackDirection];
                }
                
                _pathInQueue = [_attackDirections objectForKey:targetNode.locationInGrid];
                if (_pathInQueue != nil) {
                    _selectedAttackDirection = targetNode.locationInGrid;
                    [_gameboard highlightSelectedAttackDirectionAtLocation:_selectedAttackDirection];
                }
                return;
            }
            
            action.delegate = self;
            
            if ([action isKindOfClass:[MeleeAttackAction class]]) {
                [_gameboard highlightCardAtLocation:action.enemyCard.cardLocation withColor:ccc3(235, 0, 0) actionType:kActionTypeMelee];
                
                if (_battlePlan.meleeActions.count > 0) {
                    _leftPanel.selectedAction = action;
                    
                    _attackDirections = [_battlePlan getAttackDirectionsForCard:action.cardInAction whenAttackingEnemyCard:action.enemyCard withUnitLayout:_gameManager.currentGame.unitLayout];
                    
                    [_gameboard highlightNodesForAttackDirectionAtLocations:_attackDirections.allKeys];
                }

                _actionInQueue = action;
            }
            else {
                [action performActionWithCompletion:^{
                }];
            }
        }
        else {
            if (targetNode.hasCard && [targetNode.card.model isOwnedByPlayerWithColor:_gameManager.currentGame.myColor]) {
                [_gameboard selectCardInGameBoardNode:targetNode useHighlighting:NO];

                _battlePlan = [[BattlePlan alloc] init];
                [_battlePlan createBattlePlanForCard:targetNode.card.model friendlyUnits:_gameManager.currentGame.myDeck.cards enemyUnits:_gameManager.currentGame.enemyDeck.cards unitLayout:_gameManager.currentGame.unitLayout];
                
                for (Action *moveAction in _battlePlan.moveActions) {
                    [_gameboard highlightNodeAtLocation:[moveAction getLastLocationInPath] withColor:ccc3(0, 235, 0)];
                }

                for (Action *meleeAction in _battlePlan.meleeActions) {
                    [_gameboard highlightCardAtLocation:[meleeAction getLastLocationInPath] withColor:ccc3(235, 0, 0)];
                }

                for (Action *rangeAction in _battlePlan.rangeActions) {
                    [_gameboard highlightCardAtLocation:[rangeAction getLastLocationInPath] withColor:ccc3(235, 0, 0) actionType:kActionTypeRanged];
                }

                for (Action *abilityAction in _battlePlan.abilityActions) {
                    [_gameboard highlightCardAtLocation:[abilityAction getLastLocationInPath] withColor:ccc3(235, 0, 0) actionType:kActionTypeRanged];
                }
                
                [self showToolsPanel];
            }
        }
    }
}

- (void)action:(Action *)action wantsToReplaceCardAtLocation:(GridLocation *)replaceLocation withCardAtLocation:(GridLocation *)withLocation {
    
    [_gameboard replaceCardAtGameBoardNode:[_gameboard getGameBoardNodeForGridLocation:replaceLocation] withCardInGameBoardNode:[_gameboard getGameBoardNodeForGridLocation:withLocation]];
}

- (void)action:(Action *)action wantsToMoveCard:(Card *)card fromLocation:(GridLocation *)fromLocation toLocation:(GridLocation *)toLocation {
    
    [_gameboard swapCardFromNode:[_gameboard getGameBoardNodeForGridLocation:fromLocation]
                          toNode:[_gameboard getGameBoardNodeForGridLocation:toLocation]];
}

- (void)action:(Action *)action wantsToMoveFollowingPath:(NSArray *)path withCompletion:(void (^)(GridLocation *))completion {
    
    [_gameboard moveCardAtLocation:action.cardInAction.cardLocation followingPath:path onCompletion:^{
        
        PathFinderStep *lastStep = path.lastObject;
        
        completion(lastStep.location);
    }];
}

- (void)action:(Action *)action hasResolvedCombatWithOutcome:(CombatOutcome)combatOutcome {
    
    [self displayCombatOutcome:combatOutcome];
    
    if (IsAttackSuccessful(combatOutcome)) {
        
        [self cardHasBeenDefeatedInCombat:action.enemyCard];
    }
}

- (void)beforePerformAction:(Action *)action {
    
}

- (void)afterPerformAction:(Action *)action {
    
    _actionInQueue = nil;
    
    NSUInteger remainingActions = _gameManager.currentGame.numberOfAvailableActions;
    [self updateRemainingActions:remainingActions];
    [self resetUserInterface];
    [self checkForEndTurn];
}

- (void)turnChangedToPlayerWithColor:(PlayerColors)player {
    
    if (_turnIndicator != nil) {
        [_turnIndicator removeFromParentAndCleanup:YES];
    }
    
    _turnIndicator = [CCSprite spriteWithFile:player == kPlayerGreen ? @"green_indicator.png" : @"red_indicator.png"];
    _turnIndicator.position = ccp(_winSize.width - _turnIndicator.contentSize.width, _winSize.height - _turnIndicator.contentSize.height - 50);
    [self addChild:_turnIndicator];
    
    [self updateRemainingActions:_gameManager.currentGame.numberOfAvailableActions];

    if (_gameManager.currentGame.gametype == kGameTypeSinglePlayer && player == _gameManager.currentGame.enemyColor) {
        
        [self performSelector:@selector(doEnemyPlayerTurn) withObject:nil afterDelay:1.0];
    }
}

- (void)doEnemyPlayerTurn {
    
    if (_gameManager.currentGame.gameOver) {
        return;
    }
    
    if (_gameManager.currentPlayersTurn != _gameManager.currentGame.enemyColor) {
        return;
    }
    
    Action *nextAction = [_gameManager getActionForEnemeyPlayer];
    
    if (nextAction == nil) {
        [self checkForEndTurn];
        return;
    }
    
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
            [nextAction performActionWithCompletion:^{
                [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallFunc actionWithTarget:self selector:@selector(doEnemyPlayerTurn)], nil]];
            }];
        }],nil]];
    }
    
    else if ([nextAction isKindOfClass:[RangedAttackAction class]]) {
        
        [_gameboard highlightCardAtLocation:toNode.locationInGrid withColor:ccc3(235, 0, 0) actionType:kActionTypeRanged];

        [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallBlock actionWithBlock:^{
            [nextAction performActionWithCompletion:^{
                [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallFunc actionWithTarget:self selector:@selector(doEnemyPlayerTurn)], nil]];
            }];
        }], nil]];
    }
    
    else if ([nextAction isKindOfClass:[MoveAction class]]){
        
        [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallBlock actionWithBlock:^{
            [nextAction performActionWithCompletion:^{
                [self runAction:[CCSequence actions:[CCDelayTime actionWithDuration:kEnemyActionDelayTime], [CCCallFunc actionWithTarget:self selector:@selector(doEnemyPlayerTurn)], nil]];
            }];
        }], nil]];
    }
}

- (void)resetAttackDirection {
    
    _actionInQueue = nil;
    _pathInQueue = nil;
    _selectedAttackDirection = nil;
}

- (void)resetUserInterface {
    
    [_gameboard deselectActiveNode];
    [_gameboard deHighlightAllNodes];
    [self hideToolsPanel];
}

- (void)card:(CardSprite *)card movedToNode:(GameBoardNode *)node {
    
}

- (void)combatHasStartedBetweenAttacker:(Card *)attacker andDefender:(Card *)defender {
    
    [[SoundManager sharedManager] playSoundEffectWithName:attacker.attackSound];
}

- (void)cardHasBeenDefeatedInCombat:(Card *)card {
    
    [[SoundManager sharedManager] playSoundEffectWithName:BOOM_SOUND];
    
    GameBoardNode *node = [_gameboard getGameBoardNodeForGridLocation:card.cardLocation];
    
    [ParticleHelper applyBurstToNode:node];
    
    if (card.dead) {
        [_gameboard removeCardAtGameBoardNode:node];
    }
}

- (void)checkForEndTurn {
    
    GameResults result = [_gameManager checkForEndGame];
    
    if (result == kGameResultInProgress) {
        if ([_gameManager shouldEndTurn]) {
            [_gameManager endTurn];
        }
    }
    else {
        
        CCLabelTTF *gameoverStatus;
        
        if (result == kGameResultVictory) {
            gameoverStatus = [CCLabelTTF labelWithString:@"Victory!" fontName:APP_FONT fontSize:48];
            [gameoverStatus setColor:ccc3(0, 255.0, 0)];
            [[SoundManager sharedManager] playSoundEffectWithName:FANFARE];
        }
        else {
            gameoverStatus = [CCLabelTTF labelWithString:@"Defeat!" fontName:APP_FONT fontSize:48];
            [gameoverStatus setColor:ccc3(255.0, 0, 0)];
        }
        
        gameoverStatus.position = ccp(_winSize.width / 2, _winSize.height - (_winSize.height / 4));
        [self addChild:gameoverStatus z:5000];
    }
}

- (void)updateRemainingActions:(NSUInteger)remainingActions {
    
    _actionCountLabel.string = [NSString stringWithFormat:@"%d", remainingActions];
}

- (void)showToolsPanel {
    
    _leftPanel.selectedAction = nil;
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
        
        activeNode.card.zOrder = 10000;
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

- (void)performQueuedMeleeActionWithAttackType:(MeleeAttackTypes)attackType {
    
    if (_actionInQueue != nil) {
        MeleeAttackAction *action = (MeleeAttackAction*)_actionInQueue;
        
        action.meleeAttackType = attackType;
        
        if (_pathInQueue != nil) {
            action.path = _pathInQueue;
        }
        
        [_actionInQueue performActionWithCompletion:^{
            [self resetAttackDirection];
        }];
    }
}

- (void)leftPanelAttackButtonPressed:(LeftPanel *)leftPanel {
    
    [self performQueuedMeleeActionWithAttackType:kMeleeAttackTypeNormal];
}

- (void)leftPanelAttackAndConquerButtonPressed:(LeftPanel *)leftPanel {

    [self performQueuedMeleeActionWithAttackType:kMeleeAttackTypeConquer];
}

- (void)displayCombatOutcome:(CombatOutcome)combatOutcome {
    
    CCLabelTTF *label;
    
    if (IsDefenseSuccessful(combatOutcome)) {
        
        if (combatOutcome == kCombatOutcomeDefendSuccessfulMissed) {
            label = [CCLabelTTF labelWithString:@"Misssed!" fontName:APP_FONT fontSize:24];
        }
        else {
            label = [CCLabelTTF labelWithString:@"Unit defended" fontName:APP_FONT fontSize:24];
        }
        
        [label setColor:ccc3(0, 0, 0)];
    }
    else if (IsAttackSuccessful(combatOutcome)) {
        label = [CCLabelTTF labelWithString:@"Attack successful" fontName:APP_FONT fontSize:24];
        [label setColor:ccc3(0, 0, 0)];
    }
    else if (IsPushSuccessful(combatOutcome)) {
        label = [CCLabelTTF labelWithString:@"Pushed!" fontName:APP_FONT fontSize:24];
        [label setColor:ccc3(0, 0, 0)];
    }
    
    label.position = ccp(_winSize.width / 2, _winSize.height - 100);
    label.zOrder = 1000;
    [self addChild:label];

    CCMoveTo *moveAction = [CCMoveTo actionWithDuration:2.0 position:ccp(_winSize.width / 2, _winSize.height + 25)];
    CCFadeOut *fadeAction = [CCFadeOut actionWithDuration:3.0];
    CCCallBlock *removeLabel = [CCCallBlock actionWithBlock:^{
        
        [label removeFromParentAndCleanup:YES];
    }];
    
    [label runAction:[CCSequence actions:[CCEaseSineIn actionWithAction:[CCSpawn actions:moveAction, fadeAction, nil]], removeLabel, nil]];
}

@end
