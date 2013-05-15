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
        
        CCLabelTTF *headline = [CCLabelTTF labelWithString:@"War Of The Roses" fontName:APP_FONT fontSize:32];
        headline.anchorPoint = ccp(0.5, 1);
        [headline setPosition:ccp(size.width / 2, size.height - 25)];
        [self addChild:headline];
		
        // Default font size will be 28 points.
		[CCMenuItemFont setFontSize:28];
        [CCMenuItemFont setFontName:APP_FONT];
		
		// Achievement Menu Item using blocks
		CCMenuItem *startGameMenuItem = [CCMenuItemFont itemWithString:@"Play game" block:^(id sender) {
			
            [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
            [[CCDirector sharedDirector] pushScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[GameTypeScene scene]]];
            
		}];
        
        CCMenuItem *settingsMenuItem = [CCMenuItemFont itemWithString:@"Settings" block:^(id sender) {
            
            [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
            CCLOG(@"Settings");
        }];
        
        CCMenuItem *creditsMenuItem = [CCMenuItemFont itemWithString:@"Credits" block:^(id sender) {
            [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
            CCLOG(@"Credits");
        }];
        
		CCMenu *menu = [CCMenu menuWithItems:startGameMenuItem, settingsMenuItem, creditsMenuItem, nil];
		
		[menu alignItemsVerticallyWithPadding:20];
		[menu setPosition:ccp(size.width/2, size.height/2 + 50)];
		
        menu.opacity = 0;
        [self addChild:menu];
        
        [menu runAction:[CCFadeIn actionWithDuration:0.5]];
        
        CCSprite *background = [CCSprite spriteWithFile:@"Background.png"];
        background.anchorPoint = CGPointMake(0, 0);
        [self addChild:background z:-1];
        
        CCParticleSystem *flame1 = [CCParticleSystemQuad particleWithFile:@"flame.plist"];
        flame1.position = ccp(55,(size.height / 2) - 47);
        //flame1.scale = 0.40;
        [background addChild:flame1 z:10];

        CCParticleSystem *flame2 = [CCParticleSystemQuad particleWithFile:@"flame.plist"];
        flame2.position = ccp(27,(size.height / 2) - 105);
       // flame2.scale = 0.40;
        [background addChild:flame2 z:10];
        
        CCParticleSystem *flame3 = [CCParticleSystemQuad particleWithFile:@"flame.plist"];
        flame3.position = ccp(265,(size.height / 2) - 93);
       // flame3.scale = 0.40;
        [background addChild:flame3 z:10];
    }
    
    return self;
}



@end
