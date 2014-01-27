//
//  AIPlayer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/22/13.
//
//

#import "AIPlayer.h"

@interface AIPlayer()


@end

@implementation AIPlayer

@synthesize deckStrategy;
@synthesize actionStrategy = _actionStrategy;

- initWithStrategy:(id<AIStrategy>)strategy {
    
    self = [super init];
    
    if (self) {
        _actionStrategy = strategy;
        _battlePlans = [[NSMutableDictionary alloc] init];
    }
    
    return self;
}

- (Action *)decideNextAction {
    
    NSMutableArray *actions = [NSMutableArray array];
    
    for (id key in _battlePlans.allKeys) {
        
        BattlePlan *battleplan = [_battlePlans objectForKey:key];
        
        [actions addObjectsFromArray:battleplan.moveActions];
        [actions addObjectsFromArray:battleplan.meleeActions];
        [actions addObjectsFromArray:battleplan.rangeActions];
    }
    
    return [_actionStrategy decideNextActionFromActions:[NSArray arrayWithArray:actions]];
}


- (void)placeCardsInDeck:(Deck *)deck {
    
    [deckStrategy placeCardsInDeck:deck inGameBoardSide:kGameBoardUpper];
}

- (void)createBattlePlansForUnits:(NSArray*)units sgainstEnemyUnits:(NSArray*)enemyUnits fromUnitLayout:(NSDictionary*)unitLayout {
    
    [_battlePlans removeAllObjects];
    
    for (Card *unit in units) {
        
        if (!unit.dead) {
            BattlePlan *battlePlan = [[BattlePlan alloc] init];
            [battlePlan createBattlePlanForCard:unit friendlyUnits:units enemyUnits:enemyUnits unitLayout:unitLayout];
            
            [_battlePlans setObject:battlePlan forKey:unit.cardLocation];
        }
    }
}


@end
