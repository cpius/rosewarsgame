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
@synthesize myColor;
@synthesize numberOfAvailableActions;
@synthesize unitLayout = _unitLayout;

- (id)init {
    
    self = [super init];
    
    if (self) {
        self.myColor = arc4random() % 1;
        
        _unitLayout = [[NSMutableDictionary alloc] init];
    }
    
    return self;
}

- (PlayerColors)enemyColor {
    
    if (self.myColor == kPlayerGreen) {
        return kPlayerRed;
    }
    
    return kPlayerGreen;
}



- (NSData *)serializeCurrentGame {
    
    return nil;
}

+ (void)deserializeGameData:(NSData *)gameData {
    
    
}

@end
