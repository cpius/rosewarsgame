//
//  Samurai.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "Samurai.h"
#import "MeleeAttackAction.h"

@interface Samurai()

@property (nonatomic, readwrite) NSInteger numberOfAttacksUsed;
@property (nonatomic, readwrite) BOOL hasPerformedMove;

@end

@implementation Samurai

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kInfantry;
        self.unitName = kSamurai;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        
        self.range = 1;
        self.move = 1;
        self.moveActionCost = 1;
        self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"samurai_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"samurai_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Samurai alloc] init];
}

- (void)resetAfterNewRound {
    
    [super resetAfterNewRound];
    
    self.numberOfAttacksUsed = 0;
    self.attackActionCost = 1;
    self.hasPerformedMove = NO;
}

- (BOOL)allowAction:(Action *)action allLocations:(NSDictionary *)allLocations {
    
    BOOL allowAction = [super allowAction:action allLocations:allLocations];

    if (action.actionType == kActionTypeMelee) {
        
        MeleeAttackAction *meleeAction = (MeleeAttackAction*)action;
        if (action.path != nil && action.path.count == 1) {
            
            if (_numberOfAttacksUsed == 0) {
                allowAction = YES;
            }
            
            if (_numberOfAttacksUsed == 1 && meleeAction.meleeAttackType == kMeleeAttackTypeNormal) {
                allowAction = YES;
            }
        }
    }
    
    return allowAction;
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    BOOL canPerformAction = [super canPerformActionOfType:actionType withRemainingActionCount:remainingActionCount];
    
    if (actionType == kActionTypeMelee && _numberOfAttacksUsed < 2) {
        canPerformAction = YES;
    }
    
    if (_hasPerformedMove) {
        canPerformAction = NO;
    }
    
    return canPerformAction;
}

- (void)didPerformedAction:(Action *)action {
    
    [super didPerformedAction:action];
    
    if (action.isMove) {
        _hasPerformedMove = YES;
    }
    
    if (action.isAttack) {
        
        MeleeAttackAction *meleeAction = (MeleeAttackAction*)action;
        
        if (_numberOfAttacksUsed < 2) {
            _numberOfAttacksUsed++;
            self.hasPerformedAttackThisRound = NO;
            self.attackActionCost = 0;
            
            if (meleeAction.battleResult.combatOutcome == kCombatOutcomeAttackSuccessful && meleeAction.meleeAttackType == kMeleeAttackTypeConquer) {
                [self consumeAllMoves];
            }
            else {
                self.movesConsumed = 0;
            }
        }
    }
}

@end
