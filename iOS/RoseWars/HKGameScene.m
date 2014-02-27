//
//  HKGameScene.m
//  RoseWars
//
//  Created by Heine Skov Kristensen on 9/30/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import "HKGameScene.h"
#import "GameBoardNode.h"
#import "GameManager.h"
#import "PlayerIndicator.h"
#import "HKImageButton.h"
#import "HKGameTypeScene.h"
#import "AbilityAction.h"
#import "HKDialogNode.h"
#import "HKLevelIncreaseDialog.h"
#import "FixedLevelIncreaseStrategy.h"
#import "HKBattleResultNode.h"
#import "HKGameOptionsDialog.h"
#import "HKConquerButton.h"

static float const kCardSpriteScaleFactor = 0.33;
static float const kCardSpriteScaleFactorExtendedHeight = 0.40;

static NSString* const kDialogNodeTagGameEnded = @"DialogNodeTagGameEnded";

@interface HKGameScene()

@property (strong, nonatomic) MeleeAttackAction *conquerAction;
@property (strong, nonatomic) GameBoardNode *conquerNode;

- (void)addDeckToScene:(Deck*)deck;

- (void)showToolsPanel;
- (void)hideToolsPanel;

- (void)resetUserInterface;
- (void)resetAttackDirection;

- (void)checkForEndTurnAfterAction:(Action*)action;
- (void)doEnemyPlayerTurn;

- (void)updateRemainingActions:(NSUInteger)remainingActions;

- (void)showCardDetail;
- (void)hideCardDetail;

- (void)performQueuedMeleeActionWithAttackType:(MeleeAttackTypes)attackType;

- (void)displayCombatOutcome:(BattleResult*)result;

- (BOOL)isAttackDirection:(GameBoardNode*)node;

- (void)layoutMyDeck;
- (void)layoutEnemyDeck;

- (void)handleTouchEndedWithTouch:(UITouch*)touch;

- (BattlePlan*)createBattlePlanForNode:(GameBoardNode *)node;

@end

@implementation HKGameScene

