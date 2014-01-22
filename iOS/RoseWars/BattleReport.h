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

@class GridLocation;
@interface BattleReport : NSObject

@property (nonatomic, readonly) NSArray *pathTaken;
@property (nonatomic, readonly) GridLocation* locationOfCardInAction;
@property (nonatomic, readonly) GridLocation* locationOfEnemyCard;
@property (nonatomic, readonly) ActionTypes actionType;

@property (nonatomic, strong) BattleResult *primaryBattleResult;

@property (nonatomic, strong) NSMutableArray *secondaryBattleReports;

@property (nonatomic, assign) BOOL levelIncreased;
@property (nonatomic, assign) LevelIncreaseAbilities abilityIncreased;

- (id)initWithAction:(Action*)action;
+ (id)battleReportWithAction:(Action*)action;

@end
