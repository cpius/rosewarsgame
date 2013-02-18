//
//  Action.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"

@interface Action : NSObject

@property (nonatomic, readonly) NSArray *path;
@property (nonatomic, readonly) Card *cardInAction;
@property (nonatomic, readonly) Card *enemyCard;

- (id)initWithPath:(NSArray*)path andCardInAction:(Card*)card enemyCard:(Card*)enemyCard;

- (BOOL)isWithinRange;
- (GridLocation*)getLastLocationInPath;

@end
