//
//  Card.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "Card.h"
#import "BonusSprite.h"

@implementation Card

@synthesize frontImageSmall = _frontImageSmall;
@synthesize frontImageLarge = _frontImageLarge;
@synthesize backImage = _backImage;
@synthesize cardColor = _cardColor;
@synthesize cardLocation = _cardLocation;
@synthesize isShowingDetail;
@synthesize attack = _attack, defence = _defence;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        _cardColor = kCardColorGreen;
        self.isShowingDetail = NO;
        
    }
    
    return self;
}

- (void)commonInit {
    
    self.attack.delegate = self;
    self.attack.attributeAbbreviation = @"A";
    
    self.defence.delegate = self;
    self.defence.attributeAbbreviation = @"D";
    
    [self setDisplayFrame:[[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:self.frontImageSmall]];
}

- (NSString *)description {
    
    NSString *description = [NSString stringWithFormat:@"CardType: %d - UnitType: %d - UnitName: %d - Boardlocation: row %d column %d",
                             self.cardType,
                             self.unitType,
                             self.unitName,
                             self.cardLocation.row,
                             self.cardLocation.column];
    
    return description;
}

- (void)rangeAttribute:(RangeAttribute *)attribute addedTimedBonus:(TimedBonus *)timedBonus {
    
    CCLOG(@"Card: %@ added timed bonus: %@", self, timedBonus);
    
    BonusSprite *bonusSprite = [[BonusSprite alloc] initWithBonusText:[NSString stringWithFormat:@"+%d%@",
                                                                      timedBonus.bonusValue,
                                                                      attribute.attributeAbbreviation]];
    
    bonusSprite.anchorPoint = ccp(0, 0);
    bonusSprite.position = ccp(0.0, self.contentSize.height - bonusSprite.contentSize.height);
    [self addChild:bonusSprite];
    
    CCScaleTo *scaleup = [CCScaleTo actionWithDuration:0.2 scale:1.5];
    CCScaleTo *scaledown = [CCScaleTo actionWithDuration:0.2 scale:1.0];
    
    [bonusSprite runAction:[CCSequence actions:scaleup, scaledown, nil]];
}

- (void)rangeAttribute:(RangeAttribute *)attribute removedTimedBonus:(TimedBonus *)timedBonus {
    
    CCLOG(@"Card: %@ removed timed bonus: %@", self, timedBonus);
}

// Must be overloaded in subclasses
- (BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return NO;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
}

-(void) completeFlipWithScale:(NSNumber*)scale
{
    CCAction* restoreWidthAction;

    if (!self.isShowingDetail) {
        
        CCSpriteFrame *frame = [[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:self.frontImageSmall];
        [self setDisplayFrame:frame];
        self.contentSize = CGSizeMake(frame.rect.size.width, frame.rect.size.height);
        restoreWidthAction = [CCScaleTo actionWithDuration:.25f scaleX:scale.floatValue scaleY:scale.floatValue];

        [self setZOrder:0];
    }
    else {
        CCSpriteFrame *frame = [[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:self.frontImageLarge];
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
    
    self.isShowingDetail = !self.isShowingDetail;

    CCAction* scaleXAction = [CCScaleTo   actionWithDuration:.25f scaleX:0.03f scaleY:self.scaleY];
    CCAction* skewAction = [CCSkewBy    actionWithDuration:.25f skewX:0.0f skewY:20.0f];
    CCAction* waitAction     = [CCDelayTime actionWithDuration:.25f];
    CCAction* callCompleteFuncAction = [CCCallFuncO actionWithTarget:self selector:@selector(completeFlipWithScale:) object:@(scale)];
    CCAction* completeFlipAction = [CCSequence actions:(CCFiniteTimeAction*)waitAction, callCompleteFuncAction, nil];
    CCAction* flipActions1 = [CCSpawn actions:(CCFiniteTimeAction*)scaleXAction, skewAction, completeFlipAction, nil];
    [self runAction:flipActions1];
    
}

@end
