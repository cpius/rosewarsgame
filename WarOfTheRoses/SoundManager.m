//
//  SoundManager.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/6/13.
//
//

#import "SoundManager.h"

@implementation SoundManager

+ (SoundManager*)sharedManager {
    
    static SoundManager* _instance = nil;
    
    @synchronized(self) {
        
        if (_instance == nil) {
            _instance = [[SoundManager alloc] init];
        }
    }
    
    return _instance;
}

- (void)preloadSoundEffects {
    
    [[SimpleAudioEngine sharedEngine] preloadEffect:BUTTON_CLICK_SOUND];
    [[SimpleAudioEngine sharedEngine] preloadEffect:BOOM_SOUND];
    [[SimpleAudioEngine sharedEngine] preloadEffect:SWOOSH_SOUND];
    [[SimpleAudioEngine sharedEngine] preloadEffect:CARDFLIP_SOUND];
}

- (void)playSoundEffectForGameEvent:(GameEvents)gameEvent {
    
    NSString *soundEffect;
    
    switch (gameEvent) {
        case kGameEventButtonClick:
            soundEffect = BUTTON_CLICK_SOUND;
            break;
            
        case kGameEventCardDropped:
            soundEffect = CARDFLIP_SOUND;
            break;
            
        case kGameEventAttack:
            soundEffect = BOOM_SOUND;
            break;
    }
    
    [[SimpleAudioEngine sharedEngine] playEffect:soundEffect];
}

@end