- (void)didMoveToView:(SKView *)view {
    
    CGSize size = self.size;
    
    self.backgroundColor = [UIColor blackColor];
    
    _gameManager = [GameManager sharedManager];
    _gameManager.delegate = self;
    
    [GCTurnBasedMatchHelper sharedInstance].delegate = self;

    SKSpriteNode *background = [SKSpriteNode spriteNodeWithImageNamed:@"woddenbackground2.png"];
    background.anchorPoint = CGPointMake(0, 0);
    background.size = self.size;
    [background setZPosition:-1];
    [self addChild:background];
    
    _gameboard = [[GameBoard alloc] init];
    
    _gameboard.size = size;
    _proceedToEnemyTurn = YES;
    
    if (IS_IPHONE5) {
        _gameboard.scale = 0.75;
        _gameboard.position = CGPointMake((size.width / 2) - (_gameboard.size.width / 2), (size.height / 2) - 55);
    }
    else {
        _gameboard.scale = 0.65;
        _gameboard.position = CGPointMake((size.width / 2) - (_gameboard.size.width / 2), (size.height / 2) + 25);
    }
    
    _gameboard.rows = 8;
    _gameboard.columns = 5;
    _gameboard.colorOfTopPlayer = _gameManager.currentGame.enemyColor;
    _gameboard.colorOfBottomPlayer = _gameManager.currentGame.myColor;
    _gameboard.delegate = self;
    
    _leftPanel = [[LeftPanel alloc] init];
    _leftPanel.delegate = self;
    _leftPanel.position = ccp(-_leftPanel.size.width, (size.height / 2));
    _leftPanel.zPosition = kOverlayZOrder;
    [self addChild:_leftPanel];
    
    _playerIndicator = [[PlayerIndicator alloc] init];
    _playerIndicator.position = ccp(size.width / 2, size.height + _playerIndicator.size.height);
    [_playerIndicator setZPosition:kOverlayZOrder];
    [self addChild:_playerIndicator];
    
    _actionCountLabel = [[SKLabelNode alloc] initWithFontNamed:APP_FONT];
    _actionCountLabel.fontSize = 32.0f;
    _actionCountLabel.text = [NSString stringWithFormat:@"%d", _gameManager.currentGame.numberOfAvailableActions];
    _actionCountLabel.position = ccp(size.width - 30, size.height - 50);
    _actionCountLabel.zPosition = kOverlayZOrder;
    [self addChild:_actionCountLabel];
    
    _backButton = [HKImageButton imageButtonWithImage:@"settings_button" block:^(id sender) {
        HKGameOptionsDialog *dialog = [[HKGameOptionsDialog alloc] initWithScene:self];
        dialog.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMidY(self.frame));
        dialog.delegate = self;
        [self addChild:dialog];
    }];
    
    _backButton.position = ccp(5, size.height - _backButton.size.height - 10);
    _backButton.anchorPoint = ccp(0, 0);
    _backButton.zPosition = kOverlayZOrder;
    [self addChild:_backButton];
    
    [self addChild:_gameboard];
    
    [GCTurnBasedMatchHelper sharedInstance].delegate = self;
    
    [_gameboard layoutBoard];
    [self layoutMyDeck];
    
    if (_gameManager.currentGame.state == kGameStateGameStarted) {
        [self layoutEnemyDeck];
    }
    
    [_gameManager.currentGame populateUnitLayout];
    
    _battlePlan = [[BattlePlan alloc] init];
    
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(cardIncreasedInLevel:) name:GAMEEVENT_LEVEL_INCREASED object:nil];
    
    [self turnChangedToPlayerWithColor:_gameManager.currentPlayersTurn];
    [_gameManager.currentGame addObserver:self forKeyPath:@"currentPlayersTurn" options:NSKeyValueObservingOptionNew context:nil];
    
    if (_gameManager.currentGame.gameOver) {
        GameResults result = [_gameManager checkForEndGame];
        [self showGameResult:result];
    }
    
    if (_gameManager.currentPlayersTurn == _gameManager.currentGame.myColor) {
        _cardsInvolvedInPlayback = [NSMutableArray array];
        _abilitiesInvolvedInPlayback = [NSMutableArray array];
        [self performSelector:@selector(playbackLastAction) withObject:nil afterDelay:1.0];
    }
}

- (void)dialogNodeDidDismiss:(HKGameOptionsDialog *)dialogNode withSelectedResult:(GameOptionsDialogResult)result {
    
    if (result == GameOptionsDialogMainMenu) {
        [self popToMainMenu];
    }
}

- (void)popToMainMenu {
    
    [_gameManager.currentGame removeObserver:self forKeyPath:@"currentPlayersTurn"];
    [self.view presentScene:[[HKGameTypeScene alloc] initWithSize:self.size] transition:[SKTransition fadeWithDuration:0.5]];
}

- (float)currentCardScale {
    
    return IS_IPHONE5 ? kCardSpriteScaleFactorExtendedHeight : kCardSpriteScaleFactor;
}

- (void)layoutMyDeck {
    _myCards = [[NSMutableArray alloc] initWithCapacity:_gameManager.currentGame.myDeck.cards.count];
    [self addDeckToScene:[GameManager sharedManager].currentGame.myDeck];
    [_gameboard layoutDeck:_myCards withCardScale:[self currentCardScale] forPlayerWithColor:_gameManager.currentGame.myColor];
}

- (void)layoutEnemyDeck {
    _enemyCards = [[NSMutableArray alloc] initWithCapacity:_gameManager.currentGame.enemyDeck.cards.count];
    [self addDeckToScene:[GameManager sharedManager].currentGame.enemyDeck];
    [_gameboard layoutDeck:_enemyCards withCardScale:[self currentCardScale] forPlayerWithColor:_gameManager.currentGame.enemyColor];
}

