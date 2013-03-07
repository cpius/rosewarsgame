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

#define RANGED_ATTACK_TAG    10
#define ATTACK_DIRECTION_TAG 11
#define MELEE_ATTACK_TAG     12

typedef enum {
    
    kHighlightTypeNone,
    kHighlightTypeAttackDirection,
    kHighlightTypeRangedTarget,
    kHighlightTypeMeleeTarget
} HighlightTypes;

@interface GameBoardNode : CCNode {
    
    
}

@property (nonatomic, readonly) HighlightTypes highlightedAs;
@property (nonatomic, assign) BOOL hasCard;
@property (nonatomic, strong) GridLocation *locationInGrid;
@property (nonatomic, strong) CardSprite *card;
@property (nonatomic, readonly) CCSprite *nodeSprite;

- (id)initWithSprite:(CCSprite*)sprite;

- (void)focusType:(HighlightTypes)highlightType;
- (void)unFocusType:(HighlightTypes)highlightType;

- (void)highlightForType:(HighlightTypes)highlightType;
- (void)highlightCardForType:(HighlightTypes)highlightType;
- (void)deHighlight;

@end
