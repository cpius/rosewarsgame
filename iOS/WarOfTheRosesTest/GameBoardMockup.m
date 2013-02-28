//
//  GameBoardMockup.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/28/13.
//
//

#import "GameBoardMockup.h"
#import "PathFinderStep.h"

@implementation GameBoardMockup

- (void)beforePerformAction:(Action *)action {
    
}

- (void)action:(Action *)action hasResolvedRangedCombatWithOutcome:(CombatOutcome)combatOutcome {
    
}

- (void)action:(Action *)action wantsToMoveCard:(Card *)card fromLocation:(GridLocation *)fromLocation toLocation:(GridLocation *)toLocation {
    
}

- (void)action:(Action *)action wantsToMoveFollowingPath:(NSArray *)path withCompletion:(void (^)(GridLocation *))completion {

    completion([path.lastObject location]);
}

- (void)action:(Action *)action wantsToReplaceCardAtLocation:(GridLocation *)replaceLocation withCardAtLocation:(GridLocation *)withLocation {
    
}

- (void)afterPerformAction:(Action *)action {
    
}

@end
