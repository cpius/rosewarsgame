//
//  HKImageButton.h
//  RoseWars
//
//  Created by Heine Skov Kristensen on 9/27/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>

@interface HKImageButton : SKSpriteNode {
    
    void (^block_)(id sender);
    SKTexture *_imageTexture;
    SKTexture *_selectedImageTexture;
}

@property (nonatomic, copy) NSString *title;

+ (id)imageButtonWithImage:(NSString *)image block:(void (^)(id sender))block;
+ (id)imageButtonWithImage:(NSString *)image selectedImage:(NSString*)selectedImage block:(void (^)(id sender))block;
+ (id)imageButtonWithImage:(NSString *)image selectedImage:(NSString *)selectedImage title:(NSString*)title block:(void (^)(id))block;

- (id)initWithImage:(NSString *)image selectedImage:(NSString*)selectedImage title:(NSString*)title block:(void (^)(id))block;

@property (nonatomic, assign) BOOL selected;

@end
