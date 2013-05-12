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
#import "AbilityAction.h"
#import "MeleeAttackAction.h"
#import "RangedAttackAction.h"
#import "FixedDiceStrategy.h"
#import "StandardBattleStrategy.h"
#import "FixedLevelIncreaseStrategy.h"
#import "MeleeAttackPlaybackAction.h"

@interface GameSerializer()

- (NSArray*)serializeCardData:(Game*)game;

- (NSMutableDictionary*)serializeBattleReport:(BattleReport*)battleReport;

- (NSArray*)deserializePathFromDictionary:(NSDictionary*)dictionary;
- (Action*)deserializeActionForGame:(Game*)game fromDictionary:(NSDictionary*)dictionary;

- (id<BattleStrategy>)battleStrategyForCard:(Card*)card fromBattleResult:(BattleResult*)battleResult;

- (Card*)getCardInActionFromBattleReportDictionary:(NSDictionary*)dictionary forGame:(Game*)game;
- (Card*)getEnemyCardFromBattleReportDictionary:(NSDictionary*)dictionary forGame:(Game*)game;

@end

@implementation GameSerializer

- (NSArray *)serializeCardData:(Game *)game {
    
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
    
    return [NSArray arrayWithArray:cards];
}

- (void)takeCardSnapshot:(Game *)game state:(CardSnapshotStates)state {

    if (state == kCardSnapshotStateBeforeAction) {
        _cardsBeforeAction = [self serializeCardData:game];
    }
    else {
        _cardsAfterAction = [self serializeCardData:game];
    }
}

- (NSMutableDictionary *)serializeBattleReport:(BattleReport *)battleReport {
    
    NSMutableDictionary *action = [NSMutableDictionary dictionary];
    NSMutableArray *path = [NSMutableArray arrayWithCapacity:battleReport.pathTaken.count];
    
    [action setValue:@(battleReport.actionType) forKey:@"actiontype"];
    
    for (PathFinderStep *step in battleReport.pathTaken) {
        [path addObject:[NSDictionary dictionaryWithObjectsAndKeys:@(step.location.row), @"row", @(step.location.column), @"column", nil]];
    }
    
    [action setValue:[NSArray arrayWithArray:path] forKey:@"path"];
    [action setValue:@(battleReport.locationOfCardInAction.row) forKey:@"cardinaction_row"];
    [action setValue:@(battleReport.locationOfCardInAction.column) forKey:@"cardinaction_column"];
    [action setValue:@(battleReport.locationOfEnemyCard.row) forKey:@"enemycard_row"];
    [action setValue:@(battleReport.locationOfEnemyCard.column) forKey:@"enemycard_column"];
    [action setValue:@(battleReport.levelIncreased) forKey:@"level_increased"];
    [action setValue:@(battleReport.abilityIncreased) forKey:@"ability_increased"];
    
    if (battleReport.primaryBattleResult != nil) {
        [action setObject:[battleReport.primaryBattleResult asDictionary] forKey:@"primarybattle"];
    }
    
    if (battleReport.secondaryBattleReports.count > 0) {
        NSMutableArray *secondaryBattleResults = [NSMutableArray array];
        
        for (BattleReport *secondaryBattleReport in battleReport.secondaryBattleReports) {
            [secondaryBattleResults addObject:[self serializeBattleReport:secondaryBattleReport]];
        }
        
        [action setObject:secondaryBattleResults forKey:@"secondarybattles"];
    }
    
    return action;
}

- (NSData *)serializeGame:(Game *)game forPlayerWithId:(NSString *)playerId {
    
    NSMutableDictionary *mutableGameData = [NSMutableDictionary dictionary];
    
    [mutableGameData setValue:@(game.state) forKey:@"gamestate"];
    [mutableGameData setValue:@(game.myColor) forKey:playerId];
    [mutableGameData setValue:@(game.numberOfAvailableActions) forKey:@"numberofactions"];
    [mutableGameData setValue:@(game.currentRound) forKey:@"currentround"];
    [mutableGameData setValue:@(game.turnCounter) forKey:@"turncounter"];
    [mutableGameData setValue:@(game.gameOver) forKey:@"gameover"];
    [mutableGameData setValue:@(game.currentPlayersTurn) forKey:@"currentplayersturn"];
    [mutableGameData setValue:@(game.myColor) forKey:@"gamedata_created_by"];
        
    if (game.state == kGameStateFinishedPlacingCards ||
        game.state == kGameStateGameStarted) {
        
        [mutableGameData setValue:[self serializeCardData:game] forKey:@"cards"];
        [mutableGameData setValue:_cardsBeforeAction forKey:@"cards_before_action"];
        [mutableGameData setValue:_cardsAfterAction forKey:@"cards_after_action"];
    }
    
    if (game.state == kGameStateGameStarted && game.latestBattleReports.count > 0) {
        
        NSMutableArray *actions = [NSMutableArray array];
        
        for (BattleReport *report in game.latestBattleReports) {
            NSMutableDictionary *action = [self serializeBattleReport:report];
            [actions addObject:action];
        }
        
        [mutableGameData setObject:actions forKey:@"actions"];
    }
    
    NSDictionary *gameData = [NSDictionary dictionaryWithDictionary:mutableGameData];
    
    NSError *error = nil;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:gameData options:kNilOptions error:&error];
    
    return jsonData;
}

