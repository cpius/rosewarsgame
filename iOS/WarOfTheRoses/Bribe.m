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
#import "AbilityFactory.h"

@implementation Bribe

- (void)startTimedAbility {
    
    [super startTimedAbility];
    
    // Bribe makes card change color
    self.card.cardColor = !self.card.cardColor;
    
    // And adds a +1 attack bonus
    [self.card.attack addTimedBonus:[[TimedBonus alloc] initWithValue:1 forNumberOfRounds:1]];
    
    CCLOG(@"Card: %@ has been bribed", self.card);
}

- (void)stopTimedAbility {
    
    // After bribe card has 1 cooldown round
    [AbilityFactory addAbilityOfType:kAbilityCoolDown onCard:self.card];
}

- (BOOL)friendlyAbility {
    
    return NO;
}

@end
