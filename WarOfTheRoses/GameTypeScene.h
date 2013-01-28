//
//  GameTypeScene.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "cocos2d.h"
#import "GCTurnBasedMatchHelper.h"

@interface GameTypeScene : CCLayer <GCTurnBasedMatchHelperDelegate> {
    
}

+ (id)scene;

@end
