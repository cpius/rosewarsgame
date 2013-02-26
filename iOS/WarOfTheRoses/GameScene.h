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

#define kZoomFactor 2.0
#define kEnemyActionDelayTime 2.0

@interface GameScene : CCLayer <GameBoardActionProtocol, GameManagerProtocol, ActionDelegate, LeftPanelProtocol> {
    
    CGSize _winSize;
    
    GameManager *_gameManager;
    GameBoard *_gameboard;
    
    BOOL _zoomedIn;
    BOOL _isZooming;
    CGPoint _originalPos;
    
    GameBoardNode *_zoomInOnNode;
    CGPoint _zoomPosition;
    
    LeftPanel *_leftPanel;
    
    CCLabelTTF *_actionCountLabel;
    CCSprite *_backButton;
    
    NSMutableArray *_myCards;
    NSMutableArray *_enemyCards;
    
    BOOL _gameover;
    
    GameBoardNode *_showingDetailOfNode;
    
    Action *_actionInQueue;
    BattlePlan *_battlePlan;
    
    CCSprite *_turnIndicator;

}

+ (id)scene;

@end
