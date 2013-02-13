//
//  EndTurnLayer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/6/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "EndTurnLayer.h"


@implementation EndTurnLayer

+ (EndTurnLayer *)getEndTurnLayerWithSize:(CGSize)size {
    
    EndTurnLayer *layer = [[EndTurnLayer alloc] initWithColor:ccc4(127, 127, 127, 225) width:size.width height:size.height];
    
    CCSprite *border = [CCSprite spriteWithFile:@"testframe.png"];
    border.position = ccp(size.width / 2, size.height / 2);
    [layer addChild:border];
    
    CCLabelTTF *label = [CCLabelTTF labelWithString:@"End of turn" fontName:APP_FONT fontSize:24];
    label.color = ccc3(0, 0, 0);
    label.position = ccp(border.contentSize.width / 2, border.contentSize.height / 2);
    [border addChild:label];
    
    return layer;
}


@end
