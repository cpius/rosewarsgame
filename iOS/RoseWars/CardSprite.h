//
//  CardSprite.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/10/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Card.h"

#define BONUSSPRITE_TAG  @"BonusSprite"
#define COLOR_INDICATOR_TAG @"ColorIndicator"

@interface CardSprite : SKNode <RangeAttributeDelegate> {
    
    NSMutableArray *_bonusSprites;
    SKSpriteNode *_cardIndicator;
}

@property (nonatomic, strong) Card *model;

- (id)initWithCard:(Card*)card;

- (void)toggleDetailWithScale:(float)scale;

- (void)setColor:(SKColor*)color;

@end
