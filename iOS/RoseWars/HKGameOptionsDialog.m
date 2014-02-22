//
//  HKGameOptionsDialog.m
//  RoseWars
//
//  Created by Heine Kristensen on 07/02/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKGameOptionsDialog.h"
#import "HKImageButton.h"

@implementation HKGameOptionsDialog

- (instancetype)initWithScene:(SKScene*)scene {
    
    self = [super init];
    
    if (self) {
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
        captionLabel.text = @"The Rose Wars";
        captionLabel.fontSize = 16.0f;
        captionLabel.fontColor = [UIColor blackColor];
        captionLabel.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        [background addChild:captionLabel];
        
        __block HKGameOptionsDialog *weakSelf = self;
        HKImageButton *resumeButton = [[HKImageButton alloc] initWithImage:@"button" selectedImage:@"button_selected" title:@"Resume" block:^(id  sender) {
            [self dismissDialogWithWeakRefToSelf:weakSelf withDialogResult:GameOptionsDialogResume];
        }];
        
        HKImageButton *optionsButton = [[HKImageButton alloc] initWithImage:@"button" selectedImage:@"button_selected" title:@"Options" block:^(id  sender) {
            [self dismissDialogWithWeakRefToSelf:weakSelf withDialogResult:GameOptionsDialogOptions];
        }];

        HKImageButton *mainmenuButton = [[HKImageButton alloc] initWithImage:@"button" selectedImage:@"button_selected" title:@"Main menu" block:^(id  sender) {
            [self dismissDialogWithWeakRefToSelf:weakSelf withDialogResult:GameOptionsDialogMainMenu];
        }];

        mainmenuButton.position = CGPointMake(background.position.x, -(background.size.height / 2) + 65);
        optionsButton.position = CGPointMake(background.position.x, -(background.size.height / 2) + 125);
        resumeButton.position = CGPointMake(background.position.x, -(background.size.height / 2) + 185);
        
        [background addChild:resumeButton];
        [background addChild:optionsButton];
        [background addChild:mainmenuButton];
        
        [self runAction:[SKAction fadeInWithDuration:0.2]];
    }
    
    return self;
}

- (void)dismissDialogWithWeakRefToSelf:(HKGameOptionsDialog*)weakSelf withDialogResult:(GameOptionsDialogResult)result {
    
    weakSelf.scene.userInteractionEnabled = YES;
    
    SKAction *fadeout = [SKAction fadeOutWithDuration:0.2];
    SKAction *dismiss = [SKAction removeFromParent];
    SKAction *informDelegate = [SKAction runBlock:^{
        if ([self.delegate respondsToSelector:@selector(dialogNodeDidDismiss:withSelectedResult:)]) {
            [self.delegate dialogNodeDidDismiss:self withSelectedResult:result];
        }
    }];
    
    [self runAction:[SKAction sequence:@[fadeout, informDelegate, dismiss]]];
}


@end
