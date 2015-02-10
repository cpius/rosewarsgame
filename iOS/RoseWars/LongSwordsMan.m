//
//  LongSwordsMan.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "Longswordsman.h"
#import "Action.h"
#import "GameManager.h"
#import "PathFinderStep.h"
#import "MeleeAttackAction.h"
#import "StandardBattleStrategy.h"
#import "HKSecondaryAttackDiceRolls.h"

@implementation Longswordsman

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kInfantry;
        self.unitName = kLongswordsman;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[HKAttribute alloc] initWithStartingValue:3];
        self.defence = [[HKAttribute alloc] initWithStartingValue:3];
        
        self.range = 1;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"longswordsman_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"longswordsman_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    return [[Longswordsman alloc] init];
}

- (void)didResolveCombatDuringAction:(Action *)action {
    
    [super didResolveCombatDuringAction:action];

    MeleeAttackAction *meleeAttackAction = (MeleeAttackAction*)action;
    
    if (meleeAttackAction.isAttack) {
        
        // Get 4 nearby tiles in attackdirection
        GridLocation *startLocation = meleeAttackAction.startLocation;
        GridLocation *endLocation = [meleeAttackAction getLastLocationInPath];
        
        NSMutableSet *surroundingMyCard = [NSMutableSet setWithArray:[startLocation surroundingEightGridLocations]];
        NSSet *surroundingEnemyCard = [NSSet setWithArray:[endLocation surroundingEightGridLocations]];
        
        [surroundingMyCard intersectSet:surroundingEnemyCard];
        
        for (GridLocation *gridLocation in surroundingMyCard.allObjects) {
            
            Card *cardInLocation = [self.gamemanager cardLocatedAtGridLocation:gridLocation];
            
            if (cardInLocation != nil && cardInLocation.cardColor != meleeAttackAction.cardInAction.cardColor) {
                
                MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:gridLocation]] andCardInAction:action.cardInAction enemyCard:cardInLocation meleeAttackType:kMeleeAttackTypeNormal];
                
                BattleReport *battleReport = [BattleReport battleReportWithAction:meleeAction];
                
                if (action.playback) {
                    
                    HKSecondaryAttackDiceRolls *secondaryAttackDiceRolls = [meleeAttackAction.secondaryActionsForPlayback objectForKey:gridLocation];
                    
                    if (secondaryAttackDiceRolls != nil) {
                        action.cardInAction.battleStrategy.attackerDiceStrategy = secondaryAttackDiceRolls.attackRoll;
                        cardInLocation.battleStrategy.defenderDiceStrategy = secondaryAttackDiceRolls.defenseRoll;
                    }
                }
                
                BattleResult *outcome = [self.gamemanager resolveCombatBetween:action.cardInAction defender:cardInLocation battleStrategy:action.cardInAction.battleStrategy];
                
                outcome.meleeAttackType = meleeAction.meleeAttackType;
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
