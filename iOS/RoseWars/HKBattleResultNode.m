//
//  HKBattleResultNode.m
//  RoseWars
//
//  Created by Heine Kristensen on 20/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKBattleResultNode.h"

@implementation HKBattleResultNode

-(instancetype)initWithBattleResult:(NSString*)resultString {
    
    self = [super init];
    
    if (self) {
        
        self.zPosition = 999;

        SKSpriteNode *background = [SKSpriteNode spriteNodeWithImageNamed:@"info_bg"];
        background.position = self.position;
        background.zPosition = 1001;
        [self addChild:background];
        
        SKLabelNode *dialogTextNode = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
        dialogTextNode.position = background.position;
        dialogTextNode.text = resultString;
        dialogTextNode.fontSize = 14.0f;
        dialogTextNode.color = [UIColor whiteColor];
        dialogTextNode.horizontalAlignmentMode = SKLabelHorizontalAlignmentModeCenter;
        dialogTextNode.verticalAlignmentMode = SKLabelVerticalAlignmentModeCenter;
        [background addChild:dialogTextNode];
    }
    
    return self;
}


@end
