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
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:3];
        self.defence = [[HKAttribute alloc] initWithStartingValue:3];
        
        self.range = 1;
        self.move = 1;
        self.moveActionCost = 1;
        self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.unitHasExtraAction = YES;
        self.extraActionType = kExtraActionTypeAttack;
        
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
    
    self.attackActionCost = 1;
    self.hasPerformedMove = NO;
    self.hasPerformedAttackThisRound = NO;
}

- (BOOL)allowAction:(Action *)action allLocations:(NSDictionary *)allLocations {
    BOOL allowAction = [super allowAction:action allLocations:allLocations];

    if (action.actionType == kActionTypeMelee) {
        
        MeleeAttackAction *meleeAction = (MeleeAttackAction*)action;
        if (action.path != nil && action.path.count == 1) {
            
            if (self.hasPerformedAttackThisRound && meleeAction.meleeAttackType == kMeleeAttackTypeNormal) {
                allowAction = YES;
            }
        }
    }
    
    return allowAction;
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    BOOL canPerformAction = [super canPerformActionOfType:actionType withRemainingActionCount:remainingActionCount];
    
    if (actionType == kActionTypeMelee) {
        if (self.extraActionConsumed) {
            canPerformAction = NO;
        }
        else {
            canPerformAction = YES;
        }
    }
    
    if (self.hasPerformedMove) {
        canPerformAction = NO;
    }
    
    return canPerformAction;
}

- (void)didPerformedAction:(Action *)action {
    if (action.isAttack) {
        MeleeAttackAction *meleeAction = (MeleeAttackAction*)action;
        
        if (self.hasPerformedAttackThisRound) {
            self.extraActionConsumed = YES;
        }
        else {
            if (IsAttackSuccessful(meleeAction.battleResult.combatOutcome) && meleeAction.meleeAttackType == kMeleeAttackTypeConquer) {
                [self consumeAllMoves];
            }
        }
    }
    
    [super didPerformedAction:action];
    
    if (action.isMove) {
        self.hasPerformedMove = YES;
    }
}

@end
