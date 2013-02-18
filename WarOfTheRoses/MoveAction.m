//
//  MoveAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "MoveAction.h"

@implementation MoveAction

- (id)initWithPath:(NSArray *)path andCardInAction:(Card*)card {
    
    return [[MoveAction alloc] initWithPath:path andCardInAction:card enemyCard:nil];
}

- (BOOL)isWithinRange {
    
    return self.path.count - 1 <= self.cardInAction.movesRemaining;
}

@end
