//
//  SoundManager.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/6/13.
//
//

#import "SoundManager.h"
#import "Deck.h"

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

- (void)preloadSoundEffectsForDeck:(Deck*)deck {
    
    for (Card *card in deck.cards) {
        
        if (card.attackSound != nil) {
            [[SimpleAudioEngine sharedEngine] preloadEffect:card.attackSound];
        }
        
        if (card.defeatSound != nil) {
            [[SimpleAudioEngine sharedEngine] preloadEffect:card.defeatSound];
        }

        if (card.moveSound != nil) {
            [[SimpleAudioEngine sharedEngine] preloadEffect:card.moveSound];
        }
}
}

- (void)preloadSoundEffects {
    
    [[SimpleAudioEngine sharedEngine] preloadEffect:BUTTON_CLICK_SOUND];
    [[SimpleAudioEngine sharedEngine] preloadEffect:BOOM_SOUND];
    [[SimpleAudioEngine sharedEngine] preloadEffect:SWOOSH_SOUND];
    [[SimpleAudioEngine sharedEngine] preloadEffect:CARDFLIP_SOUND];
    [[SimpleAudioEngine sharedEngine] preloadEffect:FANFARE];
}

- (void)playSoundEffectWithName:(NSString*)name {
    
    if (name != nil) {
        [[SimpleAudioEngine sharedEngine] playEffect:name];
    }
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
