//
//  GameBoardNode.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/8/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "cocos2d.h"
#import "CardSprite.h"

@interface GameBoardNode : CCNode {
    
    
}

@property (nonatomic, assign) BOOL hasCard;
@property (nonatomic, strong) GridLocation *locationInGrid;
@property (nonatomic, strong) CardSprite *card;
@property (nonatomic, readonly) CCSprite *nodeSprite;

- (id)initWithSprite:(CCSprite*)sprite;

@end
