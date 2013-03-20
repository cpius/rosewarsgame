//
//  CardSprite.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/10/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "cocos2d.h"
#import "Card.h"

#define BONUSSPRITE_TAG  500

@interface CardSprite : CCSprite <RangeAttributeDelegate> {
    
    NSMutableArray *_bonusSprites;
    CCSprite *_cardIndicator;
}

@property (nonatomic, strong) Card *model;

- (id)initWithCard:(Card*)card;

- (void)toggleDetailWithScale:(float)scale;
-(void) completeFlipWithScale:(NSNumber*)scale;

@end
