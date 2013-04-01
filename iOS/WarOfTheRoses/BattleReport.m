//
//  BattleReport.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/27/13.
//
//

#import "BattleReport.h"

@implementation BattleReport

- (id)initWithAction:(Action*)action {
    
    self = [super init];
    
    if (self) {
        _pathTaken = action.path;
        _cardInAction = action.cardInAction;
        _enemyCard = action.enemyCard;
        _actionType = action.actionType;
    }
    
    return self;
}

+ (id)battleReportWithAction:(Action*)action {
    
    return [[BattleReport alloc] initWithAction:action];
}

@end
