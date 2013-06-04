//
//  SelectAbilityLayer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 5/10/13.
//
//

#import "SelectAbilityLayer.h"

@implementation SelectAbilityLayer

- (id)init {
    
    self = [super initWithColor:ccc4(0, 0, 0, 200)];
    
    if (self) {
        
        CGSize size = [CCDirector sharedDirector].winSize;
        
        CCLabelTTF *headline = [CCLabelTTF labelWithString:@"Level increased - select ability" fontName:APP_FONT fontSize:20];
        headline.anchorPoint = ccp(0.5, 1);
        [headline setPosition:ccp(size.width / 2, size.height - 25)];
        [self addChild:headline];
        
        CCSprite *ironplate = [CCSprite spriteWithFile:@"ironplate.png"];
        ironplate.anchorPoint = ccp(0.5, 0.5);
        ironplate.position = ccp(size.width / 2, size.height / 2);
        [self addChild:ironplate];

        CCMenuItemImage *attackMenuItem = [CCMenuItemImage itemWithNormalImage:@"attack_menu_button.png" selectedImage:@"attack_menu_button.png" block:^(id sender) {
        
            [_delegate layer:self selectedAbilityRaiseType:kAbilityRaiseTypeAttack forCard:_card];
        }];
        
        CCMenuItemImage *defenseMenuItem = [CCMenuItemImage itemWithNormalImage:@"defense_menu_button.png" selectedImage:@"defense_menu_button.png" block:^(id sender) {
            
            [_delegate layer:self selectedAbilityRaiseType:kAbilityRaiseTypeDefense forCard:_card];
        }];

		CCMenu *menu = [CCMenu menuWithItems:attackMenuItem, defenseMenuItem, nil];
		
		[menu alignItemsVerticallyWithPadding:10];
		[menu setPosition:ccp(ironplate.contentSize.width/2, ironplate.contentSize.height/2)];
		
		// Add the menu to the layer
		[ironplate addChild:menu];
    }
    
    return self;
}
@end
