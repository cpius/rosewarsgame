//
//  BattleReport.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/27/13.
//
//

#import "BattleReport.h"
#import "GridLocation.h"

@implementation BattleReport

- (id)initWithAction:(Action*)action {
    
    self = [super init];
    
    if (self) {
        _pathTaken = action.path;
        _locationOfCardInAction = [GridLocation gridLocationWithRow:action.cardInAction.cardLocation.row column:action.cardInAction.cardLocation.column];
        _locationOfEnemyCard = [GridLocation gridLocationWithRow:action.enemyCard.cardLocation.row column:action.enemyCard.cardLocation.column];
        _actionType = action.actionType;
        
        _secondaryBattleReports = [NSMutableArray array];
    }
    
    return self;
}

+ (id)battleReportWithAction:(Action*)action {
    
    return [[BattleReport alloc] initWithAction:action];
}

@end
