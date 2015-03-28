//
//  BonusSprite.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "BonusSprite.h"
#import "HKAttribute.h"

static NSString* const kBonusLabelName = @"bonuslabel";

@implementation BonusSprite

@synthesize bonusText = _bonusText;
@synthesize attribute = _attribute;

- (id)initWithAttribute:(HKAttribute*)attribute {
    
    self = [super initWithImageNamed:@"bonus"];
    
    if (self) {
        _attribute = attribute;
        
        NSUInteger bonusValue = [_attribute getRawBonusValue] + [_attribute getTimedBonusValue];

        [self setBonusText:[NSString stringWithFormat:@"+%lu%@",
                            (unsigned long)bonusValue,
                            _attribute.attributeAbbreviation]];
    }
    
    return self;
}

- (void)setBonusText:(NSString *)bonusText {

    SKLabelNode *bonusLabel = (SKLabelNode*)[self childNodeWithName:kBonusLabelName];
    if (!bonusLabel) {
        bonusLabel = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        bonusLabel.position = self.position;
        bonusLabel.name = kBonusLabelName;
        bonusLabel.fontSize = 14.0;
        bonusLabel.fontColor = [UIColor blackColor];
        bonusLabel.verticalAlignmentMode = SKLabelVerticalAlignmentModeCenter;
        bonusLabel.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        [self addChild:bonusLabel];
    }
    
    bonusLabel.text = bonusText;
}

@end
