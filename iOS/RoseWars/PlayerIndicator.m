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
    
    self = [super initWithImageNamed:@"topbar"];
    
    if (self) {
        SKLabelNode *label = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        
        label.text = @"Opponent moving";
        label.fontSize = 14.0;
        label.fontColor = [SKColor colorWithRed:255 green:255 blue:255 alpha:1.0];
        label.position = CGPointMake(self.size.width / 2, self.size.height / 2);
        label.zPosition = 10;
        
        [self addChild:label];
    }
    
    return self;
}


@end
