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

- (void)startTimedAbilityOnCard:(Card *)card {
    
    [super startTimedAbilityOnCard:card];
    
    // Bribe makes card change color
    card.cardColor = !card.cardColor;
    
    // And adds a +1 attack bonus
    [card.attack addTimedBonus:[[TimedBonus alloc] initWithValue:1 forNumberOfRounds:1]];
}

@end
