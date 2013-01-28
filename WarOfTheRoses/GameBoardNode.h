//
//  GameBoardNode.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/8/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "cocos2d.h"
#import "Card.h"

@interface GameBoardNode : CCNode {
    
    CCSprite *_sprite;
}

@property (nonatomic, assign) BOOL hasCard;
@property (nonatomic, assign) GridLocation locationInGrid;
@property (nonatomic, strong) Card *card;

- (id)initWithSprite:(CCSprite*)sprite;

@end
