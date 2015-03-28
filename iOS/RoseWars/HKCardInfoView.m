//
//  HKCardInfoView.m
//  RoseWars
//
//  Created by Heine Kristensen on 26/03/15.
//  Copyright (c) 2015 Heine Skov Kristensen. All rights reserved.
//

#import "HKCardInfoView.h"
#import "Card.h"
#import "HKImageButton.h"

@interface HKCardInfoView()

@property (nonatomic) Card *card;

@end

@implementation HKCardInfoView

- (instancetype)initWithCard:(Card*)card inScene:(SKScene*)scene
{
    self = [super init];
    if (self) {
        self.zPosition = 999;
        
        SKSpriteNode *background = [SKSpriteNode spriteNodeWithImageNamed:@"dialog_frame"];
        background.position = self.position;
        background.zPosition = 1001;
        [self addChild:background];
        
        SKSpriteNode *cardsprite = [SKSpriteNode spriteNodeWithImageNamed:card.frontImageSmall];
        cardsprite.anchorPoint = CGPointMake(1, 0.5);
        [cardsprite setScale:0.85];
        cardsprite.position = CGPointMake((background.size.width / 2) - 30.0, background.position.y + 10);
        [background addChild:cardsprite];
        
        SKLabelNode *classNode = [SKLabelNode labelNodeWithFontNamed:APP_FONT_BOLD];
        classNode.fontSize = 14.0;
        classNode.fontColor =[UIColor blackColor];
        classNode.position = CGPointMake(background.position.x, background.position.y + (background.size.height / 2) - 40);
        classNode.text = card.unitDescriptionName;
        classNode.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        [background addChild:classNode];
        
        SKLabelNode *attackLabel = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        attackLabel.fontSize = 16.0;
        attackLabel.fontColor = [UIColor whiteColor];
        attackLabel.text = [NSString stringWithFormat:@"Attack:\t\t\t%ld", (long)[card.attack calculateValue]];
        attackLabel.position =CGPointMake((-background.size.width / 2.0) + 35.0, (cardsprite.position.y + cardsprite.size.height / 2.0) - 15.0);
        attackLabel.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeLeft;
        [background addChild:attackLabel];

        SKLabelNode *defenseLabel = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        defenseLabel.fontSize = 16.0;
        defenseLabel.fontColor = [UIColor whiteColor];
        defenseLabel.text = [NSString stringWithFormat:@"Defence:\t\t%ld", (long)[card.defence calculateValue]];
        defenseLabel.position =CGPointMake((-background.size.width / 2.0) + 35.0, attackLabel.position.y - 25.0);
        defenseLabel.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeLeft;
        [background addChild:defenseLabel];

        SKLabelNode *experienceLabel = [SKLabelNode labelNodeWithFontNamed:APP_FONT_BOLD];
        experienceLabel.fontSize = 18.0;
        experienceLabel.fontColor = [UIColor whiteColor];
        experienceLabel.text = [NSString stringWithFormat:@"Experience"];
        experienceLabel.position =CGPointMake((-background.size.width / 2.0) + 35.0, defenseLabel.position.y - 30.0);
        experienceLabel.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeLeft;
        [background addChild:experienceLabel];
        
        for (int i = 0; i < card.experience; i++) {
            SKSpriteNode *experienceStar = [SKSpriteNode spriteNodeWithImageNamed:@"bonus"];
            experienceStar.position = CGPointMake(-(background.size.width / 2.0) + 40.0 + (i * (experienceStar.size.width / 1.5)), experienceLabel.position.y - 30.0);
            [experienceStar setScale:0.50];
            [background addChild:experienceStar];
        }

        __block HKCardInfoView *weakSelf = self;
        HKImageButton *dismissButton = [[HKImageButton alloc] initWithImage:@"button" selectedImage:@"button_selected" title:@"Dismiss" block:^(id  sender) {
            [self dismissDialogWithWeakRefToSelf:weakSelf];
        }];

        dismissButton.position = CGPointMake(background.position.x, -(background.size.height / 2) + dismissButton.size.height);
        [background addChild:dismissButton];
    }
    return self;
}

- (void)dismissDialogWithWeakRefToSelf:(HKCardInfoView*)weakSelf {
    weakSelf.scene.userInteractionEnabled = YES;
    
    SKAction *fadeout = [SKAction fadeOutWithDuration:0.2];
    SKAction *dismiss = [SKAction removeFromParent];
    [self runAction:[SKAction sequence:@[fadeout, dismiss]]];
}

@end
