//
//  SKSpriteNode+NodePosition.h
//  RoseWars
//
//  Created by Heine Kristensen on 17/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>

typedef NS_ENUM(NSInteger, NodePosition) {
    kNodePositionUpperLeft,
    kNodePositionUpperRight,
    kNodePositionLowerLeft,
    kNodePositionLowerRight
};

@interface SKSpriteNode (NodePosition)

- (CGPoint)positionForChildNode:(SKSpriteNode*)childNode position:(NodePosition)nodePosition;
- (CGPoint)positionForChildNode:(SKSpriteNode*)childNode position:(NodePosition)nodePosition insets:(UIEdgeInsets)insets;

@end
