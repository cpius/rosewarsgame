//
//  BattlePlan.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"

@interface BattlePlan : NSObject

@property (nonatomic, readonly) NSArray *moveActions;
@property (nonatomic, readonly) NSArray *meleeActions;
@property (nonatomic, readonly) NSArray *rangeActions;

- (NSArray*)createBattlePlanForCard:(Card*)card enemyUnits:(NSArray*)enemyUnits unitLayout:(NSDictionary*)unitLayout;

@end
