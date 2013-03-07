//
//  Action.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"
#import "GridLocation.h"

@class Action;
@class GameManager;
@protocol ActionDelegate <NSObject>

- (void)beforePerformAction:(Action*)action;

- (void)action:(Action*)action wantsToMoveCard:(Card*)card fromLocation:(GridLocation*)fromLocation toLocation:(GridLocation*)toLocation;
- (void)action:(Action*)action wantsToMoveFollowingPath:(NSArray*)path withCompletion:(void (^)(GridLocation*))completion;
- (void)action:(Action*)action hasResolvedRangedCombatWithOutcome:(CombatOutcome)combatOutcome;
- (void)action:(Action*)action wantsToReplaceCardAtLocation:(GridLocation*)replaceLocation withCardAtLocation:(GridLocation*)withLocation;

- (void)afterPerformAction:(Action*)action;

@end

@class Card;
@interface Action : NSObject

@property (nonatomic, weak) id<ActionDelegate> delegate;
@property (nonatomic, strong) NSArray *path;
@property (nonatomic, readonly) Card *cardInAction;
@property (nonatomic, readonly) Card *enemyCard;

@property (nonatomic, assign) NSUInteger score;
@property (nonatomic, readonly) BOOL isAttack;

@property (nonatomic, readonly) ActionTypes actionType;

- (id)initWithPath:(NSArray*)path andCardInAction:(Card*)card enemyCard:(Card*)enemyCard;

- (BOOL)isWithinRange;
- (GridLocation*)getLastLocationInPath;
- (GridLocation *)getEntryLocationInPath;

- (void)performActionWithCompletion:(void (^)())completion;

@end
