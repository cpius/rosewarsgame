//
//  Pikeman.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "Pikeman.h"

@implementation Pikeman

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kInfantry;
        self.unitName = kPikeman;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(5, 6)];
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        self.range = 1;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        
        hasSpecialAbility = YES;
        
        self.attackSound = @"sword_sound.wav";

        self.frontImageSmall = @"pikeman_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"pikeman_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Pikeman alloc]init];
}

- (BOOL)zoneOfControlAgainst:(Card *)opponent {
    
    return (self.cardColor != opponent.cardColor) && (opponent.unitType == kCavalry);
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return opponent.unitType == kCavalry;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
    if (opponent.unitType == kCavalry) {
        _bonusAgainstCavalry = [[RawBonus alloc] initWithValue:1];
        [self.attack addRawBonus:_bonusAgainstCavalry];
    }
}

- (void)combatFinishedAgainstAttacker:(Card *)attacker withOutcome:(CombatOutcome)combatOutcome {
    
    [super combatFinishedAgainstAttacker:attacker withOutcome:combatOutcome];
    
    [self.attack removeRawBonus:_bonusAgainstCavalry];
    _bonusAgainstCavalry = nil;
}

- (void)combatFinishedAgainstDefender:(Card *)defender withOutcome:(CombatOutcome)combatOutcome {
    
    [super combatFinishedAgainstDefender:defender withOutcome:combatOutcome];

    [self.attack removeRawBonus:_bonusAgainstCavalry];
    _bonusAgainstCavalry = nil;
}

@end
