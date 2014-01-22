//
//  HKTextButton.h
//  RoseWars
//
//  Created by Heine Skov Kristensen on 8/9/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>

@interface HKTextButton : SKNode {
    
    void (^block_)(id sender);
    NSString *_text;
}

- (id)initTextButtonWithText:(NSString *)text block:(void (^)(id))block;
+ (id)textButtonWithText:(NSString*)text block:(void(^)(id sender))block;

@end
