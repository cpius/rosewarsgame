//
//  HKTextButton.m
//  RoseWars
//
//  Created by Heine Skov Kristensen on 8/9/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import "HKTextButton.h"

@implementation HKTextButton

- (id)initTextButtonWithText:(NSString *)text block:(void (^)(id))block {
    
    self = [super init];
    
    if (self) {
        
        self.userInteractionEnabled = YES;
        
        if (block) {
            block_ = [block copy];
        }

        _text = text;
        
        SKLabelNode *label = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        
        label.text = _text;
        label.position = self.position;
        label.fontSize = 24.0;
        
        [self addChild:label];
    }
    
    return self;
}

+ (id)textButtonWithText:(NSString *)text block:(void (^)(id))block {
    
    return [[HKTextButton alloc] initTextButtonWithText:text block:block];
}

- (void)touchesEnded:(NSSet *)touches withEvent:(UIEvent *)event {
    
    if (block_) {
        block_(self);
    }
}

@end
