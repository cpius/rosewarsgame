//
//  HKGameScene.h
//  RoseWars
//
//  Created by Heine Skov Kristensen on 9/30/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>
#import "GameBoard.h"
#import "GCTurnBasedMatchHelper.h"
#import "LeftPanel.h"
#import "HKDialogNodeProtocol.h"
#import "HKLevelIncreaseDialogProtocol.h"

#define kZoomFactor 2.0
#define CARD_TAG @"CARD_TAG"

@class PlayerIndicator;
@class GameManager;
@class HKImageButton;

@interface HKGameScene : SKScene <GameBoardActionProtocol, GameManagerProtocol, ActionDelegate, LeftPanelProtocol, GCTurnBasedMatchHelperDelegate, HKDialogNodeProtocol, HKLevelIncreaseDialogProtocol> {
    
    GameManager *_gameManager;
    GameBoard *_gameboard;
    
    BOOL _zoomedIn;
    BOOL _isZooming;
    CGPoint _originalPos;
    
    GameBoardNode *_zoomInOnNode;
    CGPoint _zoomPosition;
    
    LeftPanel *_leftPanel;
    PlayerIndicator *_playerIndicator;
    
    SKLabelNode *_actionCountLabel;
    HKImageButton *_backButton;
    
    NSMutableArray *_myCards;
    NSMutableArray *_enemyCards;
    
    GameBoardNode *_showingDetailOfNode;
    
    Action *_actionInQueue;
    NSArray *_pathInQueue;
    GridLocation *_selectedAttackDirection;
    NSDictionary *_attackDirections;
    
    BattlePlan *_battlePlan;
    
    SKSpriteNode*_turnIndicator;
    BOOL _playback;
    BOOL _proceedToEnemyTurn;
    
    NSMutableArray *_cardsInvolvedInPlayback;
    NSMutableArray *_abilitiesInvolvedInPlayback;
}

@end
