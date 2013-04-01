//
//  BattleResult.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/27/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"

@interface BattleResult : NSObject

@property (nonatomic, assign) NSUInteger attackRoll;
@property (nonatomic, assign) NSUInteger defenseRoll;

@property (nonatomic, strong) Card *attackingUnit;
@property (nonatomic, strong) Card *defendingUnit;

@property (nonatomic, assign) CombatOutcome combatOutcome;

- (id)initWithAttacker:(Card*)attacker defender:(Card*)defender;
+ (id)battleResultWithAttacker:(Card*)attacker defender:(Card*)defender;

- (NSDictionary*)asDictionary;

@end
