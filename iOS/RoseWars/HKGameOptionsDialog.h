//
//  HKGameOptionsDialog.h
//  RoseWars
//
//  Created by Heine Kristensen on 07/02/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>
#import "HKGameOptionsDialogProtocol.h"

@interface HKGameOptionsDialog : SKNode

- (instancetype)initWithScene:(SKScene*)scene;

@property (weak, nonatomic) id<HKGameOptionsDialogProtocol> delegate;

@end
