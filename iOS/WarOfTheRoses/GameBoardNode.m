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
@synthesize nodeSprite = _nodeSprite;
@synthesize highlightedAs = _highlightedAs;

- (id)initWithSprite:(CCSprite *)sprite {
    
    self = [super init];
    
    if (self) {
        
        self.anchorPoint = ccp(0.5, 0.5);
        
        self.contentSize = CGSizeMake(64, 87);
        
        _nodeSprite = sprite;
        
        _nodeSprite.position = ccp(self.contentSize.width / 2, self.contentSize.height / 2);
        
        [self addChild:_nodeSprite];
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
        CCSprite *attackdirection = (CCSprite*)[self.nodeSprite getChildByTag:ATTACK_DIRECTION_TAG];
        if (attackdirection) {
            [attackdirection removeFromParentAndCleanup:YES];
        }
    }

    if (_highlightedAs == kHighlightTypeRangedTarget) {
        CCSprite *crosshair = (CCSprite*)[self.card getChildByTag:RANGED_ATTACK_TAG];
        if (crosshair) {
            [crosshair removeFromParentAndCleanup:YES];
        }
    }
    
    if (_highlightedAs == kHighlightTypeMeleeTarget) {
        CCSprite *swordClash = (CCSprite*)[self.card getChildByTag:MELEE_ATTACK_TAG];
        if (swordClash) {
            [swordClash removeFromParentAndCleanup:YES];
        }
    }
    
    _highlightedAs = kHighlightTypeNone;
}

- (void)focusType:(HighlightTypes)highlightType {
    
    if (highlightType == kHighlightTypeAttackDirection) {
        CCSprite *attackdirection = (CCSprite*)[self.nodeSprite getChildByTag:ATTACK_DIRECTION_TAG];
        if (attackdirection) {
            [attackdirection runAction:[CCScaleTo actionWithDuration:0.2 scale:0.6]];
        }
    }
}

- (void)unFocusType:(HighlightTypes)highlightType {
    
    if (highlightType == kHighlightTypeAttackDirection) {
        CCSprite *attackdirection = (CCSprite*)[self.nodeSprite getChildByTag:ATTACK_DIRECTION_TAG];
        if (attackdirection) {
            [attackdirection runAction:[CCScaleTo actionWithDuration:0.2 scale:0.4]];
        }
    }
}

- (void)highlightCardForType:(HighlightTypes)highlightType {
    
    _highlightedAs = highlightType;
    
    if (highlightType == kHighlightTypeRangedTarget) {
        CCSprite *crosshair = [CCSprite spriteWithFile:@"crosshair.png"];
        crosshair.scale = self.card.scaleX;
        crosshair.anchorPoint = ccp(0.5, 0.5);
        crosshair.position = ccp(self.card.contentSize.width / 2, self.card.contentSize.height / 2);
        [self.card addChild:crosshair z:10 tag:RANGED_ATTACK_TAG];
        [crosshair runAction:[CCRepeatForever actionWithAction:
                              [CCSequence actions:[CCScaleTo actionWithDuration:0.2 scale:1.2],
                               [CCScaleTo actionWithDuration:0.2 scale:1.0],
                               nil]]];
    }
    
    else if (highlightType == kHighlightTypeMeleeTarget) {
        CCSprite *swordClash = [CCSprite spriteWithFile:@"swordclash.png"];
        swordClash.scale = self.card.scaleX;
        swordClash.anchorPoint = ccp(0.5, 0.5);
        swordClash.position = ccp(self.card.contentSize.width / 2, self.card.contentSize.height / 2);
        [self.card addChild:swordClash z:10 tag:MELEE_ATTACK_TAG];
        [swordClash runAction:[CCRepeatForever actionWithAction:
                               [CCSequence actions:[CCScaleTo actionWithDuration:0.2 scale:1.2],
                                [CCScaleTo actionWithDuration:0.2 scale:1.0],
                                nil]]];
    }
}

- (void)highlightForType:(HighlightTypes)highlightType {

    if (highlightType == kHighlightTypeAttackDirection) {
        CCSprite *attackDirection = [CCSprite spriteWithFile:@"attack_direction.png"];
        attackDirection.scale = 0.40;
        attackDirection.anchorPoint = ccp(0.5, 0.5);
        attackDirection.position = ccp(self.nodeSprite.contentSize.width / 2, self.nodeSprite.contentSize.height / 2);
        [self.nodeSprite addChild:attackDirection z:10 tag:ATTACK_DIRECTION_TAG];
    }
    
    _highlightedAs = highlightType;
}

@end
