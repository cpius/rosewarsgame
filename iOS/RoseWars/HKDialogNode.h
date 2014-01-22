//
//  HKDialogNode.h
//  RoseWars
//
//  Created by Heine Kristensen on 08/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>
#import "HKDialogNodeProtocol.h"

@interface HKDialogNode : SKNode

@property (nonatomic, readonly, strong) SKLabelNode *dialogTextNode;
@property (nonatomic, weak) id<HKDialogNodeProtocol> delegate;

-(instancetype)initWithCaption:(NSString*)caption dialogText:(NSString*)dialogText inScene:(SKScene*)scene;

@end
