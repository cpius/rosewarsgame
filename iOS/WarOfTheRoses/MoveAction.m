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
@synthesize startLocation = _startLocation;
@synthesize battleReport = _battleReport;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super initWithPath:path andCardInAction:card enemyCard:enemyCard];
    
    if (self) {
        _actionType = kActionTypeMove;
        _startLocation = card.cardLocation;
    }
    
    return self;
}

- (BOOL)isAttack {
    
    return NO;
}

- (BOOL)isMove {
    
    return YES;
}

- (ActionTypes)actionType {
    
    return _actionType;
}

- (NSUInteger)cost {
    
    return self.cardInAction.moveActionCost;
}

- (void)performActionWithCompletion:(void (^)())completion {
    
    _battleReport = [BattleReport battleReportWithAction:self];

    [[GameManager sharedManager] willUseAction:self];
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];
    
    [self.delegate action:self wantsToMoveFollowingPath:self.path withCompletion:^(GridLocation *endLocation) {
        
        [self.cardInAction consumeMoves:self.path.count];
        
        if (![self.cardInAction.cardLocation isEqual:endLocation]) {
            
            [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:endLocation];
            
            [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:_startLocation toLocation:endLocation];
        }
        
        [[GameManager sharedManager] actionUsed:self];
        [self.cardInAction didPerformedAction:self];

        if (!self.playback) {
            [[GameManager sharedManager].currentGame addBattleReport:_battleReport];
        }

        [self.delegate afterPerformAction:self];

        if (completion != nil) {
            completion();
        }
    }];
}

@end
