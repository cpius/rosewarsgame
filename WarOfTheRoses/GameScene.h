//
//  GameScene.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Game.h"
#import "GameBoard.h"

#define kZoomFactor 2.0

@interface GameScene : CCLayer {
    
    Game *_currentGame;
    GameBoard *_gameboard;
    
    BOOL _zoomedIn;
    BOOL _isZooming;
    CGPoint _originalPos;
    
    GameBoardNode *_zoomInOnNode;
    CGPoint _zoomPosition;
    GameBoardNode *_activeNode;
}

+ (id)scene;

@end
