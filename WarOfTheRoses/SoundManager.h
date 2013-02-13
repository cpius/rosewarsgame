//
//  SoundManager.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/6/13.
//
//

#import <Foundation/Foundation.h>

#define BUTTON_CLICK_SOUND @"buttonclick.wav"
#define BOOM_SOUND @"boom.wav"
#define SWOOSH_SOUND @"swoosh.wav"
#define CARDFLIP_SOUND @"pageflip.mp3"

typedef enum {
    
    kGameEventButtonClick = 0,
    kGameEventCardDropped,
    kGameEventAttack
} GameEvents;

@interface SoundManager : NSObject

- (void)preloadSoundEffects;
- (void)playSoundEffectForGameEvent:(GameEvents)gameEvent;

+ (SoundManager*)sharedManager;

@end
