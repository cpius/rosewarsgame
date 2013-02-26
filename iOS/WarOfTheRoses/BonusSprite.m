//
//  BonusSprite.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "BonusSprite.h"


@implementation BonusSprite

@synthesize bonusText = _bonusText;
@synthesize attribute = _attribute;

- (id)initWithAttribute:(RangeAttribute *)attribute {
    
    self = [super initWithFile:@"bonus.png"];
    
    if (self) {
        _attribute = attribute;
        
        NSUInteger bonusValue = [_attribute getRawBonusValue] + [_attribute getTimedBonusValue];

        [self setBonusText:[NSString stringWithFormat:@"+%d%@",
                            bonusValue,
                            _attribute.attributeAbbreviation]];
    }
    
    return self;
}

- (void)setBonusText:(NSString *)bonusText {
    
    [self removeAllChildrenWithCleanup:YES];
    
    CCLabelTTF *bonusLabel = [CCLabelTTF labelWithString:bonusText fontName:APP_FONT fontSize:10.0];
    
    [self addChild:bonusLabel];
    
    bonusLabel.color = ccc3(0, 0, 0);
    bonusLabel.anchorPoint = ccp(0.5, 0.5);
    bonusLabel.position = ccp(self.contentSize.width / 2, self.contentSize.height / 2);
}

@end
