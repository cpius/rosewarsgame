//
//  WarElephant.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/15/13.
//
//

#import "WarElephant.h"
#import "MeleeAttackAction.h"
#import "GameManager.h"
#import "PathFinderStep.h"
#import "StandardBattleStrategy.h"
#import "WarElephantBattleStrategy.h"
#import "MoveAction.h"
#import "PushAction.h"
#import "HKSecondaryAttackDiceRolls.h"

@implementation WarElephant

@synthesize battleStrategy = _battleStrategy;
@synthesize aoeBattleStrategy = _aoeBattleStrategy;

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kCavalry;
        self.unitName = kWarElephant;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:3];
        self.defence = [[HKAttribute alloc] initWithStartingValue:3];
        
        self.range = 1;
        self.move = 2;
        self.moveActionCost = 1;
        self.attackActionCost = 2;
        self.hitpoints = 1;
        
        self.attackSound = @"Elephant.mp3";
        self.defeatSound = @"Elephant.mp3";

        self.frontImageSmall = @"warelephant_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"warelephant_%d.png", self.cardColor];
        
        _aoeBattleStrategy = [StandardBattleStrategy strategy];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[WarElephant alloc] init];
}

- (BaseBattleStrategy*)newBattleStrategy {
    
    return [WarElephantBattleStrategy strategy];
}

- (id<BattleStrategy>)battleStrategy {
    
    if (_battleStrategy == nil) {
        _battleStrategy = [self newBattleStrategy];
    }
    
    return _battleStrategy;
}

- (void)didResolveCombatDuringAction:(Action *)action {
    
    [super didResolveCombatDuringAction:action];
    
    if (action.isAttack) {
        MeleeAttackAction *meleeAttackAction = (MeleeAttackAction*)action;
        
        // Get 2 diagonally nodes in attackdirection
        GridLocation *startLocation = [meleeAttackAction getEntryLocationInPath];
        
        NSMutableSet *surroundingMyCard = [NSMutableSet setWithArray:[startLocation surroundingEightGridLocations]];
        NSSet *surroundingEnemyCard = [NSSet setWithArray:[action.enemyInitialLocation surroundingGridLocations]];
        
        [surroundingMyCard intersectSet:surroundingEnemyCard];
        
        for (GridLocation *gridLocation in surroundingMyCard.allObjects) {
            
            Card *cardInLocation = [self.gamemanager cardLocatedAtGridLocation:gridLocation];
            
            if (cardInLocation != nil && cardInLocation.cardColor != meleeAttackAction.cardInAction.cardColor) {
                
                MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:(GameManager*)self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:gridLocation]] andCardInAction:action.cardInAction enemyCard:cardInLocation];
                
                BattleReport *battleReport = [BattleReport battleReportWithAction:meleeAction];
                
                if (action.playback) {
                    
                    HKSecondaryAttackDiceRolls *secondaryAttackDiceRolls = [meleeAttackAction.secondaryActionsForPlayback objectForKey:gridLocation];
                    
                    if (secondaryAttackDiceRolls != nil) {
                        action.cardInAction.battleStrategy.attackerDiceStrategy = secondaryAttackDiceRolls.attackRoll;
                        cardInLocation.battleStrategy.defenderDiceStrategy = secondaryAttackDiceRolls.defenseRoll;
                    }
                }
                
                BattleResult *outcome = [self.gamemanager resolveCombatBetween:action.cardInAction defender:cardInLocation battleStrategy:action.cardInAction.battleStrategy];
                
                outcome.meleeAttackType = kMeleeAttackTypeNormal;
                battleReport.primaryBattleResult = outcome;
                
                if (!action.playback) {
                    [action.battleReport.secondaryBattleReports addObject:battleReport];
                }
                
                [action.delegate action:meleeAction hasResolvedCombatWithResult:outcome];
            }
        }
    }
}

- (void)didPerformedAction:(Action *)action {
    
    [super didPerformedAction:action];
    
}


@end
