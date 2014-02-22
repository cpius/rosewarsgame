//
//  SKAction+Utility.m
//  RoseWars
//
//  Created by Heine Kristensen on 29/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "SKAction+Utility.h"

@implementation SKAction (Utility)

+ (SKAction*)moveTo:(CGPoint)location duration:(NSTimeInterval)sec timingMode:(SKActionTimingMode)timingMode {
    
    SKAction *moveAction = [SKAction moveTo:location duration:sec];
    moveAction.timingMode = timingMode;
    
    return moveAction;
}

@end
