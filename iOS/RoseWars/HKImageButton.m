//
//  HKImageButton.m
//  RoseWars
//
//  Created by Heine Skov Kristensen on 9/27/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import "HKImageButton.h"

static NSString* const kTitleNodeName = @"TitleNode";

@implementation HKImageButton

- (id)initWithImage:(NSString *)image selectedImage:(NSString*)selectedImage title:(NSString *)title block:(void (^)(id))block {
    
    _imageTexture = [SKTexture textureWithImageNamed:image];
    _title = title;
    
    self = [super initWithTexture:_imageTexture];
    
    if (self) {
        
        self.userInteractionEnabled = YES;
        self.enabled = YES;
        
        if (selectedImage != nil) {
            _selectedImageTexture = [SKTexture textureWithImageNamed:selectedImage];
        }
        
        if (_title != nil && _title.length > 0) {
            SKLabelNode *titleNode = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
            titleNode.fontSize = 14.0;
            titleNode.fontColor = [UIColor blackColor];
            titleNode.text = _title;
            titleNode.name = kTitleNodeName;
            titleNode.position = self.position;
            titleNode.verticalAlignmentMode = SKLabelVerticalAlignmentModeCenter;
            [self addChild:titleNode];
        }
        
        if (block) {
            block_ = [block copy];
        }
    }
    
    return self;
}

+ (id)imageButtonWithImage:(NSString *)image selectedImage:(NSString *)selectedImage title:(NSString *)title block:(void (^)(id))block {
    
    return [[HKImageButton alloc] initWithImage:image selectedImage:selectedImage title:title block:block];
}

+ (id)imageButtonWithImage:(NSString *)image selectedImage:(NSString*)selectedImage block:(void (^)(id sender))block {
    
    return [[HKImageButton alloc] initWithImage:image selectedImage:selectedImage title:nil block:block];
}

+ (id)imageButtonWithImage:(NSString *)image block:(void (^)(id sender))block {
    
    return [[HKImageButton alloc] initWithImage:image selectedImage:nil title:nil block:block];
}

- (void)setEnabled:(BOOL)enabled {
    
    _enabled = enabled;
    
    if (!_enabled) {
        [self setColor:[UIColor darkGrayColor]];
        [self setColorBlendFactor:0.5];
    }
    else {
        [self setColor:[SKColor colorWithRed:1.0 green:1.0 blue:1.0 alpha:1.0]];
    }
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    
    if (!self.enabled) return;
    
    if (_selectedImageTexture != nil) {
        [self setTexture:_selectedImageTexture];
        SKLabelNode *titleNode = (SKLabelNode*)[self childNodeWithName:kTitleNodeName];
        if (titleNode) {
            titleNode.fontColor = [UIColor lightTextColor];
        }
    }
}

- (void)touchesCancelled:(NSSet *)touches withEvent:(UIEvent *)event {
    
    if (!self.enabled) return;

    [self setTexture:_imageTexture];
}

- (void)touchesEnded:(NSSet *)touches withEvent:(UIEvent *)event {
    
    if (!self.enabled) return;

    [self setTexture:_imageTexture];
    
    SKLabelNode *titleNode = (SKLabelNode*)[self childNodeWithName:kTitleNodeName];
    if (titleNode) {
        titleNode.fontColor = [UIColor blackColor];
    }

    [SKAction playSoundFileNamed:@"buttonclick.wav" waitForCompletion:YES];
    
    if (self.removeOnClick) {
        [self runAction:[SKAction fadeOutWithDuration:0.2]];
    }

    if (block_) {
        block_(self);
    }
    
    if (self.removeOnClick) {
        [self removeFromParent];
    }
}

- (void)setSelected:(BOOL)selected {
    
    _selected = selected;
    
    [self setTexture:_selected ? _selectedImageTexture : _imageTexture];
}

@end
