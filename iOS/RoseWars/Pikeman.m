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
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:2];
        self.defence = [[HKAttribute alloc] initWithStartingValue:2];

        self.range = 1;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

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

- (void)combatStartingAgainstDefender:(Card *)defender {
    
    if (defender.unitType == kCavalry) {
        _bonusAgainstCavalry = [[RawBonus alloc] initWithValue:1];
        [self.attack addRawBonus:_bonusAgainstCavalry];
    }
}

- (void)combatFinishedAgainstDefender:(Card *)defender withOutcome:(CombatOutcome)combatOutcome {
    
    [super combatFinishedAgainstDefender:defender withOutcome:combatOutcome];

    [self.attack removeRawBonus:_bonusAgainstCavalry];
    _bonusAgainstCavalry = nil;
}

@end
