//
//  CardSprite.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/10/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "CardSprite.h"
#import "BonusSprite.h"

@interface CardSprite()

- (void)addBonusSprite:(RangeAttribute*)rangeAttribute bonusValue:(NSUInteger)bonusValue animated:(BOOL)animated;
- (void)updateBonusSprite:(RangeAttribute*)rangeAttribute;

@end

@implementation CardSprite

@synthesize model = _model;

- (id)initWithCard:(Card*)card {
    
    self = [super init];
    
    if (self) {
        
        _model = card;
        
        _model.attack.delegate = self;
        _model.defence.delegate = self;
        
        [self setDisplayFrame:[[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:_model.frontImageSmall]];
        
        [self updateBonusSprite:_model.attack];
        [self updateBonusSprite:_model.defence];
        
    }
    
    return self;
}

- (void)draw {
    
    [super draw];
    
    if (_model.cardColor == kCardColorGreen) {
        ccDrawColor4B(0, 235, 0, 255);
        ccDrawCircle(ccp(self.contentSize.width - 15, self.contentSize.height - 15), 5, 0, 10, NO);
    }
    else {
        ccDrawColor4B(235, 0, 0, 255);
        ccDrawCircle(ccp(self.contentSize.width - 15, self.contentSize.height - 15), 5, 0, 10, NO);
    }
}

- (void)rangeAttribute:(RangeAttribute *)attribute addedRawBonus:(RawBonus *)rawBonus {
    
    CCLOG(@"Card: %@ added raw bonus: %@", self.model, rawBonus);
    
    [self addBonusSprite:attribute bonusValue:rawBonus.bonusValue animated:YES];
}

- (void)rangeAttribute:(RangeAttribute *)attribute removedRawBonus:(RawBonus *)rawBonus {
    
    CCLOG(@"Card: %@ removed raw bonus: %@", self.model, rawBonus);
}

- (void)rangeAttribute:(RangeAttribute *)attribute addedTimedBonus:(TimedBonus *)timedBonus {
    
    CCLOG(@"Card: %@ added timed bonus: %@", self.model, timedBonus);
    
    [self addBonusSprite:attribute bonusValue:timedBonus.bonusValue animated:YES];
}

- (void)rangeAttribute:(RangeAttribute *)attribute removedTimedBonus:(TimedBonus *)timedBonus {
    
    CCLOG(@"Card: %@ removed timed bonus: %@", self.model, timedBonus);
}

- (void)updateBonusSprite:(RangeAttribute *)rangeAttribute {
    
    NSUInteger bonusValue = [rangeAttribute getRawBonusValue] + [rangeAttribute getTimedBonusValue];
    
    if (bonusValue != 0) {
        BonusSprite *bonusSprite = (BonusSprite*)[self getChildByTag:BONUSSPRITE_TAG];
        
        if (bonusSprite != nil) {
            [bonusSprite setBonusText:[NSString stringWithFormat:@"+%d%@",
                                       bonusValue,
                                       rangeAttribute.attributeAbbreviation]];
        }
        else {
            [self addBonusSprite:rangeAttribute bonusValue:bonusValue animated:NO];
        }
    }
}

- (void)addBonusSprite:(RangeAttribute*)rangeAttribute bonusValue:(NSUInteger)bonusValue animated:(BOOL)animated {
    
    BonusSprite *bonusSprite = [[BonusSprite alloc] initWithBonusText:[NSString stringWithFormat:@"+%d%@",
                                                                       bonusValue,
                                                                       rangeAttribute.attributeAbbreviation]];
    
    bonusSprite.tag = BONUSSPRITE_TAG;
    bonusSprite.anchorPoint = ccp(0, 0);
    bonusSprite.position = ccp(0.0, self.contentSize.height - bonusSprite.contentSize.height);
    [self addChild:bonusSprite];
    
    if (animated) {
        CCScaleTo *scaleup = [CCScaleTo actionWithDuration:0.2 scale:1.5];
        CCScaleTo *scaledown = [CCScaleTo actionWithDuration:0.2 scale:1.0];
        
        [bonusSprite runAction:[CCSequence actions:scaleup, scaledown, nil]];
    }
}


-(void) completeFlipWithScale:(NSNumber*)scale
{
    CCAction* restoreWidthAction;
    
    if (!_model.isShowingDetail) {
        
        CCSpriteFrame *frame = [[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:_model.frontImageSmall];
        [self setDisplayFrame:frame];
        self.contentSize = CGSizeMake(frame.rect.size.width, frame.rect.size.height);
        restoreWidthAction = [CCScaleTo actionWithDuration:.25f scaleX:scale.floatValue scaleY:scale.floatValue];
        
        [self setZOrder:0];
    }
    else {
        CCSpriteFrame *frame = [[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:_model.frontImageLarge];
        [self setDisplayFrame:frame];
        
        self.contentSize = CGSizeMake(frame.rect.size.width, frame.rect.size.height);
        restoreWidthAction = [CCScaleTo actionWithDuration:.25f scaleX:1.0f scaleY:1.0f];
        
        [self setZOrder:100];
    }
    
    CCAction* unskewAction = [CCSkewBy actionWithDuration:.25f skewX:0.0f skewY:-20.0f];
    CCAction* flipActions2 = [CCSpawn actions:(CCFiniteTimeAction*)restoreWidthAction, unskewAction, nil];
    [self runAction:flipActions2];
}

- (void)toggleDetailWithScale:(float)scale {
    
    _model.isShowingDetail = !_model.isShowingDetail;
    
    CCAction* scaleXAction = [CCScaleTo   actionWithDuration:.25f scaleX:0.03f scaleY:self.scaleY];
    CCAction* skewAction = [CCSkewBy    actionWithDuration:.25f skewX:0.0f skewY:20.0f];
    CCAction* waitAction     = [CCDelayTime actionWithDuration:.25f];
    CCAction* callCompleteFuncAction = [CCCallFuncO actionWithTarget:self selector:@selector(completeFlipWithScale:) object:@(scale)];
    CCAction* completeFlipAction = [CCSequence actions:(CCFiniteTimeAction*)waitAction, callCompleteFuncAction, nil];
    CCAction* flipActions1 = [CCSpawn actions:(CCFiniteTimeAction*)scaleXAction, skewAction, completeFlipAction, nil];
    [self runAction:flipActions1];
    
}

@end