- (void)deserializeGameData:(NSData *)gameData forPlayerWithId:(NSString*)playerId allPlayers:(NSArray*)allPlayers toGame:(Game *)game onlyActions:(BOOL)onlyActions onlyEnemyUnits:(BOOL)onlyEnemyUnits {
    
    NSError *error = nil;
    NSDictionary *data = [NSJSONSerialization JSONObjectWithData:gameData options:NSJSONReadingMutableContainers error:&error];
    
    game.state = [[data objectForKey:@"gamestate"] integerValue];
    game.numberOfAvailableActions = [[data objectForKey:@"numberofactions"] integerValue];
    game.currentRound = [[data objectForKey:@"currentround"] integerValue];
    game.turnCounter = [[data objectForKey:@"turncounter"] integerValue];
    BOOL gameover = [[data objectForKey:@"gameover"] boolValue];
    game.currentPlayersTurn = [[data objectForKey:@"currentplayersturn"] integerValue];
    PlayerColors creator = [[data objectForKey:@"gamedata_created_by"] integerValue];
    
    for (NSString *playerName in allPlayers) {
        
        id color = [data valueForKey:playerName];
        
        if (color != nil) {
            
            if ([playerName isEqualToString:playerId]) {
                game.myColor = (PlayerColors)[color integerValue];
                game.enemyColor = OppositeColorOf(game.myColor);
            }
            else {
                PlayerColors playerColor = (PlayerColors)[color integerValue];
                game.enemyColor = playerColor;
                game.myColor = OppositeColorOf(playerColor);
            }
            
            break;
        }
    }
    
    if (!onlyActions) {
        NSMutableArray *myCards = [NSMutableArray array];
        NSMutableArray *enemyCards = [NSMutableArray array];
        
        if (game.state == kGameStateFinishedPlacingCards ||
            game.state == kGameStateGameStarted) {
            
            NSArray *cards;
            if ((game.currentPlayersTurn == game.myColor)) {
                cards = [data objectForKey:@"cards_before_action"];;
            }
            else if (gameover) {
                cards = [data objectForKey:@"cards_after_action"];
                game.gameOver = YES;
            }
            
            if (cards == nil) {
                cards = [data objectForKey:@"cards"];
            }
            
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
                
                [card resetAfterNewRound];
                
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
            
            if (!onlyEnemyUnits) {
                game.myDeck = [[Deck alloc] initWithCards:myCards];
            }

            game.enemyDeck = [[Deck alloc] initWithCards:enemyCards];
        }
    }
    
    if (game.state == kGameStateGameStarted) {
        
        NSArray *actions = [data objectForKey:@"actions"];
        
        [game.actionsForPlayback removeAllObjects];
        [game.latestBattleReports removeAllObjects];

        if (actions != nil) {
            
            for (NSDictionary *action in actions) {
                [game.actionsForPlayback addObject:[self deserializeActionForGame:game fromDictionary:action]];
            }
        }
    }
}

