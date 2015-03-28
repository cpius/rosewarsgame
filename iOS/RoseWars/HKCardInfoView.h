//
//  HKCardInfoView.h
//  RoseWars
//
//  Created by Heine Kristensen on 26/03/15.
//  Copyright (c) 2015 Heine Skov Kristensen. All rights reserved.
//

#import <SpriteKit/SpriteKit.h>

@class Card;
@interface HKCardInfoView : SKNode

- (instancetype)initWithCard:(Card*)card inScene:(SKScene*)scene;

@end
