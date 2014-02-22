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
#import "HKPlaygroundScene.h"

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
        
        HKPlaygroundScene *playground = [HKPlaygroundScene sceneWithSize:self.size];
        playground.scaleMode = SKSceneScaleModeFill;
        [self.view presentScene:playground transition:[SKTransition fadeWithDuration:0.5]];
    }];

    HKImageButton *creditsButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Credits" block:^(id sender) {
    }];

    [playGameButton setScale:1.4];
    [settingsButton setScale:1.4];
    [creditsButton setScale:1.4];
    
    playGameButton.position = CGPointMake(-CGRectGetWidth(playGameButton.frame), CGRectGetHeight(self.frame) - 150);
    settingsButton.position = CGPointMake(CGRectGetWidth(self.frame) + CGRectGetWidth(settingsButton.frame), CGRectGetMinY(playGameButton.frame) - 40);
    creditsButton.position = CGPointMake(-CGRectGetWidth(creditsButton.frame), CGRectGetMinY(settingsButton.frame) - 40);
    
    [self addChild:playGameButton];
    [self addChild:settingsButton];
    [self addChild:creditsButton];
    
    SKAction *presentMenuAction = [SKAction sequence:@[[SKAction waitForDuration:0.2], [SKAction runBlock:^{
        
        [playGameButton runAction:[SKAction moveTo:CGPointMake(CGRectGetMidX(self.frame), CGRectGetHeight(self.frame) - 150) duration:0.2 timingMode:SKActionTimingEaseIn]];
        [settingsButton runAction:[SKAction moveTo:CGPointMake(CGRectGetMidX(self.frame), CGRectGetMinY(playGameButton.frame) - 40) duration:0.2 timingMode:SKActionTimingEaseIn]];
        [creditsButton runAction:[SKAction moveTo:CGPointMake(CGRectGetMidX(self.frame), CGRectGetMinY(settingsButton.frame) - 40) duration:0.2 timingMode:SKActionTimingEaseIn]];
    }]]];
    
    [self runAction:presentMenuAction];
   
    SKEmitterNode *fireNode = [self newFireEmitter];
    fireNode.position = CGPointMake(55, CGRectGetHeight(self.frame) / 2 - 47);
    [fireNode setScale:0.5];
    [self addChild:fireNode];
    
    SKEmitterNode *fireNode2 = [ self newFireEmitter];
    fireNode2.position = CGPointMake(27, CGRectGetHeight(self.frame) / 2 - 110);
    [fireNode2 setScale:0.5];
    [self addChild:fireNode2];

    SKEmitterNode *fireNode3 = [ self newFireEmitter];
    fireNode3.position = CGPointMake(265, CGRectGetHeight(self.frame) / 2 - 90);
    [fireNode3 setScale:0.5];
    [self addChild:fireNode3];
}

- (SKEmitterNode*)newFireEmitter {
    
    NSString *fireEmitterPath = [[NSBundle mainBundle] pathForResource:@"Flame" ofType:@"sks"];
    
    return [NSKeyedUnarchiver unarchiveObjectWithFile:fireEmitterPath];
}

@end
