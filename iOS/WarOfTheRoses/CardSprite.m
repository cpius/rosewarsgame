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
- (void)updateBonusSprite:(BonusSprite*)bonusSprite;
- (void)updateBonusSpriteForAttribute:(RangeAttribute*)rangeAttribute;
- (void)updateAllBonusSprites;
- (void)updateSpritePositions;
- (BonusSprite*)getBonusSpriteForAttribute:(RangeAttribute*)attribute;

@end

@implementation CardSprite

@synthesize model = _model;

- (id)initWithCard:(Card*)card {
    
    self = [super init];
    
    if (self) {
        
        _model = card;
        
        _bonusSprites = [NSMutableArray array];
        
        _model.attack.delegate = self;
        _model.defence.delegate = self;
        
        [self setDisplayFrame:[[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:_model.frontImageSmall]];
        
        [self updateBonusSpriteForAttribute:_model.attack];
        [self updateBonusSpriteForAttribute:_model.defence];

        if (_model.cardColor == kCardColorGreen) {
            _cardIndicator = [CCSprite spriteWithFile:@"green_cardindicator.png"];
        }
        else {
            _cardIndicator = [CCSprite spriteWithFile:@"red_cardindicator.png"];
        }
        
        _cardIndicator.position = ccp(self.contentSize.width - 15, self.contentSize.height - 15);
        [self addChild:_cardIndicator];
    }
    
    return self;
}

- (void)rangeAttribute:(RangeAttribute *)attribute addedRawBonus:(RawBonus *)rawBonus {
    
    CCLOG(@"Card: %@ added raw bonus: %@", self.model, rawBonus);
    
    [self addBonusSprite:attribute bonusValue:rawBonus.bonusValue animated:YES];
}

- (void)rangeAttribute:(RangeAttribute *)attribute removedRawBonus:(RawBonus *)rawBonus {
    
    CCLOG(@"Card: %@ removed raw bonus: %@", self.model, rawBonus);
    
    [self updateBonusSpriteForAttribute:attribute];
}

- (void)rangeAttribute:(RangeAttribute *)attribute addedTimedBonus:(TimedBonus *)timedBonus {
    
    CCLOG(@"Card: %@ added timed bonus: %@", self.model, timedBonus);
    
    [self addBonusSprite:attribute bonusValue:timedBonus.bonusValue animated:YES];
}

- (void)rangeAttribute:(RangeAttribute *)attribute removedTimedBonus:(TimedBonus *)timedBonus {
    
    CCLOG(@"Card: %@ removed timed bonus: %@", self.model, timedBonus);

    [self updateBonusSpriteForAttribute:attribute];
}

- (BonusSprite *)getBonusSpriteForAttribute:(RangeAttribute *)attribute {
    
    for (BonusSprite* bonusSprite in _bonusSprites) {
        if (bonusSprite.attribute == attribute) {
            return bonusSprite;
        }
    }
    
    return nil;
}

- (void)updateAllBonusSprites {
    
    for (BonusSprite *bonusSprite in _bonusSprites) {
        [self updateBonusSprite:bonusSprite];
    }
}

- (void)updateBonusSpriteForAttribute:(RangeAttribute *)rangeAttribute {
    
    BonusSprite *bonusSprite = [self getBonusSpriteForAttribute:rangeAttribute];
    
    if (bonusSprite == nil) {
        NSUInteger bonusValue = [rangeAttribute getRawBonusValue] + [rangeAttribute getTimedBonusValue];
        
        if (bonusValue > 0) {
            [self addBonusSprite:rangeAttribute bonusValue:bonusValue animated:YES];
        }
    }
    else {
        [self updateBonusSprite:bonusSprite];
    }
}

- (void)updateBonusSprite:(BonusSprite *)bonusSprite {
    
    NSUInteger bonusValue = [bonusSprite.attribute getRawBonusValue] + [bonusSprite.attribute getTimedBonusValue];
    
    if (bonusValue != 0) {
        [bonusSprite setBonusText:[NSString stringWithFormat:@"+%d%@",
                                   bonusValue,
                                   bonusSprite.attribute.attributeAbbreviation]];
    }
    else {
        [bonusSprite removeFromParentAndCleanup:YES];
        [_bonusSprites removeObject:bonusSprite];
    }
}

- (void)addBonusSprite:(RangeAttribute*)rangeAttribute bonusValue:(NSUInteger)bonusValue animated:(BOOL)animated {
    
    BonusSprite *bonusSprite = [self getBonusSpriteForAttribute:rangeAttribute];
    
    if (bonusSprite != nil) {
        [self updateBonusSprite:bonusSprite];
    }
    else {
        BonusSprite *bonusSprite = [[BonusSprite alloc] initWithAttribute:rangeAttribute];
        
        bonusSprite.tag = BONUSSPRITE_TAG;
        bonusSprite.anchorPoint = ccp(0, 0);
        bonusSprite.position = ccp(0.0, self.contentSize.height - ((bonusSprite.contentSize.height + 5) * (_bonusSprites.count + 1)));
        [self addChild:bonusSprite];

        [_bonusSprites addObject:bonusSprite];
        
        if (animated) {
            CCScaleTo *scaleup = [CCScaleTo actionWithDuration:0.2 scale:1.5];
            CCScaleTo *scaledown = [CCScaleTo actionWithDuration:0.2 scale:1.0];
            
            [bonusSprite runAction:[CCSequence actions:scaleup, scaledown, nil]];
        }
    }
}

- (void)updateSpritePositions {
    
    NSUInteger counter = 1;
    
    for (BonusSprite *bonusSprite in _bonusSprites) {
        bonusSprite.position = ccp(0.0, self.contentSize.height - ((bonusSprite.contentSize.height + 5) * counter));
        counter++;
    }
    
    _cardIndicator.position = ccp(self.contentSize.width - 15, self.contentSize.height - 15);
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
        
        [self setZOrder:1000];
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
    CCAction* repositionBonusSprites = [CCCallFunc actionWithTarget:self selector:@selector(updateSpritePositions)];
    CCAction* completeFlipAction = [CCSequence actions:(CCFiniteTimeAction*)waitAction, callCompleteFuncAction, repositionBonusSprites, nil];
    CCAction* flipActions1 = [CCSpawn actions:(CCFiniteTimeAction*)scaleXAction, skewAction, completeFlipAction, nil];
    [self runAction:flipActions1];
    
}

@end
