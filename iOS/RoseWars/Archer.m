//
//  Archer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "Archer.h"

@implementation Archer

-(id)init {
    self = [super init];
    
    if (self) {
                
        self.cardType = kCardTypeBasicUnit;
        self.unitType = kInfantry;
        self.unitName = kArcher;
        self.unitAttackType = kUnitAttackTypeRanged;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:2];
        self.defence = [[HKAttribute alloc] initWithStartingValue:2];
        
        self.range = 4;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"bow_fired.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";
        self.frontImageSmall = @"archer_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"archer_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Archer alloc] init];
}

- (void)combatStartingAgainstDefender:(Card *)defender {
    
    if (defender.unitType == kInfantry) {
        _bonusAgainstInfantry = [[RawBonus alloc] initWithValue:1];
        [self.attack addRawBonus:_bonusAgainstInfantry];
    }
}

- (void)combatFinishedAgainstDefender:(Card *)defender withOutcome:(CombatOutcome)combatOutcome {
    
    [super combatFinishedAgainstDefender:defender withOutcome:combatOutcome];
    
    [self.attack removeRawBonus:_bonusAgainstInfantry];
    _bonusAgainstInfantry = nil;
}

@end
