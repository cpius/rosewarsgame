//
//  WarElephant.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/15/13.
//
//

#import "Card.h"
#import "BattleStrategy.h"

@interface WarElephant : Card

@property (nonatomic, strong) id<BattleStrategy> aoeBattleStrategy;

+ (id)card;

@end