- (void)addDeckToScene:(Deck *)deck {
    
    CGSize screenSize = self.size;
    
    for (Card *card in deck.cards) {
        
        CardSprite *cardSprite = [[CardSprite alloc] initWithCard:card];
        
        cardSprite.position = ccp(screenSize.width / 2, screenSize.height + 50);
        cardSprite.name = CARD_TAG;
        
        [self addChild:cardSprite];
        
        if ([card isOwnedByMe]) {
            [_myCards addObject:cardSprite];
        }
        else {
            [_enemyCards addObject:cardSprite];
        }
    }
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    
    [super touchesBegan:touches withEvent:event];
}

- (void)touchesEnded:(NSSet *)touches withEvent:(UIEvent *)event {
    
    UITouch *touch = [touches anyObject];
    
    [self handleTouchEndedWithTouch:touch];
}

- (BOOL)isAttackDirection:(GameBoardNode *)node {
    
    return [_attackDirections objectForKey:node.locationInGrid] != nil;
}

- (void)handleTouchEndedWithTouch:(UITouch *)touch {
        
    if (_playback) {
        return;
    }
    
    if (_gameManager.currentGame.state != kGameStateGameStarted) {
        return;
    }
    
    if (_gameManager.currentGame.gameOver) {
        [self popToMainMenu];
        return;
    }
    
    if (_gameManager.currentPlayersTurn != _gameManager.currentGame.myColor) {
        return;
    }
    
    if (_gameboard.isMoving) {
        return;
    }
    
    if (_showingDetailOfNode != nil) {
        
        if ([_showingDetailOfNode.card.model isOwnedByEnemy]) {
            [_gameboard deselectActiveNode];
        }
        
        [self hideCardDetail];
    }
    
    GameBoardNode *targetNode = [_gameboard getGameBoardNodeForPosition:[touch locationInNode:_gameboard]];
    
    if (targetNode != nil) {
        
        GameBoardNode *conquerNode = [_gameboard nodeHighlightedForConquer];
        if (conquerNode) {
            if ((targetNode != conquerNode)) {
                // User selected different node than conquernode
                [_gameboard highlightNodeAtLocation:conquerNode.locationInGrid forConquer:NO];
                self.conquerAction = nil;
            }
            else {
                [self.conquerAction conquerEnemyLocation:self.conquerNode.locationInGrid withCompletion:^{
                    [_gameboard highlightNodeAtLocation:conquerNode.locationInGrid forConquer:NO];
                    [self afterPerformAction:self.conquerAction];
                }];
            }
        }

        if ([_gameboard nodeIsActive]) {
            
            // User selected the same unit again - deselect it
            if (_gameboard.activeNode == targetNode) {
                [_gameboard deHighlightAllNodes];
                [_gameboard deselectActiveNode];
                [self hideToolsPanel];
                return;
            }
            
            Action *action = [_battlePlan getActionToGridLocation:targetNode.locationInGrid];
            
            if (![self isAttackDirection:targetNode]) {
                if (action == nil || ![action isWithinRange]) {
                    
                    [self resetUserInterface];
                    [self resetAttackDirection];
                    
                    if ([targetNode.card.model isOwnedByMe]) {
                        [self createBattlePlanForNode:targetNode];
                        if (_battlePlan.hasActions) {
                            [self showToolsPanel];
                        }
                        else {
                            [self hideToolsPanel];
                        }
                    }
                    else {
                        [self hideToolsPanel];
                    }
                    
                    return;
                }
            }
            
            if (_actionInQueue != nil) {
                
                _pathInQueue = [_attackDirections objectForKey:targetNode.locationInGrid];
                if (_pathInQueue != nil ) {
                    _actionInQueue.path = _pathInQueue;
                    [_actionInQueue performActionWithCompletion:^{
                        
                        if ([_actionInQueue isKindOfClass:[MeleeAttackAction class]]) {
                            MeleeAttackAction *attackAction = (MeleeAttackAction*)_actionInQueue;
                            if ([attackAction unitCanConquerEnemyLocation]) {
                                GameBoardNode *enemyNode = [_gameboard getGameBoardNodeForGridLocation:attackAction.enemyCard.cardLocation];
                                [self afterPerformAction:_actionInQueue];
                                [_gameboard highlightNodeAtLocation:enemyNode.locationInGrid forConquer:YES];
                                self.conquerAction = attackAction;
                                self.conquerNode = enemyNode;
                            }
                            else {
                                [self afterPerformAction:_actionInQueue];
                            }
                        }
                        else {
                            [self afterPerformAction:_actionInQueue];
                        }
                    }];
                }
                return;
            }
            
            action.delegate = self;
            
            if ([action isKindOfClass:[MeleeAttackAction class]]) {
                [_gameboard highlightCardAtLocation:action.enemyCard.cardLocation withColor:[SKColor colorWithRed:1.0/235.0 green:0.0 blue:0.0 alpha:1.0] actionType:kActionTypeMelee];
                
                if (_battlePlan.meleeActions.count > 0) {
                    
                    _leftPanel.selectedAction = action;
                    
                    _attackDirections = [_battlePlan getAttackDirectionsAction:(MeleeAttackAction*)action withUnitLayout:_gameManager.currentGame.unitLayout];
                    
                    if (_attackDirections.count - 1 > 1) {
                        [_gameboard highlightNodesForAttackDirectionAtLocations:_attackDirections.allKeys];
                        _actionInQueue = action;
                    }
                    else {
                        [action performActionWithCompletion:^{
                            
                            MeleeAttackAction *attackAction = (MeleeAttackAction*)action;
                            if ([attackAction unitCanConquerEnemyLocation]) {
                                GameBoardNode *enemyNode = [_gameboard getGameBoardNodeForGridLocation:attackAction.enemyCard.cardLocation];
                                [self afterPerformAction:action];
                                [_gameboard highlightNodeAtLocation:enemyNode.locationInGrid forConquer:YES];
                                self.conquerAction = attackAction;
                                self.conquerNode= enemyNode;
                            }
                            else {
                                [self afterPerformAction:action];
                            }
                        }];
                    }
                }
            }
            else {
                [action performActionWithCompletion:^{
                }];
            }
        }
        else {
            if ([targetNode.card.model isOwnedByMe]) {
                _battlePlan = [self createBattlePlanForNode:targetNode];
                
                if ([_battlePlan hasActions]) {
                    [self showToolsPanel];
                }
            }
            else {
                [_gameboard selectCardInGameBoardNode:targetNode useHighlighting:NO];
                [self showCardDetail];
            }
        }
    }
}

