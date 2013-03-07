//
//  MoveAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "MoveAction.h"
#import "GameManager.h"

@implementation MoveAction

@synthesize actionType = _actionType;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super initWithPath:path andCardInAction:card enemyCard:enemyCard];
    
    if (self) {
        _actionType = kActionTypeMove;
    }
    
    return self;
}

/*- (BOOL)isWithinRange {
    
    return self.path.count <= self.cardInAction.movesRemaining;
}*/

- (BOOL)isAttack {
    
    return NO;
}

- (ActionTypes)actionType {
    
    return kActionTypeMove;
}

- (void)performActionWithCompletion:(void (^)())completion {
    
    [self.delegate beforePerformAction:self];
    
    GridLocation *startLocation = self.cardInAction.cardLocation;

    [self.delegate action:self wantsToMoveFollowingPath:self.path withCompletion:^(GridLocation *endLocation) {
        
        [self.cardInAction consumeMoves:self.path.count];
        
        if (![self.cardInAction.cardLocation isEqual:endLocation]) {
            
            [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:endLocation];
            
            [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:startLocation toLocation:endLocation];
        }
        
        [[GameManager sharedManager] actionUsed:self];
        [self.cardInAction didPerformedAction:self];
        
        [self.delegate afterPerformAction:self];

        if (completion != nil) {
            completion();
        }
    }];
}

@end
