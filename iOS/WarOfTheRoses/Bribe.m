//
//  Bribe.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/4/13.
//
//

#import "Bribe.h"
#import "Card.h"
#import "TimedBonus.h"

@implementation Bribe

- (void)startTimedAbility {
    
    [super startTimedAbility];
    
    // Bribe makes card change color
    _card.cardColor = !_card.cardColor;
    
    // And adds a +1 attack bonus
    [_card.attack addTimedBonus:[[TimedBonus alloc] initWithValue:1 forNumberOfRounds:1]];
}

@end
