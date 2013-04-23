//
//  GameScene.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "GameManager.h"
#import "GameBoard.h"
#import "LeftPanel.h"
#import "GCTurnBasedMatchHelper.h"
#import "PlayerIndicator.h"

#define kZoomFactor 2.0

#define CARD_TAG 666

@interface GameScene : CCLayer <GameBoardActionProtocol, GameManagerProtocol, ActionDelegate, LeftPanelProtocol, GCTurnBasedMatchHelperDelegate> {
    
    CGSize _winSize;
    
    GameManager *_gameManager;
    GameBoard *_gameboard;
    
    BOOL _zoomedIn;
    BOOL _isZooming;
    CGPoint _originalPos;
    
    GameBoardNode *_zoomInOnNode;
    CGPoint _zoomPosition;
    
    LeftPanel *_leftPanel;
    PlayerIndicator *_playerIndicator;
    
    CCLabelTTF *_actionCountLabel;
    CCSprite *_backButton;
    
    NSMutableArray *_myCards;
    NSMutableArray *_enemyCards;
    
    GameBoardNode *_showingDetailOfNode;
    
    Action *_actionInQueue;
    NSArray *_pathInQueue;
    GridLocation *_selectedAttackDirection;
    NSDictionary *_attackDirections;
    
    BattlePlan *_battlePlan;
    
    CCSprite *_turnIndicator;
    BOOL _playback;
    
    NSMutableArray *_cardsInvolvedInPlayback;
    NSMutableArray *_abilitiesInvolvedInPlayback;

}

+ (id)scene;

@end
