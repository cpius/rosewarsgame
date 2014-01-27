//
//  HKLevelIncreaseDialog.h
//  RoseWars
//
//  Created by Heine Kristensen on 16/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>
#import "HKLevelIncreaseDialogProtocol.h"

@class Card;
@interface HKLevelIncreaseDialog : SKNode

@property (readonly, strong, nonatomic) Card *card;
@property (weak, nonatomic) id<HKLevelIncreaseDialogProtocol> delegate;

-(instancetype)initWithCard:(Card*)card inScene:(SKScene*)scene;

@end
