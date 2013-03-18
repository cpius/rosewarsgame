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

@implementation WarElephant

@synthesize battleStrategy = _battleStrategy;
@synthesize aoeBattleStrategy = _aoeBattleStrategy;

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kCavalry;
        self.unitName = kWarElephant;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(4, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        
        self.range = 1;
        self.move = 2;
        self.moveActionCost = 1;
        self.attackActionCost = 2;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
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

- (id<BattleStrategy>)battleStrategy {
    
    if (_battleStrategy == nil) {
        _battleStrategy = [WarElephantBattleStrategy strategy];
    }
    
    return _battleStrategy;
}

- (void)didPerformedAction:(Action *)action {
    
    [super didPerformedAction:action];
    
    if (action.isAttack) {
        MeleeAttackAction *meleeAttackAction = (MeleeAttackAction*)action;
        
        // Get 2 diagonally nodes in attackdirection
        GridLocation *startLocation = [meleeAttackAction getEntryLocationInPath];
        
        NSMutableSet *surroundingMyCard = [NSMutableSet setWithArray:[startLocation surroundingEightGridLocations]];
        NSSet *surroundingEnemyCard = [NSSet setWithArray:[action.enemyCard.cardLocation surroundingGridLocations]];
        
        [surroundingMyCard intersectSet:surroundingEnemyCard];
        
        for (GridLocation *gridLocation in surroundingMyCard.allObjects) {
            
            Card *cardInLocation = [[GameManager sharedManager] cardLocatedAtGridLocation:gridLocation];
            
            if (cardInLocation != nil && cardInLocation.cardColor != meleeAttackAction.cardInAction.cardColor) {
                
                MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:gridLocation]] andCardInAction:action.cardInAction enemyCard:cardInLocation];
                
                CombatOutcome outcome = [[GameManager sharedManager] resolveCombatBetween:action.cardInAction defender:cardInLocation battleStrategy:_aoeBattleStrategy];
                
                [action.delegate action:meleeAction hasResolvedCombatWithOutcome:outcome];
            }
        }
        
        if (IsPushSuccessful(meleeAttackAction.combatOutcome) && !action.enemyCard.dead) {
            
            GridLocation *pushLocation = [action.enemyCard.cardLocation getPushLocationForGridLocationWhenComingFromGridLocation:[meleeAttackAction getEntryLocationInPath]];
            
            Card *cardAtPushLocation = [[GameManager sharedManager] cardLocatedAtGridLocation:pushLocation];
            
            if (cardAtPushLocation == nil) {

                MoveAction *pushAction = [[MoveAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:pushLocation]] andCardInAction:action.enemyCard enemyCard:nil];
                
                pushAction.delegate = action.delegate;
                [pushAction performActionWithCompletion:^{
                    
                }];
            }
            else {
                [[GameManager sharedManager] attackSuccessfulAgainstCard:action.enemyCard];
            }
        }
    }
}


@end
