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
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(5, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 2)];
        
        self.range = 4;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        
        hasSpecialAbility = YES;
        
        self.attackSound = @"bow_fired.wav";
        self.frontImageSmall = @"archer_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"archer_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Archer alloc] init];
}

-(BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return opponent.unitType == kInfantry;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {

    if (opponent.unitType == kInfantry) {
        _bonusAgainstInfantry = [[RawBonus alloc] initWithValue:1];
        [self.attack addRawBonus:_bonusAgainstInfantry];
    }
}

- (void)combatFinishedAgainstAttacker:(Card *)attacker withOutcome:(CombatOutcome)combatOutcome {
    
    [super combatFinishedAgainstAttacker:attacker withOutcome:combatOutcome];
    
    [self.attack removeRawBonus:_bonusAgainstInfantry];
    _bonusAgainstInfantry = nil;
}

- (void)combatFinishedAgainstDefender:(Card *)defender withOutcome:(CombatOutcome)combatOutcome {
    
    [super combatFinishedAgainstDefender:defender withOutcome:combatOutcome];
    
    [self.attack removeRawBonus:_bonusAgainstInfantry];
    _bonusAgainstInfantry = nil;
}

@end
