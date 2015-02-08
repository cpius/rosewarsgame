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
@synthesize gamemanager = _gamemanager;

- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super initWithGameManager:gamemanager path:path andCardInAction:card enemyCard:enemyCard];
    
    if (self) {
        _gamemanager = gamemanager;
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

    [self.gamemanager willUseAction:self];
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];
    
    [self.delegate action:self wantsToMoveFollowingPath:self.path withCompletion:^(GridLocation *endLocation) {
        
        [self.cardInAction consumeMoves:self.path.count];
        
        if (![self.cardInAction.cardLocation isEqual:endLocation]) {
            
            [self.gamemanager card:self.cardInAction movedToGridLocation:endLocation];
            
            [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:_startLocation toLocation:endLocation];
        }
        
        [self.gamemanager actionUsed:self];
        [self.cardInAction didPerformedAction:self];

        [self.gamemanager.currentGame addBattleReport:_battleReport forAction:self];

        [self.delegate afterPerformAction:self];

        if (completion != nil) {
            completion();
        }
    }];
}

@end
