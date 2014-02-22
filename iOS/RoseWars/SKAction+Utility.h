//
//  SKAction+Utility.h
//  RoseWars
//
//  Created by Heine Kristensen on 29/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>

@interface SKAction (Utility)

+ (SKAction*)moveTo:(CGPoint)location duration:(NSTimeInterval)sec timingMode:(SKActionTimingMode)timingMode;

@end
