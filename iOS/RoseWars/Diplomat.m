//
//  Diplomat.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/20/13.
//
//

#import "Diplomat.h"
#import "AbilityAction.h"

@interface Diplomat()

- (BOOL)canBribeOpponent:(Card*)opponent;
- (void)bribeOpponent:(Card*)opponent;

@end

@implementation Diplomat

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kInfantry;
        self.unitName = kDiplomat;
        self.unitAttackType = kUnitAttackTypeCaster;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:0];
        self.defence = [[HKAttribute alloc] initWithStartingValue:2];
        
        self.range = 3;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"diplomat_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"diplomat_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {

    return [[Diplomat alloc] init];
}

- (NSArray *)abilities {
    
    return @[@(kAbilityBribe)];
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    BOOL canPerformAction = [super canPerformActionOfType:actionType withRemainingActionCount:remainingActionCount];
    
    // Diplomat can't attack
    if (actionType == kActionTypeMelee || actionType == kActionTypeRanged) {
        canPerformAction = NO;
    }
    
    return canPerformAction;
}

- (BOOL)canBribeOpponent:(Card *)opponent {
    
    if ([opponent.cardIdentifier isEqualToString:_bribedOpponentIdentifier] && self.gamemanager.currentGame.currentRound - _opponentBribedInRound < 2) {
        return NO;
    }
    
    return YES;
}

- (void)bribeOpponent:(Card *)opponent {
    
    _bribedOpponentIdentifier = opponent.cardIdentifier;
    _opponentBribedInRound = self.gamemanager.currentGame.currentRound;
}

- (BOOL)isValidTarget:(Card*)targetCard {
    
    return [targetCard isOwnedByEnemy] && [self canBribeOpponent:targetCard];
}

- (void)didPerformedAction:(Action *)action {
    
    if ([action isKindOfClass:[AbilityAction class]]) {
        
        [self bribeOpponent:action.enemyCard];
    }
}

- (NSDictionary *)asDictionary {
    
    return [NSDictionary dictionaryWithObjectsAndKeys:
            _bribedOpponentIdentifier, @"bribed_opponent_identifier",
            @(_opponentBribedInRound), @"opponent_bribed_in_round", nil];
}

- (void)fromDictionary:(NSDictionary*)dictionary {
    
    _bribedOpponentIdentifier = [NSString stringWithFormat:@"%@", [dictionary valueForKey:@"bribed_opponent_identifier"]];
    _opponentBribedInRound = [[dictionary valueForKey:@"opponent_bribed_in_round"] integerValue];
}
@end
