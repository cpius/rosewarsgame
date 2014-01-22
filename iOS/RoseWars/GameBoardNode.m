//
//  GameBoardNode.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/8/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameBoardNode.h"


@implementation GameBoardNode

@synthesize hasCard, card = _card;
@synthesize highlightedAs = _highlightedAs;

- (id)initWithSprite:(NSString *)sprite {
    
    self = [super initWithImageNamed:sprite];
    
    if (self) {
        
        self.size = CGSizeMake(64, 87);
    }
    
    return self;
}

- (BOOL)hasCard {
    
    return _card != nil;
}

-(NSString *)description {
    
    return [NSString stringWithFormat:@"Location in grid: row: %d column: %d",
            self.locationInGrid.row,
            self.locationInGrid.column];
}

- (void)deHighlight {
    
    if (_highlightedAs == kHighlightTypeAttackDirection) {
        SKSpriteNode *attackdirection = (SKSpriteNode*)[self childNodeWithName:ATTACK_DIRECTION_TAG];
        if (attackdirection) {
            [attackdirection removeFromParent];
        }
    }

    [self enumerateChildNodesWithName:HIGHLIGHT_TAG usingBlock:^(SKNode *node, BOOL *stop) {
       
        [node removeFromParent];
    }];
    
    if (self.card != nil) {
        [self.card enumerateChildNodesWithName:HIGHLIGHT_TAG usingBlock:^(SKNode *node, BOOL *stop) {
            [node removeFromParent];
        }];
    }
    
    _highlightedAs = kHighlightTypeNone;
}

- (void)focusType:(HighlightTypes)highlightType {
    
    if (highlightType == kHighlightTypeAttackDirection) {
        [self enumerateChildNodesWithName:ATTACK_DIRECTION_TAG usingBlock:^(SKNode *node, BOOL *stop) {
            [node runAction:[SKAction scaleTo:0.6 duration:0.2f]];
        }];
    }
}

- (void)unFocusType:(HighlightTypes)highlightType {
    
    if (highlightType == kHighlightTypeAttackDirection) {
        [self enumerateChildNodesWithName:ATTACK_DIRECTION_TAG usingBlock:^(SKNode *node, BOOL *stop) {
            [node runAction:[SKAction scaleTo:0.4 duration:0.2f]];
        }];
    }
}

- (void)highlightCardForType:(HighlightTypes)highlightType {
    
    _highlightedAs = highlightType;
    
    if (highlightType == kHighlightTypeRangedTarget) {
        SKSpriteNode *crosshair = [SKSpriteNode spriteNodeWithImageNamed:@"crosshair.png"];
        crosshair.position = ccp(0,0);
        [crosshair setScale:0.2f];
        crosshair.name = HIGHLIGHT_TAG;
        crosshair.zPosition = kOverlayZOrder;
        [self addChild:crosshair];
        
        [crosshair runAction:[SKAction repeatActionForever:[SKAction sequence:@[[SKAction scaleTo:0.4 duration:0.2], [SKAction scaleTo:0.2 duration:0.2]]]]];
    }
    
    else if (highlightType == kHighlightTypeMeleeTarget) {
        SKSpriteNode *swordClash = [SKSpriteNode spriteNodeWithImageNamed:@"swordclash.png"];
        swordClash.scale = 0.5;
        swordClash.position = CGPointMake(0, 0);
        swordClash.zPosition = kOverlayZOrder;
        swordClash.name = HIGHLIGHT_TAG;
        [self.card addChild:swordClash];

        [swordClash runAction:[SKAction repeatActionForever:[SKAction sequence:@[[SKAction scaleTo:1.2 duration:0.2], [SKAction scaleTo:1.0 duration:0.2]]]]];
    }
}

- (void)highlightForType:(HighlightTypes)highlightType {

    if (highlightType == kHighlightTypeAttackDirection) {
        SKSpriteNode *attackDirection = [SKSpriteNode spriteNodeWithImageNamed:@"attack_direction.png"];
        attackDirection.scale = 0.40;
        attackDirection.position = CGPointMake(0, 0);
        attackDirection.zPosition = kOverlayZOrder;
        attackDirection.name = ATTACK_DIRECTION_TAG;
        [self addChild:attackDirection];
    }
    
    _highlightedAs = highlightType;
}

@end