- (Action *)deserializeActionForGame:(Game *)game fromDictionary:(NSDictionary *)dictionary {
    
    Action *action;
    
    ActionTypes actionType = [[dictionary valueForKey:@"actiontype"] integerValue];
    NSArray *pathTaken = [self deserializePathFromDictionary:[dictionary objectForKey:@"path"]];
        
    // Get card in action from enemy deck
    Card *cardInAction = [self getCardInActionFromBattleReportDictionary:dictionary forGame:game];
    Card *enemyCard = [self getEnemyCardFromBattleReportDictionary:dictionary forGame:game];
    
    BOOL levelIncreased = [[dictionary valueForKey:@"level_increased"] boolValue];
    
    if (levelIncreased) {
        LevelIncreaseAbilities abilityIncreased = [[dictionary valueForKey:@"ability_increased"] integerValue];
        
        FixedLevelIncreaseStrategy *levelIncreaseStrategy = [[FixedLevelIncreaseStrategy alloc] init];
        levelIncreaseStrategy.levelIncreaseAbility = abilityIncreased;
        
        cardInAction.levelIncreaseStrategy = levelIncreaseStrategy;
    }
    
    if (actionType == kActionTypeMove) {
        
        action = [[MoveAction alloc] initWithPath:pathTaken andCardInAction:cardInAction
                                                                  enemyCard:enemyCard];
    }
    
    if (actionType == kActionTypeRanged) {
        
        BattleResult *battleresult = [[BattleResult alloc] initWithAttacker:cardInAction defender:enemyCard];
        [battleresult fromDictionary:[dictionary objectForKey:@"primarybattle"]];
        
        cardInAction.battleStrategy = [self battleStrategyForCard:cardInAction fromBattleResult:battleresult];
        
        action = [[RangedAttackAction alloc ] initWithPath:pathTaken andCardInAction:cardInAction enemyCard:enemyCard];
    }
    
    if (actionType == kActionTypeAbility) {
                
        action = [[AbilityAction alloc] initWithPath:pathTaken andCardInAction:cardInAction targetCard:enemyCard];
    }
    
    if (actionType == kActionTypeMelee) {
        
        BattleResult *battleresult = [[BattleResult alloc] initWithAttacker:cardInAction defender:enemyCard];
        [battleresult fromDictionary:[dictionary objectForKey:@"primarybattle"]];
        
        MeleeAttackPlaybackAction *meleeAction = [[MeleeAttackPlaybackAction alloc] initWithPath:pathTaken andCardInAction:cardInAction enemyCard:enemyCard];

        meleeAction.meleeAttackType = battleresult.meleeAttackType;
        meleeAction.battleStrategy = [self battleStrategyForCard:cardInAction fromBattleResult:battleresult];
        
        NSArray *secondaryBattles = [dictionary objectForKey:@"secondarybattles"];
        
        for (NSDictionary *secondaryBattleDictionary in secondaryBattles) {
            
            Card *secondaryEnemy = [self getEnemyCardFromBattleReportDictionary:secondaryBattleDictionary forGame:game];
           
            BattleResult *secondaryBattle = [[BattleResult alloc ]initWithAttacker:cardInAction defender:secondaryEnemy];
            [secondaryBattle fromDictionary:[secondaryBattleDictionary objectForKey:@"primarybattle"]];
            
            BaseBattleStrategy *battleStrategy = [self battleStrategyForCard:cardInAction fromBattleResult:secondaryBattle];
                        
            [meleeAction.secondaryActionsForPlayback setObject:battleStrategy forKey:secondaryEnemy.cardLocation];
        }
        
        action = meleeAction;
    }
    
    return action;
}

- (Card *)getCardInActionFromBattleReportDictionary:(NSDictionary *)dictionary forGame:(Game *)game {
    
    GridLocation *cardInActionLocation = [GridLocation gridLocationWithRow:[[dictionary valueForKey:@"cardinaction_row"] integerValue]
                                                                    column:[[dictionary valueForKey:@"cardinaction_column"] integerValue]];
    
    // Get card in action from enemy deck
    Card *cardInAction = [game getCardFromDeck:game.enemyDeck locatedAt:[cardInActionLocation flipBacklineFromCurrentBackline:LOWER_BACKLINE]];
    
    // If cardInAction is nil, it's probably an enemy ability
    if (cardInAction == nil) {
        cardInAction = [game getCardFromDeck:game.myDeck locatedAt:cardInActionLocation];
    }
    
    return cardInAction;
}

- (Card *)getEnemyCardFromBattleReportDictionary:(NSDictionary *)dictionary forGame:(Game *)game {
    
    GridLocation *enemyCardLocation = [GridLocation gridLocationWithRow:[[dictionary valueForKey:@"enemycard_row"] integerValue]
                                                                 column:[[dictionary valueForKey:@"enemycard_column"] integerValue]];
    // Get enemy card from my deck
    Card *enemyCard = [game getCardFromDeck:game.myDeck locatedAt:[enemyCardLocation flipBacklineFromCurrentBackline:UPPER_BACKLINE]];
    
    // If enemycard is nil, it's probably a friendly ability
    if (enemyCard == nil) {
        enemyCard = [game getCardFromDeck:game.enemyDeck locatedAt:enemyCardLocation];
    }

    return enemyCard;
}

- (NSArray *)deserializePathFromDictionary:(NSDictionary *)dictionary {
    
    NSMutableArray *pathTaken = [NSMutableArray array];
    
    for (NSDictionary *pathStep in dictionary) {
        
        GridLocation *location = [GridLocation gridLocationWithRow:[[pathStep valueForKey:@"row"] integerValue]
                                                            column:[[pathStep valueForKey:@"column"] integerValue]];
        
        [pathTaken addObject:[[PathFinderStep alloc] initWithLocation:[location flipBacklineFromCurrentBackline:LOWER_BACKLINE]]];
    }
    
    return pathTaken;
}

- (id<BattleStrategy>)battleStrategyForCard:(Card*)card fromBattleResult:(BattleResult *)battleResult {
    
    BaseBattleStrategy *battleStrategy = [card newBattleStrategy];
    FixedDiceStrategy *fixedAttackRoll = [FixedDiceStrategy strategy];
    FixedDiceStrategy *fixedDesenseRoll = [FixedDiceStrategy strategy];
    
    fixedAttackRoll.fixedDieValue = battleResult.attackRoll;
    fixedDesenseRoll.fixedDieValue = battleResult.defenseRoll;
    
    battleStrategy.attackerDiceStrategy = fixedAttackRoll;
    battleStrategy.defenderDiceStrategy = fixedDesenseRoll;
    
    return battleStrategy;
}

@end
