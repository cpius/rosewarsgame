//
//  HKLevelIncreaseDialog.m
//  RoseWars
//
//  Created by Heine Kristensen on 16/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKLevelIncreaseDialog.h"
#import "Card.h"
#import "HKImageButton.h"

@implementation HKLevelIncreaseDialog

-(instancetype)initWithCard:(Card*)card inScene:(SKScene*)scene {
    
    self = [super init];
    
    if (self) {
        
        _card = card;
        
        self.alpha = 0.0f;
        self.zPosition = 999;
        
        scene.userInteractionEnabled = NO;
        
        SKSpriteNode *background = [SKSpriteNode spriteNodeWithImageNamed:@"dialog_frame"];
        background.position = self.position;
        background.zPosition = 1001;
        [self addChild:background];
        
        SKSpriteNode *grayBackground = [SKSpriteNode spriteNodeWithColor:[UIColor darkGrayColor] size:scene.size];
        grayBackground.alpha = 0.3;
        grayBackground.position = self.position;
        grayBackground.zPosition = 1000;
        [self addChild:grayBackground];
        
        SKLabelNode *captionLabel = [SKLabelNode labelNodeWithFontNamed:APP_FONT_BOLD];
        captionLabel.position = CGPointMake(background.position.x, (background.size.height / 2) - 40);
        captionLabel.text = @"Level increased";
        captionLabel.fontSize = 16.0f;
        captionLabel.fontColor = [UIColor blackColor];
        captionLabel.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        [background addChild:captionLabel];
        
        SKLabelNode *dialogTextNode = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        dialogTextNode.position = CGPointMake(self.position.x, self.position.y + 60);
        dialogTextNode.text = [NSString stringWithFormat:@"Your %@ increased in level", _card.unitDescriptionName];
        dialogTextNode.fontSize = 14.0f;
        dialogTextNode.color = [UIColor whiteColor];
        dialogTextNode.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        [background addChild:dialogTextNode];
        
        SKLabelNode *subtitleTextNode = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        subtitleTextNode.position = CGPointMake(self.position.x, dialogTextNode.position.y - 25);
        subtitleTextNode.text = @"Select bonus:";
        subtitleTextNode.fontSize = 14.0f;
        subtitleTextNode.color = [UIColor whiteColor];
        subtitleTextNode.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        [background addChild:subtitleTextNode];
        
        __block HKLevelIncreaseDialog *weakSelf = self;
        HKImageButton *attackButton = [[HKImageButton alloc] initWithImage:@"button" selectedImage:@"button_selected" title:@"Attack" block:^(id  sender) {
            [self dismissDialogWithWeakRefToSelf:weakSelf selectedAbility:kLevelIncreaseAbilityAttack];
        }];

        HKImageButton *defenseButton = [[HKImageButton alloc] initWithImage:@"button" selectedImage:@"button_selected" title:@"Defense" block:^(id  sender) {
            [self dismissDialogWithWeakRefToSelf:weakSelf selectedAbility:kLevelIncreaseAbilityDefense];
        }];

        defenseButton.position = CGPointMake(background.position.x, -(background.size.height / 2) + 70);
        attackButton.position = CGPointMake(background.position.x, -(background.size.height / 2) + 130);
        
        [background addChild:defenseButton];
        [background addChild:attackButton];
        
        [self runAction:[SKAction fadeInWithDuration:0.2]];
    }
    
    return self;
}

- (void)dismissDialogWithWeakRefToSelf:(HKLevelIncreaseDialog*)weakSelf selectedAbility:(LevelIncreaseAbilities)ability {
    
    weakSelf.scene.userInteractionEnabled = YES;
    
    SKAction *fadeout = [SKAction fadeOutWithDuration:0.2];
    SKAction *dismiss = [SKAction removeFromParent];
    SKAction *informDelegate = [SKAction runBlock:^{
           if ([_delegate respondsToSelector:@selector(dialogNodeDidDismiss:withSelectedAbility:)]) {
         [_delegate dialogNodeDidDismiss:self withSelectedAbility:ability];
         }
    }];
    
    [self runAction:[SKAction sequence:@[fadeout, informDelegate, dismiss]]];
}

@end
