//
//  BattlePlan.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import "BattlePlan.h"
#import "PathFinder.h"
#import "GameManager.h"

@implementation BattlePlan

- init {
    
    self = [super init];
    
    if (self) {
        
    }
    
    return self;
}

- (NSArray *)createBattlePlanForCard:(Card *)card enemyUnits:(NSArray *)enemyUnits unitLayout:(NSDictionary *)unitLayout {
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSUInteger remainingActionCount = [GameManager sharedManager].currentGame.numberOfAvailableActions;
    
    if ([card canPerformActionOfType:kActionTypeMove withRemainingActionCount:remainingActionCount]) {
        _moveActions = [pathFinder getMoveActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits allLocations:unitLayout];
    }
    
    if ([card canPerformActionOfType:kActionTypeMelee withRemainingActionCount:remainingActionCount]) {
        _meleeActions = [pathFinder getMeleeAttackActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits allLocations:unitLayout];
    }

    if ([card canPerformActionOfType:kActionTypeRanged withRemainingActionCount:remainingActionCount]) {
        _rangeActions = [pathFinder getRangedAttackActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits allLocations:unitLayout];
    }
    
    return [[_moveActions arrayByAddingObjectsFromArray:_meleeActions] arrayByAddingObjectsFromArray:_rangeActions];
}

@end
