//
//  AttackAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "MeleeAttackAction.h"

@implementation MeleeAttackAction

@synthesize meleeAttackType;

- (BOOL)isWithinRange {
    
    return self.path.count <= self.cardInAction.movesRemaining;
}

- (BOOL)isAttack {
    
    return YES;
}

- (ActionTypes)actionType {
    
    return kActionTypeMelee;
}

- (void)performAction {
    
 /*   [self.delegate beforePerformAction:self];
    
    [_gameboard moveActiveGameBoardNodeFollowingPath:action.path onCompletion:^{
        
        CombatOutcome outcome = [self engageCombatBetweenMyCard:[_gameboard activeNode].card.model andEnemyCard:targetNode.card.model];
        
        if (outcome == kCombatOutcomeDefendSuccessful) {
            
            PathFinderStep *retreatToLocation = [action.path objectAtIndex:action.path.count - 2];
            
            [_gameboard moveActiveGameBoardNodeFollowingPath:[NSArray arrayWithObject:retreatToLocation] onCompletion:^{
                
                if (![[_gameboard activeNode].locationInGrid isEqual:retreatToLocation.location]) {
                    [_gameManager card:[_gameboard activeNode].card.model movedToGridLocation:retreatToLocation.location];
                    [_gameboard swapCardFromNode:[_gameboard activeNode] toNode:[_gameboard getGameBoardNodeForGridLocation:retreatToLocation.location]];
                }
                
                [_gameboard deselectActiveNode];
                [_gameboard deHighlightAllNodes];
            }];
        }
        else {
            [ParticleHelper applyBurstToNode:targetNode];
            
            [_gameManager cardHasBeenDefeated:targetNode.card.model];
            [_gameboard replaceCardAtGameBoardNode:targetNode withCard:[_gameboard activeNode].card];
            [self resetUserInterface];
        }
    }];

    [self.delegate afterPerformAction:self]*/
}

@end