- (BattlePlan*)createBattlePlanForNode:(GameBoardNode *)node {
    
    BattlePlan *battleplan = [[BattlePlan alloc] init];
    
    if (node.hasCard && [node.card.model isOwnedByPlayerWithColor:_gameManager.currentGame.myColor]) {
        [_gameboard selectCardInGameBoardNode:node useHighlighting:NO];
        
        [battleplan createBattlePlanForCard:node.card.model friendlyUnits:_gameManager.currentGame.myDeck.cards enemyUnits:_gameManager.currentGame.enemyDeck.cards unitLayout:_gameManager.currentGame.unitLayout];
        
        for (Action *moveAction in battleplan.moveActions) {
            [_gameboard highlightNodeAtLocation:[moveAction getLastLocationInPath] withColor:RGB(0, 235, 0)];
        }
        
        for (Action *meleeAction in battleplan.meleeActions) {
            [_gameboard highlightCardAtLocation:[meleeAction getLastLocationInPath] withColor:RGB(235, 0, 0)];
        }
        
        for (Action *rangeAction in battleplan.rangeActions) {
            [_gameboard highlightCardAtLocation:[rangeAction getLastLocationInPath] withColor:RGB(235, 0, 0) actionType:kActionTypeRanged];
        }
        
        for (Action *abilityAction in battleplan.abilityActions) {
            [_gameboard highlightCardAtLocation:[abilityAction getLastLocationInPath] withColor:RGB(235, 0, 0) actionType:kActionTypeRanged];
        }
    }
    else {
        battleplan = nil;
    }
    
    return battleplan;
}

