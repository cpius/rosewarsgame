//
//  MainMenuScene.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/18/12.
//
//

#import "MainMenuScene.h"
#import "AppDelegate.h"
#import "ConstructDeckScene.h"
#import "GameTypeScene.h"

@implementation MainMenuScene

+ (id)scene {
    
    CCScene *scene = [CCScene node];
    
    MainMenuScene *layer = [MainMenuScene node];
    
    [scene addChild:layer];
    
    return scene;
}

- (id)init {
    
    self = [super init];
    
    if (self) {
		// ask director for the window size
		CGSize size = [[CCDirector sharedDirector] winSize];
        
        CCLabelTTF *headline = [CCLabelTTF labelWithString:@"War Of The Roses" fontName:@"AppleGothic" fontSize:32];
        headline.anchorPoint = ccp(0.5, 1);
        [headline setPosition:ccp(size.width / 2, size.height - 25)];
        [self addChild:headline];
		
        // Default font size will be 28 points.
		[CCMenuItemFont setFontSize:28];
        [CCMenuItemFont setFontName:@"AppleGothic"];
		
		// Achievement Menu Item using blocks
		CCMenuItem *startGameMenuItem = [CCMenuItemFont itemWithString:@"Play game" block:^(id sender) {
			
            [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
            [[CCDirector sharedDirector] pushScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[GameTypeScene scene]]];
            
		}];
        
        CCMenuItem *settingsMenuItem = [CCMenuItemFont itemWithString:@"Settings" block:^(id sender) {
            
            [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
            CCLOG(@"Settings");
        }];
        
        CCMenuItem *creditsMenuItem = [CCMenuItemFont itemWithString:@"Credits" block:^(id sender) {
            [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
            CCLOG(@"Credits");
        }];
        
		CCMenu *menu = [CCMenu menuWithItems:startGameMenuItem, settingsMenuItem, creditsMenuItem, nil];
		
		[menu alignItemsVerticallyWithPadding:20];
		[menu setPosition:ccp(size.width/2, size.height/2 + 50)];
		
		// Add the menu to the layer
		[self addChild:menu];
        
        CCSprite *background = [CCSprite spriteWithFile:@"Background.png"];
        background.anchorPoint = CGPointMake(0, 0);
        [self addChild:background z:-1];
    }
    
    return self;
}



@end
