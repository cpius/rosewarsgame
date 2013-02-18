//
//  Action.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "Action.h"
#import "PathFinderStep.h"

@implementation Action

@synthesize path = _path;
@synthesize cardInAction = _cardInAction;
@synthesize enemyCard = _enemyCard;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super init];
    
    if (self) {
        _path = path;
        _cardInAction = card;
        _enemyCard = enemyCard;
    }
    
    return self;
}

- (BOOL)isWithinRange {
    
    @throw [NSException exceptionWithName:@"Error" reason:@"Musn't call on baseclass" userInfo:nil];
}

- (GridLocation *)getLastLocationInPath {
    
    if (_path != nil && _path.count > 0) {
        return [[_path lastObject] location];
    }
    
    return nil;
}

@end
