//
//  Bribe.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/4/13.
//
//

#import "Bribe.h"
#import "Card.h"
#import "AbilityFactory.h"

@implementation Bribe

- (void)applyEffect {
    
    // Bribe makes card change color
    self.card.cardColor = OppositeColorOfCardColor(_originalColorOfBribedUnit);
    
    // And adds a +1 attack bonus
    [self.card.attack addTimedBonus:[[TimedBonus alloc] initWithValue:1 forNumberOfTurns:1 gamemanager:self.card.gamemanager]];
    
    NSLog(@"Card: %@ has been bribed", self.card);
}

- (void)startTimedAbility {
    
    [super startTimedAbility];
    
    _originalColorOfBribedUnit = self.card.cardColor;
    
    [self applyEffect];
}

- (void)reactivateTimedAbility {
    
    [super reactivateTimedAbility];
    [self applyEffect];
}

- (void)stopTimedAbility {

    // Reset card color
    self.card.cardColor = _originalColorOfBribedUnit;

    // After bribe card has 1 cooldown round
    [AbilityFactory addAbilityOfType:kAbilityCoolDown onCard:self.card];
    
    [super stopTimedAbility];
    
    NSLog(@"Card: %@ in no longe bribed", self.card);
}

- (BOOL)friendlyAbility {
    
    return NO;
}

- (AbilityTypes)abilityType {
    
    return kAbilityBribe;
}

- (NSDictionary*)asDictionary {
    
    return [NSDictionary dictionaryWithObjectsAndKeys:@(_originalColorOfBribedUnit), @"original_color_of_bribed_unit", nil];
}

- (void)fromDictionary:(NSDictionary*)dictionary {
    
    _originalColorOfBribedUnit = (CardColors)[[dictionary valueForKey:@"original_color_of_bribed_unit"] integerValue];
}

@end
