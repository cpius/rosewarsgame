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
    
    return [_actionStrategy decideNextActionFromBattlePlans:_battlePlans];
}

- (void)createBattlePlansForUnits:(NSArray*)units sgainstEnemyUnits:(NSArray*)enemyUnits fromUnitLayout:(NSDictionary*)unitLayout {
    
    [_battlePlans removeAllObjects];
    
    for (Card *unit in units) {
        
        if (!unit.dead) {
            BattlePlan *battlePlan = [[BattlePlan alloc] init];
            [battlePlan createBattlePlanForCard:unit enemyUnits:enemyUnits unitLayout:unitLayout];
            
            [_battlePlans setObject:battlePlan forKey:unit.cardLocation];
        }
    }
}

- (void)placeCardsInDeck:(Deck *)deck {
    
    [deckStrategy placeCardsInDeck:deck inGameBoardSide:kGameBoardUpper];
}



@end
