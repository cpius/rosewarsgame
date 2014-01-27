//
//  CardSprite.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/10/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "CardSprite.h"
#import "BonusSprite.h"
#import "SKSpriteNode+NodePosition.h"

@interface CardSprite() {
    
    SKSpriteNode *_cardImageNode;
}

- (void)addBonusSprite:(RangeAttribute*)rangeAttribute bonusValue:(NSUInteger)bonusValue animated:(BOOL)animated;
- (void)updateBonusSprite:(BonusSprite*)bonusSprite;
- (void)updateBonusSpriteForAttribute:(RangeAttribute*)rangeAttribute;
- (void)updateAllBonusSprites;
- (void)updateSpritePositions;
- (BonusSprite*)getBonusSpriteForAttribute:(RangeAttribute*)attribute;

- (void)setCardColorIndicator;

@end

@implementation CardSprite

@synthesize model = _model;

- (id)initWithCard:(Card*)card {
    
    self = [super init];
    
    if (self) {
        
        _cardImageNode = [SKSpriteNode spriteNodeWithImageNamed:card.frontImageSmall];
        _cardImageNode.position = self.position;
        [self addChild:_cardImageNode];
        
        _model = card;
        
        _bonusSprites = [NSMutableArray array];
        
        _model.attack.delegate = self;
        _model.defence.delegate = self;
                
        [self updateBonusSpriteForAttribute:_model.attack];
        [self updateBonusSpriteForAttribute:_model.defence];

        [self setCardColorIndicator];
        
        [_model addObserver:self forKeyPath:@"cardColor" options:NSKeyValueObservingOptionNew context:nil];
    }
    
    return self;
}

- (void)dealloc {
    
    [_model removeObserver:self forKeyPath:@"cardColor"];
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    
    NSLog(@"Card: %@ changed color to %d", self, _model.cardColor);
    
    if ([keyPath isEqualToString:@"cardColor"]) {
        [self setCardColorIndicator];
    }
}

- (void)setColor:(UIColor *)color {
    
    _cardImageNode.color = color;
    _cardImageNode.colorBlendFactor = 0.5;
}

- (CGSize)size {
    
    return _cardImageNode.size;
}

- (void)setCardColorIndicator {
    
    SKNode *colorIndicator = [self childNodeWithName:COLOR_INDICATOR_TAG];
    
    if (colorIndicator) {
        [colorIndicator removeFromParent];
    }
    
    if (_model.cardColor == kCardColorGreen) {
        _cardIndicator = [SKSpriteNode spriteNodeWithImageNamed:@"green_cardindicator.png"];
    }
    else {
        _cardIndicator = [SKSpriteNode spriteNodeWithImageNamed:@"red_cardindicator.png"];
    }
    
    _cardIndicator.position = [_cardImageNode positionForChildNode:_cardIndicator position:kNodePositionUpperRight insets:UIEdgeInsetsMake(10, 0, 0, 10)];
    _cardIndicator.name = COLOR_INDICATOR_TAG;

    [self addChild:_cardIndicator];
}

- (void)rangeAttribute:(RangeAttribute *)attribute addedRawBonus:(RawBonus *)rawBonus {
    
    NSLog(@"Card: %@ added raw bonus: %@", self.model, rawBonus);
    
    [self addBonusSprite:attribute bonusValue:rawBonus.bonusValue animated:YES];
}

- (void)rangeAttribute:(RangeAttribute *)attribute removedRawBonus:(RawBonus *)rawBonus {
    
    NSLog(@"Card: %@ removed raw bonus: %@", self.model, rawBonus);
    
    [self updateBonusSpriteForAttribute:attribute];
}

- (void)rangeAttribute:(RangeAttribute *)attribute addedTimedBonus:(TimedBonus *)timedBonus {
    
    NSLog(@"Card: %@ added timed bonus: %@", self.model, timedBonus);
    
    [self addBonusSprite:attribute bonusValue:timedBonus.bonusValue animated:YES];
}

- (void)rangeAttribute:(RangeAttribute *)attribute removedTimedBonus:(TimedBonus *)timedBonus {
    
    NSLog(@"Card: %@ removed timed bonus: %@", self.model, timedBonus);

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
        [bonusSprite removeFromParent];
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
        
        bonusSprite.name = BONUSSPRITE_TAG;
        bonusSprite.position = [_cardImageNode positionForChildNode:bonusSprite position:kNodePositionUpperLeft insets:UIEdgeInsetsMake(bonusSprite.size.height * _bonusSprites.count, 0, 0, 0)];
        [self addChild:bonusSprite];

        [_bonusSprites addObject:bonusSprite];
        
        if (animated) {
            SKAction *scaleup = [SKAction scaleTo:1.5 duration:0.2];
            SKAction *scaledown = [SKAction scaleTo:1.0 duration:0.2];

            [bonusSprite runAction:[SKAction sequence:@[scaleup, scaledown]]];
        }
    }
}

- (void)updateSpritePositions {
    
    NSUInteger counter = 0;
    
    for (BonusSprite *bonusSprite in _bonusSprites) {
        bonusSprite.position = [_cardImageNode positionForChildNode:bonusSprite position:kNodePositionUpperLeft insets:UIEdgeInsetsMake(bonusSprite.size.height * counter, 0, 0, 0)];
        counter++;
    }
    
    _cardIndicator.position = [_cardImageNode positionForChildNode:_cardIndicator position:kNodePositionUpperRight insets:UIEdgeInsetsMake(10, 0, 0, 10)];
}

- (void)toggleDetailWithScale:(float)scale {
    
    
    _model.isShowingDetail = !_model.isShowingDetail;
    
    SKAction *textureAction;
    SKAction *scaleAction = [SKAction scaleTo:scale duration:0.2f];
    SKAction *zPositionAction = [SKAction runBlock:^{
       
        if (_model.isShowingDetail) {
            self.zPosition = kCardSpriteDetailZOrder;
        }
        else {
            self.zPosition = kCardSpriteZOrder;
        }
    }];

    if (_model.isShowingDetail) {
        textureAction = [SKAction setTexture:[SKTexture textureWithImageNamed:_model.frontImageLarge]];
    }
    else {
        textureAction = [SKAction setTexture:[SKTexture textureWithImageNamed:_model.frontImageSmall]];
    }
    
    [self runAction:[SKAction group:@[zPositionAction, textureAction, scaleAction]]];
}

@end
