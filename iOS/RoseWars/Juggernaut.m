//
//  Juggernaut.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 5/26/13.
//
//

#import "Juggernaut.h"
#import "PushAction.h"
#import "PathFinderStep.h"
#import "MeleeAttackAction.h"
#import "JuggernautBattleStrategy.h"

@implementation Juggernaut

@synthesize battleStrategy = _battleStrategy;

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kSiege;
        self.unitName = kJuggernaut;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(3, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 2)];
        
        self.range = 1;
        self.move = 2;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";
        
        self.frontImageSmall = @"juggernaut_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"juggernaut_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Juggernaut alloc] init];
}

- (BaseBattleStrategy*)newBattleStrategy {
    
    return [JuggernautBattleStrategy strategy];
}

- (id<BattleStrategy>)battleStrategy {
    
    if (_battleStrategy == nil) {
        _battleStrategy = [self newBattleStrategy];
    }
    
    return _battleStrategy;
}

- (void)combatStartingAgainstAttacker:(Card *)attacker {
    
    [super combatStartingAgainstAttacker:attacker];
    
    if (attacker.isRanged) {
        _bonusAgainstRanged = [[RawBonus alloc] initWithValue:1];
        [self.defence addRawBonus:_bonusAgainstRanged];
    }
}

- (void)combatFinishedAgainstAttacker:(Card *)attacker withOutcome:(CombatOutcome)combatOutcome {

    [super combatFinishedAgainstAttacker:attacker withOutcome:combatOutcome];
    
    [self.defence removeRawBonus:_bonusAgainstRanged];
    _bonusAgainstRanged = nil;
}

@end
