//
//  Action.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "Action.h"
#import "PathFinderStep.h"
#import "GameManager.h"
#import "BattleReport.h"
#import "BattleResult.h"

@implementation Action

@synthesize path = _path;
@synthesize cardInAction = _cardInAction;
@synthesize enemyCard = _enemyCard;
@synthesize score = _score;
@synthesize isAttack = _isAttack;
@synthesize isMove = _isMove;
@synthesize delegate = _delegate;
@synthesize actionType = _actionType;
@synthesize startLocation = _startLocation;
@synthesize enemyInitialLocation = _enemyInitialLocation;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super init];
    
    if (self) {
        _path = path;
        _cardInAction = card;
        _enemyCard = enemyCard;
    }
    
    return self;
}

- (BOOL)isMove {
    
    return NO;
}

- (BOOL)isWithinRange {
    
    return [self.cardInAction allowAction:self allLocations:[GameManager sharedManager].currentGame.unitLayout];
}

- (void)performActionWithCompletion:(void (^)())completion {
    
    @throw [NSException exceptionWithName:@"Error" reason:@"Musn't call on baseclass" userInfo:nil];
}

- (GridLocation *)getFirstLocationInPath {
    
    if (_path != nil && _path.count > 0) {
        PathFinderStep *step = [_path objectAtIndex:0];
        return step.location;
    }
    
    return nil;
}

- (GridLocation *)getLastLocationInPath {
    
    if (_path != nil && _path.count > 0) {
        PathFinderStep *step = [_path lastObject];
        return step.location;
    }
    
    return nil;
}

- (GridLocation *)getEntryLocationInPath {
    
    if (_path != nil && _path.count > 1) {
        PathFinderStep *step = [_path objectAtIndex:_path.count - 2];
        return step.location;
    }
    
    if (_path != nil && _path.count == 1) {
        // If path only contains 1 step, the entry location is the cards start location
        return self.startLocation;
    }
    
    return nil;
}


- (ActionTypes)actionType {
    
    @throw [NSException exceptionWithName:@"Error" reason:@"Musn't call on baseclass" userInfo:nil];
}

@end