- (void)cardIncreasedInLevel:(NSNotification*)notification {

    HKLevelIncreaseDialog *dialog = [[HKLevelIncreaseDialog alloc] initWithCard:(Card*)notification.object inScene:self];
    dialog.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMidY(self.frame));
    dialog.delegate = self;

    // Cannot proceed to enemy turn while leveldialog is active
    _proceedToEnemyTurn = NO;
    
    [self addChild:dialog];
}

- (void)dialogNodeDidDismiss:(HKLevelIncreaseDialog *)dialogNode withSelectedAbility:(LevelIncreaseAbilities)ability {
    
    _proceedToEnemyTurn = YES;
    
    FixedLevelIncreaseStrategy *levelIncreaseStrategy = [[FixedLevelIncreaseStrategy alloc] init];
    
    levelIncreaseStrategy.levelIncreaseAbility = ability;
    [levelIncreaseStrategy cardIncreasedInLevel:dialogNode.card];
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

- (void)action:(Action *)action hasResolvedCombatWithResult:(BattleResult*)result {
    
    [self displayCombatOutcome:result];
    
    if (IsAttackSuccessful(result.combatOutcome)) {
        
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
    [self hideToolsPanel];
    [self checkForEndTurnAfterAction:action];
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    
    if ([keyPath isEqualToString:@"currentPlayersTurn"]) {
        
        [self turnChangedToPlayerWithColor:_gameManager.currentPlayersTurn];
    }
}

- (void)turnChangedToPlayerWithColor:(PlayerColors)player {
    
    if (_turnIndicator != nil) {
        [_turnIndicator removeFromParent];
    }
    
    _turnIndicator = [[SKSpriteNode alloc] initWithImageNamed:player == kPlayerGreen ? @"green_indicator.png" : @"red_indicator.png"];
    _turnIndicator.position = ccp(self.size.width - _turnIndicator.size.width, self.size.height - _turnIndicator.size.height - 50);
    [self addChild:_turnIndicator];
    
    [self updateRemainingActions:_gameManager.currentGame.numberOfAvailableActions];
    
    if (_gameManager.currentGame.gametype == kGameTypeSinglePlayer && player == _gameManager.currentGame.enemyColor) {
        
        [self performSelector:@selector(doEnemyPlayerTurn) withObject:nil afterDelay:1.0];
    }
}

- (void)doEnemyPlayerTurn {

    if (!_proceedToEnemyTurn) {
        [self performSelector:@selector(doEnemyPlayerTurn) withObject:nil afterDelay:0.5];
        return;
    }
    
    if (_gameManager.currentGame.gameOver) {
        return;
    }
    
    if (_gameManager.currentPlayersTurn != _gameManager.currentGame.enemyColor) {
        return;
    }
    
    Action *nextAction = [_gameManager getActionForEnemeyPlayer];
    
    if (nextAction == nil) {
        [self checkForEndTurnAfterAction:nextAction];
        return;
    }
    
    nextAction.delegate = self;
    
    GridLocation *fromLocation = nextAction.cardInAction.cardLocation;
    PathFinderStep *lastStep = [nextAction.path lastObject];
    GridLocation *toLocation = lastStep.location;
    
    GameBoardNode *fromNode = [_gameboard getGameBoardNodeForGridLocation:fromLocation];
    GameBoardNode *toNode = [_gameboard getGameBoardNodeForGridLocation:toLocation];
    
    NSLog(@"Enemy performing action: %@ - from node: %@ to node: %@", nextAction, fromNode, toNode);
    
    [_gameboard selectCardInGameBoardNode:fromNode useHighlighting:NO];
    
    if (nextAction.isAttack) {
        [_gameboard highlightCardAtLocation:toNode.locationInGrid withColor:[SKColor colorWithRed:1.0/235.0 green:0.0 blue:0.0 alpha:1.0] actionType:nextAction.actionType];
    }
    
    [self runAction:[SKAction sequence:@[[SKAction waitForDuration:kEnemyActionDelayTime],
                                         [SKAction runBlock:^{
        [nextAction performActionWithCompletion:^{
            [self afterPerformAction:nextAction];
            [self runAction:[SKAction sequence:@[[SKAction waitForDuration:kEnemyActionDelayTime],
                                                 [SKAction performSelector:@selector(doEnemyPlayerTurn) onTarget:self]]]];
        }];
    }]]]];
}

- (void)resetAttackDirection {
    
    _actionInQueue = nil;
    _pathInQueue = nil;
    _selectedAttackDirection = nil;
    _attackDirections = nil;
}

- (void)resetUserInterface {
    
    [_gameboard deselectActiveNode];
    [_gameboard deHighlightAllNodes];
}

- (void)card:(CardSprite *)card movedToNode:(GameBoardNode *)node {
    
}

- (void)combatHasStartedBetweenAttacker:(Card *)attacker andDefender:(Card *)defender {
    
    [self runAction:[SKAction playSoundFileNamed:attacker.attackSound waitForCompletion:NO]];
}

- (void)cardHasBeenDefeatedInCombat:(Card *)card {
    
    [self runAction:[SKAction playSoundFileNamed:card.defeatSound waitForCompletion:NO]];
    
    GameBoardNode *node = [_gameboard getGameBoardNodeForGridLocation:card.cardLocation];
    
    if (card.dead) {
        [_gameboard removeCardAtGameBoardNode:node];
    }
}

- (void)showGameResult:(GameResults)result {
    HKDialogNode *gamestatusDialog = [[HKDialogNode alloc] initWithCaption:@"Battle ended!" dialogText:@"" inScene:self];
    gamestatusDialog.dialogTextNode.fontSize = 48.0f;
    
    if (result == kGameResultVictory) {
        gamestatusDialog.dialogTextNode.text = @"Victory!";
        gamestatusDialog.dialogTextNode.fontColor = [SKColor greenColor];

        [self runAction:[SKAction playSoundFileNamed:@"fanfare.mp3" waitForCompletion:NO]];
    }
    else {
        gamestatusDialog.dialogTextNode.text = @"Defeat!";
        gamestatusDialog.dialogTextNode.fontColor = [SKColor redColor];
    }
    
    gamestatusDialog.position = CGPointMake(CGRectGetWidth(self.frame) / 2, CGRectGetHeight(self.frame) / 2);
    gamestatusDialog.delegate = self;
    gamestatusDialog.name = kDialogNodeTagGameEnded;
    
    [self addChild:gamestatusDialog];
}

- (void)dialogNodeDidDismiss:(HKDialogNode *)dialogNode {
    
    if ([dialogNode.name isEqualToString:kDialogNodeTagGameEnded]) {
        [self popToMainMenu];
    }
}

- (void)checkForEndTurnAfterAction:(Action *)action {
    
    GameResults result = [_gameManager checkForEndGame];
    
    if (result == kGameResultInProgress) {
        if (!action.playback) {
            if ([_gameManager shouldEndTurn]) {
                if (_gameManager.currentPlayersTurn == _gameManager.currentGame.myColor) {
                    HKImageButton *endturnButton = [[HKImageButton alloc] initWithImage:@"button_endturn" selectedImage:@"button_endturn" title:@"" block:^(id sender) {
                        [endturnButton removeFromParent];
                        if (self.conquerAction) {
                            [_gameboard highlightNodeAtLocation:self.conquerNode.locationInGrid forConquer:NO];
                        }
                        [_gameManager endTurn];
                    }];
                    
                    [endturnButton setScale:0.75];
                    endturnButton.zPosition = kOverlayZOrder;
                    endturnButton.removeOnClick = YES;
                    endturnButton.position = _turnIndicator.position;
                    [self addChild:endturnButton];
                }
                else {
                    [_gameManager endTurn];
                }
            }
        }
    }
    else {
        
        [self showGameResult:result];
        
        [_gameManager endGameWithGameResult:result];
    }
}

- (void)updateRemainingActions:(NSUInteger)remainingActions {
    
    _actionCountLabel.text = [NSString stringWithFormat:@"%d", remainingActions];
}

- (void)showToolsPanel {
    
    _leftPanel.selectedAction = nil;
    [_leftPanel runAction:[SKAction moveTo:ccp((_leftPanel.size.width / 2) - 5, (self.size.height / 2)) duration:0.5]];
}

- (void)hideToolsPanel {
    
    [_leftPanel runAction:[SKAction sequence:@[[SKAction moveTo:ccp(-_leftPanel.size.width, (self.size.height / 2)) duration:0.5],
                                               [SKAction runBlock:^{
        [_leftPanel reset];
    }]]]];
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
        
        activeNode.card.zPosition = 10000;
        _showingDetailOfNode = activeNode;
        
        [_gameboard deselectActiveNode];
        [activeNode.card toggleDetailWithScale:2.0];
        [activeNode.card runAction:[SKAction moveTo:ccp(self.size.width / 2, self.size.height / 2) duration:0.2]];
    }
}

- (void)hideCardDetail {
    
    [_showingDetailOfNode.card toggleDetailWithScale:0.4];
    
    [_showingDetailOfNode.card runAction:[SKAction moveTo:[self convertPoint:_showingDetailOfNode.position fromNode:_gameboard] duration:0.5]];
    
    [_gameboard selectCardInGameBoardNode:_showingDetailOfNode useHighlighting:NO];
    _showingDetailOfNode.card.zPosition = kOverlayZOrder;
    _showingDetailOfNode = nil;
}

- (void)performQueuedMeleeActionWithAttackType:(MeleeAttackTypes)attackType {
    
    if (_actionInQueue != nil) {
        MeleeAttackAction *action = (MeleeAttackAction*)_actionInQueue;
        
        if (_pathInQueue != nil) {
            action.path = _pathInQueue;
        }
        
        action.meleeAttackType = attackType;
        
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

- (void)displayCombatOutcome:(BattleResult*)result {
    
    HKBattleResultNode *battleResultNode = [[HKBattleResultNode alloc] initWithBattleResult:result.battleResultString];
    battleResultNode.position = ccp(self.size.width / 2, self.size.height - 100);
    [self addChild:battleResultNode];
    
    SKAction *moveAction = [SKAction moveTo:ccp(self.size.width / 2, self.size.height + 25) duration:2.0];
    moveAction.timingMode = SKActionTimingEaseIn;
    SKAction *fadeAction = [SKAction fadeOutWithDuration:3.0];
    fadeAction.timingMode = SKActionTimingEaseIn;
    SKAction *removeLabel = [SKAction runBlock:^{
        [battleResultNode removeFromParent];
    }];
    
    [battleResultNode runAction:[SKAction sequence:@[[SKAction group:@[moveAction, fadeAction]], removeLabel]]];
}

- (void)sendNotice:(NSString *)notice forMatch:(GKTurnBasedMatch *)match {
    
    [GKNotificationBanner showBannerWithTitle:@"Notice" message:notice completionHandler:^{
        
    }];
}

- (void)takeTurn:(GKTurnBasedMatch *)match {
    
    GameStates oldGameState = _gameManager.currentGame.state;
    
    [_gameManager.currentGame deserializeGameData:match.matchData forPlayerWithId:[GKLocalPlayer localPlayer].playerID allPlayers:[GCTurnBasedMatchHelper sharedInstance].currentPlayerIds onlyActions:(oldGameState == kGameStateGameStarted)
                                   onlyEnemyUnits:(oldGameState == kGameStateFinishedPlacingCards)];
    
    if (oldGameState == kGameStateFinishedPlacingCards && _gameManager.currentGame.state == kGameStateGameStarted) {
        [self layoutEnemyDeck];
        [_gameManager.currentGame populateUnitLayout];
    }
    
    _cardsInvolvedInPlayback = [NSMutableArray array];
    _abilitiesInvolvedInPlayback = [NSMutableArray array];
    
    [self performSelector:@selector(playbackLastAction) withObject:nil afterDelay:1.0];
}

- (void)playbackLastAction {
    
    if ([GameManager sharedManager].currentGame.actionsForPlayback.count > 0) {
        
        if (!_playback) {
            [_playerIndicator runAction:[SKAction moveTo:ccp(self.size.width / 2, self.size.height - (_playerIndicator.size.height / 2)) duration:0.3]];
        }
        _playback = YES;
        
        Action *action = [GameManager sharedManager].currentGame.actionsForPlayback[0];
        
        action.delegate = self;
        action.playback = YES;
        
        [_gameboard selectCardInGameBoardNode:[_gameboard getGameBoardNodeForGridLocation:action.cardInAction.cardLocation] useHighlighting:NO];
        
        if (!action.isMove) {
            [_gameboard highlightCardAtLocation:action.enemyCard.cardLocation withColor:[SKColor colorWithRed:1.0/235.0 green:0.0 blue:0.0 alpha:1.0] actionType:action.actionType];
        }
        
        [self runAction:[SKAction sequence:@[[SKAction waitForDuration:kEnemyActionDelayTime],
                                             [SKAction runBlock:^{
            [action performActionWithCompletion:^{
                
                if (![_cardsInvolvedInPlayback containsObject:action.cardInAction]) {
                    [_cardsInvolvedInPlayback addObject:action.cardInAction];
                }
                
                if (action.enemyCard != nil && ![_cardsInvolvedInPlayback containsObject:action.enemyCard]) {
                    [_cardsInvolvedInPlayback addObject:action.enemyCard];
                }
                
                if ([action isKindOfClass:[MeleeAttackAction class]]) {
                    MeleeAttackAction *attackAction = (MeleeAttackAction*)action;
                    if (attackAction.autoConquer) {
                        [attackAction conquerEnemyLocation:attackAction.enemyInitialLocation withCompletion:nil];
                    }
                }
                
                if ([action isKindOfClass:[AbilityAction class]]) {
                    AbilityAction *abilityAction = (AbilityAction*)action;
                    [_abilitiesInvolvedInPlayback addObject:abilityAction.abilityUsed];
                }
                
                [_gameboard deHighlightNodeAtLocation:action.enemyCard.cardLocation];
                [self afterPerformAction:action];
                
                [[GameManager sharedManager].currentGame.actionsForPlayback removeObject:action];
                [self runAction:[SKAction sequence:@[[SKAction waitForDuration:kEnemyActionDelayTime],
                                                     [SKAction performSelector:@selector(playbackLastAction) onTarget:self]]]];
            }];
            
        }]]]];
    }
    else {
        
        [_playerIndicator runAction:[SKAction moveTo:ccp(self.size.width / 2, self.size.height + _playerIndicator.size.height) duration:0.3]];
        
        for (Card *card in _cardsInvolvedInPlayback) {
            [card resetAfterNewRound];
        }
        
        for (TimedAbility *ability in _abilitiesInvolvedInPlayback) {
            [ability forceTurnChanged];
        }
        
        _playback = NO;
        
        // Take a snapshot of the current cardstate
        [_gameManager.currentGame takeCardSnapshot:kCardSnapshotStateBeforeAction];
    }
}


@end
