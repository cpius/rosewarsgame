//
//  PlayerIndicator.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/18/13.
//
//

#import "PlayerIndicator.h"

@implementation PlayerIndicator

- (id)init {
    
    self = [super initWithFile:@"topbar.png"];
    
    if (self) {
        CCLabelTTF *label = [CCLabelTTF labelWithString:@"Opponent moving" fontName:APP_FONT fontSize:14];
        label.anchorPoint = ccp(0.5, 0.5);
        label.position = ccp(self.contentSize.width / 2, self.contentSize.height / 2);
        label.color = ccc3(255, 255, 255);
        
        [self addChild:label z:10];
    }
    
    return self;
}


@end
