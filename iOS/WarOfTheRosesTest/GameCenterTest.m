//
//  GameCenterTest.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/25/13.
//
//

#import "GameCenterTest.h"

#import "Definitions.h"
#import "Archer.h"
#import "Pikeman.h"
#import "TestHelper.h"
#import "ImproveWeapons.h"
#import "GameManager.h"
#import "AbilityFactory.h"
#import "LongSwordsMan.h"
#import "FixedDiceStrategy.h"
#import "Samurai.h"
#import "StandardBattleStrategy.h"
#import "MeleeAttackAction.h"
#import "PathFinderStep.h"
#import "GameBoardMockup.h"

@implementation GameCenterTest

- (void)setUp
{
    [super setUp];
    
    [[GameManager sharedManager] startNewGameOfType:kGameTypeSinglePlayer];
    [GameManager sharedManager].currentGame.localUserId = @"localuser";
}

- (void)tearDown
{
    // Tear-down code here.
    
    [super tearDown];
}

- (void)testTimedAbilityPersistsThroughEndTurn {
    
    Pikeman *attacker = [Pikeman card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    attacker.cardColor = kCardColorGreen;
    
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    defender1.cardColor = kCardColorRed;
    
    [GameManager sharedManager].currentGame.myColor = kPlayerGreen;
    [GameManager sharedManager].currentGame = [TestHelper setupGame:[GameManager sharedManager].currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    [GameManager sharedManager].currentGame.state = kGameStateGameStarted;
    
    [AbilityFactory addAbilityOfType:kAbilityImprovedWeapons onCard:attacker];
    
    [[GameManager sharedManager] endTurn];

    NSData *data = [[GameManager sharedManager].currentGame serializeCurrentGameForPlayerWithId:@"TestPlayerId"];
    
    STAssertTrue([attacker.attack calculateValue].lowerValue == 2, @"Pikeman attack should be 2-6");
    
    [[GameManager sharedManager].currentGame deserializeGameData:data forPlayerWithId:@"TestPlayerId" allPlayers:@[@"TestPlayerId", @"TestPlayerId2"] onlyActions:NO onlyEnemyUnits:NO];
    
    attacker = [[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0];
    
    STAssertTrue([attacker.attack calculateValue].lowerValue == 2, @"Pikeman attack should still be 2-6");

    [[GameManager sharedManager] endTurn];

    data = [[GameManager sharedManager].currentGame serializeCurrentGameForPlayerWithId:@"TestPlayerId"];

    
    [[GameManager sharedManager].currentGame deserializeGameData:data forPlayerWithId:@"TestPlayerId" allPlayers:@[@"TestPlayerId", @"TestPlayerId2"] onlyActions:NO onlyEnemyUnits:NO];

    attacker = [[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0];

    STAssertTrue([attacker.attack calculateValue].lowerValue == 5, @"Pikeman attack should be 5-6");
}

- (void)testReplayOfSamuraiSecondaryAttacks {
    
    Samurai *samurai = [Samurai card];
    Pikeman *defender1 = [Pikeman card];
    
    samurai.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    samurai.cardColor = kCardColorGreen;
    
    defender1.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardColor = kCardColorRed;
    
    [GameManager sharedManager].currentGame.myColor = kPlayerGreen;
    [GameManager sharedManager].currentGame = [TestHelper setupGame:[GameManager sharedManager].currentGame
                                                   withPlayer1Units:[NSArray arrayWithObject:samurai]
                                                       player2Units:[NSArray arrayWithObject:defender1]];
    
    [GameManager sharedManager].currentGame.state = kGameStateGameStarted;
    
    StandardBattleStrategy *battleStrategy = [StandardBattleStrategy strategy];
    
    battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
    battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:2];
    
    samurai.battleStrategy = battleStrategy;
    
    PathFinderStep *step = [[PathFinderStep alloc] initWithLocation:defender1.cardLocation];
    MeleeAttackAction *firstAttack = [[MeleeAttackAction alloc] initWithPath:@[step] andCardInAction:samurai enemyCard:defender1 meleeAttackType:kMeleeAttackTypeNormal];
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    firstAttack.delegate = mock;
    
    [firstAttack performActionWithCompletion:^{
        
        MeleeAttackAction *secondAttack = [[MeleeAttackAction alloc] initWithPath:@[step] andCardInAction:samurai enemyCard:defender1 meleeAttackType:kMeleeAttackTypeNormal];
        secondAttack.delegate = mock;
        
        samurai.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
        samurai.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
        
        [secondAttack performActionWithCompletion:^{
           
            STAssertTrue([GameManager sharedManager].currentGame.latestBattleReports.count == 2, @"2 actions were performed");
            
            NSData *data = [[GameManager sharedManager].currentGame serializeCurrentGameForPlayerWithId:@"TestPlayerId"];
            [[GameManager sharedManager] endTurn];
            
            [TestHelper swapBoardInGame:[GameManager sharedManager].currentGame myCurrentGameBoardSide:kGameBoardLower];
            
            [[GameManager sharedManager].currentGame deserializeGameData:data forPlayerWithId:@"TestPlayerId" allPlayers:@[@"TestPlayerId", @"TestPlayerId2"] onlyActions:YES onlyEnemyUnits:NO];
            
            STAssertTrue([GameManager sharedManager].currentGame.actionsForPlayback.count == 2, @"Should contain 2 actions for playback");
            
            for (Action *action in [GameManager sharedManager].currentGame.actionsForPlayback) {
                
                action.playback = YES;
                action.delegate = mock;
                
                [action performActionWithCompletion:^{
                    
                }];
            }
        }];
    }];
}

@end
