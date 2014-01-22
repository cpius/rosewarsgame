//
//  HKMainMenuScene.m
//  RoseWars
//
//  Created by Heine Skov Kristensen on 8/9/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import "HKMainMenuScene.h"
#import "HKImageButton.h"
#import "HKGameTypeScene.h"
#import "HKDialogNode.h"
#import "HKLevelIncreaseDialog.h"

@implementation HKMainMenuScene

- (instancetype)initWithSize:(CGSize)size {
    
    self = [super initWithSize:size];
    
    if (self) {
        
    }
    
    return self;
}

- (void)didMoveToView:(SKView *)view {
    
    SKSpriteNode *backgroundNode = [SKSpriteNode spriteNodeWithImageNamed:@"Background"];
    
    backgroundNode.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMidY(self.frame));
    [self addChild:backgroundNode];
    
    SKLabelNode *headline = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
    
    headline.text = @"The Rose Wars";
    headline.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetHeight(self.frame) - 50);
    headline.fontSize = 32;
    
    [self addChild:headline];
    
    HKImageButton *playGameButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Play game" block:^(id sender) {
        HKGameTypeScene *gameTypeScene = [HKGameTypeScene sceneWithSize:self.size];
        gameTypeScene.scaleMode = SKSceneScaleModeFill;
        
        [self.view presentScene:gameTypeScene transition:[SKTransition fadeWithDuration:0.5]];
    }];
    
    HKImageButton *settingsButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Settings" block:^(id sender) {
        
        HKLevelIncreaseDialog *dialog = [[HKLevelIncreaseDialog alloc] initWithCard:Nil inScene:self];
        dialog.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMidY(self.frame));
        [self addChild:dialog];
    }];

    HKImageButton *creditsButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Credits" block:^(id sender) {
    }];

    [playGameButton setScale:1.4];
    [settingsButton setScale:1.4];
    [creditsButton setScale:1.4];
    
    playGameButton.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetHeight(self.frame) - 150);
    settingsButton.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMinY(playGameButton.frame) - 40);
    creditsButton.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMinY(settingsButton.frame) - 40);
    
    [self addChild:playGameButton];
    [self addChild:settingsButton];
    [self addChild:creditsButton];
    
    SKEmitterNode *fireNode = [self newFireEmitter];
    fireNode.position = CGPointMake(55, CGRectGetHeight(self.frame) / 2 - 47);
    fireNode.xScale = 0.5;
    fireNode.yScale = 0.5;
    [self addChild:fireNode];
}

- (SKEmitterNode*)newFireEmitter {
    
    NSString *fireEmitterPath = [[NSBundle mainBundle] pathForResource:@"Flame" ofType:@"sks"];
    
    return [NSKeyedUnarchiver unarchiveObjectWithFile:fireEmitterPath];
}

@end
