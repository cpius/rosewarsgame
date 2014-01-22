//
//  HKDialogNode.m
//  RoseWars
//
//  Created by Heine Kristensen on 08/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKDialogNode.h"
#import "HKImageButton.h"

@implementation HKDialogNode

-(instancetype)initWithCaption:(NSString*)caption dialogText:(NSString*)dialogText inScene:(SKScene*)scene {
    
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
        captionLabel.text = caption;
        captionLabel.fontSize = 16.0f;
        captionLabel.fontColor = [UIColor blackColor];
        captionLabel.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        [background addChild:captionLabel];
        
        _dialogTextNode = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        _dialogTextNode.position = self.position;
        _dialogTextNode.text = dialogText;
        _dialogTextNode.fontSize = 14.0f;
        _dialogTextNode.color = [UIColor whiteColor];
        _dialogTextNode.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        [background addChild:_dialogTextNode];
        
        __block HKDialogNode *weakSelf = self;
        HKImageButton *okButton = [[HKImageButton alloc] initWithImage:@"button" selectedImage:@"button_selected" title:@"OK" block:^(id  sender) {
            
            weakSelf.scene.userInteractionEnabled = YES;
            
            SKAction *fadeout = [SKAction fadeOutWithDuration:0.2];
            SKAction *dismiss = [SKAction removeFromParent];
            SKAction *informDelegate = [SKAction runBlock:^{
                if ([_delegate respondsToSelector:@selector(dialogNodeDidDismiss:)]) {
                    [_delegate dialogNodeDidDismiss:self];
                }
            }];
            
            [self runAction:[SKAction sequence:@[fadeout, informDelegate, dismiss]]];
        }];
        
        okButton.position = CGPointMake(background.position.x, -(background.size.height / 2) + 60);
        [background addChild:okButton];
        
        [self runAction:[SKAction fadeInWithDuration:0.2]];
    }
    
    return self;
}


@end
