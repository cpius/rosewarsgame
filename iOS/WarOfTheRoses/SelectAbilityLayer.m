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
    
    self = [super initWithColor:ccc4(139.0, 137.0, 137.0, 100.0)];
    
    if (self) {
        
        CGSize size = [CCDirector sharedDirector].winSize;
        
        CCLabelTTF *headline = [CCLabelTTF labelWithString:@"Level increased - select ability" fontName:APP_FONT fontSize:20];
        headline.anchorPoint = ccp(0.5, 1);
        [headline setPosition:ccp(size.width / 2, size.height - 25)];
        [self addChild:headline];

        CCMenuItemImage *attackMenuItem = [CCMenuItemImage itemWithNormalImage:@"attack_menu_button.png" selectedImage:@"attack_menu_button.png" block:^(id sender) {
        
            [_delegate layer:self selectedAbilityRaiseType:kAbilityRaiseTypeAttack];
        }];
        
        CCMenuItemImage *defenseMenuItem = [CCMenuItemImage itemWithNormalImage:@"defense_menu_button.png" selectedImage:@"defense_menu_button.png" block:^(id sender) {
            
            [_delegate layer:self selectedAbilityRaiseType:kAbilityRaiseTypeDefense];
        }];

		CCMenu *menu = [CCMenu menuWithItems:attackMenuItem, defenseMenuItem, nil];
		
		[menu alignItemsVerticallyWithPadding:10];
		[menu setPosition:ccp(size.width/2, size.height/2 + 50)];
		
		// Add the menu to the layer
		[self addChild:menu];
    }
    
    return self;
}
@end
