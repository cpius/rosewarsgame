//
//  GameSerializer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/8/13.
//
//

#import "GameSerializer.h"

#import "CardForSerialization.h"
#import "TimedAbilityForSerialization.h"
#import "GCTurnBasedMatchHelper.h"

#import "PathFinderStep.h"
#import "CardPool.h"
#import "AbilityFactory.h"
#import "MoveAction.h"

@interface GameSerializer()

- (NSMutableArray*)serializeCardData:(Game*)game;

@end

@implementation GameSerializer

- (NSMutableArray *)serializeCardData:(Game *)game {
    
    NSMutableArray *cards = [NSMutableArray array];

    for (Card *myCard in game.myDeck.cards) {
        if (!myCard.dead) {
            CardForSerialization *serializeObject = [[CardForSerialization alloc] initWithCard:myCard];
            [cards addObject:[serializeObject asDictionary]];
        }
    }
    
    for (Card *enemyCard in game.enemyDeck.cards) {
        if (!enemyCard.dead) {
            CardForSerialization *serializeObject = [[CardForSerialization alloc] initWithCard:enemyCard];
            [cards addObject:[serializeObject asDictionary]];
        }
    }
    
    return cards;
}

/*- (NSData *)serializeGame:(Game *)game {
    
    NSMutableDictionary *mutableGameData = [NSMutableDictionary dictionary];
    
    [mutableGameData setValue:@(game.state) forKey:@"gamestate"];
    [mutableGameData setValue:@(game.myColor) forKey:game.localUserId];
    [mutableGameData setValue:@(game.numberOfAvailableActions) forKey:@"numberofactions"];
    [mutableGameData setValue:@(game.currentRound) forKey:@"currentround"];
    [mutableGameData setValue:@(game.turnCounter) forKey:@"turncounter"];
    [mutableGameData setValue:@(game.gameOver) forKey:@"gameover"];
    [mutableGameData setValue:@(game.currentPlayersTurn) forKey:@"currentplayersturn"];
    [mutableGameData setValue:@(game.myColor) forKey:@"gamedata_created_by"];
        
    if (game.state == kGameStateFinishedPlacingCards ||
        game.state == kGameStateGameStarted) {
        
        NSMutableArray *cards = [self serializeCardData:game];
        [mutableGameData setValue:[NSArray arrayWithArray:cards] forKey:@"cards"];
    }
    
    if (game.state == kGameStateGameStarted && game.latestBattleReport != nil) {
        
        NSMutableDictionary *action = [NSMutableDictionary dictionary];
        NSMutableArray *path = [NSMutableArray arrayWithCapacity:game.latestBattleReport.pathTaken.count];
        
        [action setValue:@(game.latestBattleReport.actionType) forKey:@"actiontype"];
        
        for (PathFinderStep *step in game.latestBattleReport.pathTaken) {
            [path addObject:[NSDictionary dictionaryWithObjectsAndKeys:@(step.location.row), @"row", @(step.location.column), @"column", nil]];
        }
        
        [action setValue:[NSArray arrayWithArray:path] forKey:@"path"];
        [action setValue:@(game.latestBattleReport.cardInAction.cardLocation.row) forKey:@"cardinaction_row"];
        [action setValue:@(game.latestBattleReport.cardInAction.cardLocation.column) forKey:@"cardinaction_column"];
        [action setValue:@(game.latestBattleReport.enemyCard.cardLocation.row) forKey:@"enemycard_row"];
        [action setValue:@(game.latestBattleReport.enemyCard.cardLocation.column) forKey:@"enemycard_column"];
        
        if (game.latestBattleReport.primaryBattleResult != nil) {
            [action setObject:[game.latestBattleReport.primaryBattleResult asDictionary] forKey:@"primarybattle"];
        }
        
        [mutableGameData setObject:action forKey:@"action"];
    }
    
    NSDictionary *gameData = [NSDictionary dictionaryWithDictionary:mutableGameData];
    
    NSError *error = nil;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:gameData options:kNilOptions error:&error];
    
    return jsonData;
}

- (void)deserializeGameData:(NSData *)gameData toGame:(Game *)game {
    
    NSError *error = nil;
    NSDictionary *data = [NSJSONSerialization JSONObjectWithData:gameData options:NSJSONReadingMutableContainers error:&error];
    
    game.state = [[data objectForKey:@"gamestate"] integerValue];
    game.numberOfAvailableActions = [[data objectForKey:@"numberofactions"] integerValue];
    game.currentRound = [[data objectForKey:@"currentround"] integerValue];
    game.turnCounter = [[data objectForKey:@"turncounter"] integerValue];
    game.gameOver = [[data objectForKey:@"gameover"] boolValue];
    game.currentPlayersTurn = [[data objectForKey:@"currentplayersturn"] integerValue];
    PlayerColors creator = [[data objectForKey:@"gamedata_created_by"] integerValue];
    
    for (GKTurnBasedParticipant *participant in [GCTurnBasedMatchHelper sharedInstance].currentMatch.participants) {
        
        id color = [data valueForKey:participant.playerID];
        
        if (color != nil) {
            
            if ([participant.playerID isEqualToString:[GCTurnBasedMatchHelper sharedInstance].localUserId]) {
                game.myColor = [color integerValue];
                game.enemyColor = OppositeColorOf(game.myColor);
            }
            else {
                game.enemyColor = [color integerValue];
                game.myColor = OppositeColorOf(game.enemyColor);
            }
            
            break;
        }
    }
    
    if (includeCardData) {
        NSMutableArray *myCards = [NSMutableArray array];
        NSMutableArray *enemyCards = [NSMutableArray array];
        
        if (game.state == kGameStateFinishedPlacingCards ||
            game.state == kGameStateGameStarted) {
            
            NSArray *cards = [data objectForKey:@"cards"];
            
            for (NSDictionary *carddata in cards) {
                
                Card *card = [CardPool createCardOfName:[[carddata objectForKey:@"unitname"] integerValue]];
                
                card.cardLocation = [GridLocation gridLocationWithRow:[[carddata objectForKey:@"row"] integerValue]
                                                               column:[[carddata objectForKey:@"column"] integerValue]];
                card.cardColor = [[carddata objectForKey:@"cardcolor"] integerValue];
                card.hitpoints = [[carddata objectForKey:@"hitpoints"] integerValue];
                card.experience = [[carddata objectForKey:@"experience"] integerValue];
                
                [card.attack addRawBonus:[[RawBonus alloc] initWithValue:[[carddata objectForKey:@"attackbonus"] integerValue]]];
                [card.defence addRawBonus:[[RawBonus alloc] initWithValue:[[carddata objectForKey:@"defensebonus"] integerValue]]];
                
                NSArray *abilities = [carddata objectForKey:@"abilities"];
                
                for (NSDictionary *ability in abilities) {
                    [AbilityFactory reapplyExistingAbilityOfType:[[ability objectForKey:@"abilitytype"] integerValue] onCard:card withAbilityData:ability];
                }
                
                [card fromDictionary:[carddata objectForKey:@"card_specific_stats"]];
                
                if ([card isOwnedByMe]) {
                    if (creator == game.enemyColor) {
                        [card.cardLocation flipBacklineFromCurrentBackline:UPPER_BACKLINE];
                    }
                    
                    [myCards addObject:card];
                }
                else {
                    if (creator == game.enemyColor) {
                        [card.cardLocation flipBacklineFromCurrentBackline:LOWER_BACKLINE];
                    }
                    
                    [enemyCards addObject:card];
                }
            }
            
            game.myDeck = [[Deck alloc] initWithCards:myCards];
            game.enemyDeck = [[Deck alloc] initWithCards:enemyCards];
        }
    }
    
    if (game.state == kGameStateGameStarted) {
        
        NSMutableDictionary *action = [data objectForKey:@"action"];
        
        if (action != nil) {
            NSArray *path = [action objectForKey:@"path"];
            NSMutableArray *pathTaken = [NSMutableArray array];
            
            for (NSDictionary *pathStep in path) {
                
                GridLocation *location = [GridLocation gridLocationWithRow:[[pathStep valueForKey:@"row"] integerValue]
                                                                    column:[[pathStep valueForKey:@"column"] integerValue]];
                
                [pathTaken addObject:[[PathFinderStep alloc] initWithLocation:[location flipBacklineFromCurrentBackline:LOWER_BACKLINE]]];
            }
            
            ActionTypes actionType = [[action valueForKey:@"actiontype"] integerValue];
            
            GridLocation *cardInActionLocation = [GridLocation gridLocationWithRow:[[action valueForKey:@"cardinaction_row"] integerValue]
                                                                            column:[[action valueForKey:@"cardinaction_column"] integerValue]];
            
            GridLocation *enemyCardLocation = [GridLocation gridLocationWithRow:[[action valueForKey:@"enemycard_row"] integerValue]
                                                                         column:[[action valueForKey:@"enemycard_column"] integerValue]];
            
            if (actionType == kActionTypeMove) {
                
                // Get card in action from enemy deck
                Card *cardInAction = [game getCardFromDeck:game.enemyDeck locatedAt:[cardInActionLocation flipBacklineFromCurrentBackline:LOWER_BACKLINE]];
                
                // Get enemy card from my deck
                Card *enemyCard = [game getCardFromDeck:game.myDeck locatedAt:[enemyCardLocation flipBacklineFromCurrentBackline:UPPER_BACKLINE]];
                
                game.actionForPlayback = [[MoveAction alloc] initWithPath:pathTaken andCardInAction:cardInAction
                                                            enemyCard:enemyCard];
            }
        }
        else {
            game.actionForPlayback = nil;
        }
    }
}
*/
@end
