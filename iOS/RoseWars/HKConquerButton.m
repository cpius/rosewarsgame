//
//  HKConquerButton.m
//  RoseWars
//
//  Created by Heine Kristensen on 18/02/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKConquerButton.h"

@implementation HKConquerButton

- (id)initWithBlock:(void (^)(id))block {
    
    self = [super initWithImage:@"button_conquer" selectedImage:@"button_conquer" title:@"" block:^(id sender) {
        block(self);
    }];
    
    if (self) {
        [self setScale:0.7];
        self.removeOnClick = YES;
        self.zPosition = 25;
    }
    
    return self;
}

@end
