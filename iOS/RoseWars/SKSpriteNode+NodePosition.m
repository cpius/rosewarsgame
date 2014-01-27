//
//  SKSpriteNode+NodePosition.m
//  RoseWars
//
//  Created by Heine Kristensen on 17/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "SKSpriteNode+NodePosition.h"

@implementation SKSpriteNode (NodePosition)

- (CGPoint)positionForChildNode:(SKSpriteNode *)childNode position:(NodePosition)nodePosition insets:(UIEdgeInsets)insets {
    
    switch (nodePosition) {
        case kNodePositionUpperLeft:
            return CGPointMake(self.position.x - (self.size.width / 2) + (childNode.size.width / 2) + insets.left,
                               self.position.y + (self.size.height / 2) - (childNode.size.height / 2) - insets.top);
            
        case kNodePositionLowerLeft:
            return CGPointMake(self.position.x - (self.size.width / 2) + (childNode.size.width / 2) + insets.left,
                               self.position.y - (self.size.height / 2) + (childNode.size.height / 2) + insets.bottom);
            
            
        case kNodePositionUpperRight:
            return CGPointMake(self.position.x + (self.size.width / 2) - (childNode.size.width / 2) - insets.right,
                               self.position.y + (self.size.height / 2) - (childNode.size.height / 2) - insets.top);
            
        case kNodePositionLowerRight:
            return CGPointMake(self.position.x + (self.size.width / 2) - (childNode.size.width / 2) - insets.right,
                               self.position.y - (self.size.height / 2) + (childNode.size.height / 2) + insets.bottom);
            
        default:
            break;
    }
    
    return CGPointZero;
}

- (CGPoint)positionForChildNode:(SKSpriteNode *)childNode position:(NodePosition)nodePosition {

    return [self positionForChildNode:childNode position:nodePosition insets:UIEdgeInsetsZero];
}

@end
