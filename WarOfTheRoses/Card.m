//
//  Card.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "Card.h"

@interface Card()


@end

@implementation Card

@synthesize frontImageSmall = _frontImageSmall;
@synthesize frontImageLarge = _frontImageLarge;
@synthesize backImage = _backImage;
@synthesize cardColor = _cardColor;
@synthesize cardLocation = _cardLocation;
@synthesize isShowingDetail;
@synthesize attack = _attack, defence = _defence;
@synthesize movesConsumed;
@synthesize move;
@synthesize experience;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        _cardColor = kCardColorGreen;
        self.isShowingDetail = NO;
        
    }
    
    return self;
}

- (void)commonInit {
    
    self.attack.attributeAbbreviation = @"A";
    self.attack.valueAffectedByBonuses = kRangedAttributeLowerValue;
    
    self.defence.attributeAbbreviation = @"D";
    self.defence.valueAffectedByBonuses = kRangedAttributeUpperValue;
    
    numberOfLevelsIncreased = 0;
    self.experience = 0;
}

- (NSString *)description {
    
    NSString *description = [NSString stringWithFormat:@"CardType: %d - UnitType: %d - UnitName: %d - Boardlocation: row %d column %d",
                             self.cardType,
                             self.unitType,
                             self.unitName,
                             self.cardLocation.row,
                             self.cardLocation.column];
    
    return description;
}


// Must be overloaded in subclasses
- (BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return NO;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
}

- (void)defenceSuccessfulAgainstAttacker:(Card *)attacker {
    
    
}

- (void)attackSuccessfulAgainstDefender:(Card *)defender {
    
    // Attack succcessfull - assign experience if applicable
    if (self.experience < 4) {
        self.experience++;
    }
}


- (BOOL)isOwnedByPlayerWithColor:(PlayerColors)playerColor {
    
    return (self.cardColor == kCardColorGreen && playerColor == kPlayerGreen) ||
    (self.cardColor == kCardColorRed && playerColor == kPlayerRed);
}

@end
