//
//  PushAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/5/13.
//
//

#import "PushAction.h"

@implementation PushAction

@synthesize actionType = _actionType;
@synthesize startLocation = _startLocation;
@synthesize battleReport = _battleReport;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card {
    
    self = [super initWithPath:path andCardInAction:card enemyCard:nil];
    
    if (self) {
        _actionType = kActionTypePush;
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
    
    // Push action cost no actionpoints
    return 0;
}

- (void)performActionWithCompletion:(void (^)())completion {
    
    _battleReport = [BattleReport battleReportWithAction:self];
    
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];
    
    [self.delegate action:self wantsToMoveFollowingPath:self.path withCompletion:^(GridLocation *endLocation) {
                
        if (![self.cardInAction.cardLocation isEqual:endLocation]) {
            
            [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:endLocation];
            
            [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:_startLocation toLocation:endLocation];
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
