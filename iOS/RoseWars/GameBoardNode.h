//
//  GameBoardNode.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/8/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <SpriteKit/SpriteKit.h>
#import "CardSprite.h"

#define HIGHLIGHT_TAG         @"HIGHLIGHT"
#define RANGED_ATTACK_TAG    10
#define ATTACK_DIRECTION_TAG @"ATTACKDIRECTION"
#define MELEE_ATTACK_TAG     12

typedef enum {
    
    kHighlightTypeNone,
    kHighlightTypeAttackDirection,
    kHighlightTypeRangedTarget,
    kHighlightTypeMeleeTarget
} HighlightTypes;

@interface GameBoardNode : SKSpriteNode {
    
    
}

@property (nonatomic, readonly) HighlightTypes highlightedAs;
@property (nonatomic, readonly) BOOL hasCard;
@property (nonatomic, strong) GridLocation *locationInGrid;
@property (nonatomic, strong) CardSprite *card;

- (id)initWithSprite:(NSString*)sprite;

- (void)focusType:(HighlightTypes)highlightType;
- (void)unFocusType:(HighlightTypes)highlightType;

- (void)highlightForType:(HighlightTypes)highlightType;
- (void)highlightCardForType:(HighlightTypes)highlightType;
- (void)deHighlight;

@end
