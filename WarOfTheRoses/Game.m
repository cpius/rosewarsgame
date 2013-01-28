//
//  Game.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/5/13.
//
//

#import "Game.h"

@implementation Game

@synthesize gametype;
@synthesize myDeck = _deck;
@synthesize enemyDeck = _enemyDeck;
@synthesize currentRound;
@synthesize state;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        self.currentRound = 1;
        self.state = kGameStateInitialState;
    }
    
    return self;
}

- (NSData *)serializeCurrentGame {
    
    return nil;
}

+ (void)deserializeGameData:(NSData *)gameData {
    
    
}

@end
