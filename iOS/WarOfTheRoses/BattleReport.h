//
//  BattleReport.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/27/13.
//
//

#import <Foundation/Foundation.h>
#import "BattleResult.h"
#import "Action.h"

@interface BattleReport : NSObject

@property (nonatomic, readonly) NSArray *pathTaken;
@property (nonatomic, readonly) Card* cardInAction;
@property (nonatomic, readonly) Card* enemyCard;
@property (nonatomic, readonly) ActionTypes actionType;

@property (nonatomic, strong) BattleResult *primaryBattleResult;
@property (nonatomic, assign) NSMutableArray *secondaryBattleResults;

- (id)initWithAction:(Action*)action;
+ (id)battleReportWithAction:(Action*)action;

@end
