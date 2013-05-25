//
//  BaseBattleStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/15/13.
//
//

#import <Foundation/Foundation.h>
#import "BattleStrategy.h"
#import "DiceStrategy.h"

@interface BaseBattleStrategy : NSObject <BattleStrategy> {
    
    NSInteger _attackRoll;
    NSInteger _defenseRoll;
    
    AttributeRange _attackValue;
    AttributeRange _defendValue;
}

@property (nonatomic, strong) id<DiceStrategy> attackerDiceStrategy;
@property (nonatomic, strong) id<DiceStrategy> defenderDiceStrategy;

@end
