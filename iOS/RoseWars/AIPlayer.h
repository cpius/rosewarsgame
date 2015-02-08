//
//  AIPlayer.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/22/13.
//
//

#import <Foundation/Foundation.h>
#import "DeckStrategy.h"
#import "Deck.h"
#import "Action.h"
#import "AIStrategy.h"

@interface AIPlayer : NSObject {
    
@protected
    NSMutableDictionary *_battlePlans;
}

@property (nonatomic, strong) id<DeckStrategy> deckStrategy;
@property (nonatomic, strong) id<AIStrategy> actionStrategy;

- initWithStrategy:(id<AIStrategy>)strategy gameManager:(GameManager*)gamemanager;

- (void)placeCardsInDeck:(Deck*)deck;
- (Action *)decideNextAction;
- (void)createBattlePlansForUnits:(NSArray*)units sgainstEnemyUnits:(NSArray*)enemyUnits fromUnitLayout:(NSDictionary*)unitLayout;

@end
