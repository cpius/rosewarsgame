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
#import "Longswordsman.h"
#import "FixedDiceStrategy.h"
#import "Samurai.h"
#import "StandardBattleStrategy.h"
#import "MeleeAttackAction.h"
#import "PathFinderStep.h"
#import "GameBoardMockup.h"
#import "Diplomat.h"
#import "AbilityAction.h"
#import "CardPool.h"

@interface GameCenterTest()

@property (nonatomic) GameManager *gamemanager;

@end

@implementation GameCenterTest

- (void)setUp
{
    [super setUp];
    
    self.gamemanager = [[GameManager alloc] init];
    [self.gamemanager startNewGameOfType:kGameTypeSinglePlayer];
    self.gamemanager.currentGame.localUserId = @"localuser";
}

- (void)tearDown
{
    // Tear-down code here.
    
    [super tearDown];
}

- (void)testTimedAbilityPersistsThroughEndTurn {
    
    Pikeman *attacker = [CardPool createCardOfName:kPikeman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    self.gamemanager.currentGame.myColor = kPlayerGreen;
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    self.gamemanager.currentGame.state = kGameStateGameStarted;
    
    [AbilityFactory addAbilityOfType:kAbilityImprovedWeapons onCard:attacker];
    
    [self.gamemanager endTurn];

    NSData *data = [self.gamemanager.currentGame serializeCurrentGameForPlayerWithId:@"TestPlayerId"];
    
    XCTAssertTrue([attacker.attack calculateValue].lowerValue == 2, @"Pikeman attack should be 2-6");
    
    [self.gamemanager.currentGame deserializeGameData:data forPlayerWithId:@"TestPlayerId" allPlayers:@[@"TestPlayerId", @"TestPlayerId2"] onlyActions:NO onlyEnemyUnits:NO];
    
    attacker = [self.gamemanager.currentGame.myDeck.cards objectAtIndex:0];
    
    XCTAssertTrue([attacker.attack calculateValue].lowerValue == 2, @"Pikeman attack should still be 2-6");

    [self.gamemanager endTurn];

    data = [self.gamemanager.currentGame serializeCurrentGameForPlayerWithId:@"TestPlayerId"];

    
    [self.gamemanager.currentGame deserializeGameData:data forPlayerWithId:@"TestPlayerId" allPlayers:@[@"TestPlayerId", @"TestPlayerId2"] onlyActions:NO onlyEnemyUnits:NO];

    attacker = [self.gamemanager.currentGame.myDeck.cards objectAtIndex:0];

    XCTAssertTrue([attacker.attack calculateValue].lowerValue == 5, @"Pikeman attack should be 5-6");
}


- (void)testDiplomatCannotBribeTheSameUnitTwoRoundsInARowInMultiplayerGame {
    
    Diplomat *diplomat = [CardPool createCardOfName:kDiplomat withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    diplomat.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    
    self.gamemanager.currentGame.myColor = kPlayerGreen;
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                                   withPlayer1Units:[NSArray arrayWithObject:diplomat]
                                                       player2Units:[NSArray arrayWithObject:defender1]];
    
    self.gamemanager.currentGame.state = kGameStateGameStarted;
    
    XCTAssertTrue([diplomat isValidTarget:defender1], @"Diplomat should be able to bribe pikeman");
    
    PathFinderStep *step = [[PathFinderStep alloc] initWithLocation:defender1.cardLocation];
    
    AbilityAction *bribeAction = [[AbilityAction alloc] initWithGameManager:self.gamemanager path:@[step] andCardInAction:diplomat targetCard:defender1];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    bribeAction.delegate = mock;
    
    [bribeAction performActionWithCompletion:^{
        
        XCTAssertTrue([defender1 isAffectedByAbility:kAbilityBribe], @"Pikeman should be affected by bribe");

        NSData *data = [self.gamemanager.currentGame serializeCurrentGameForPlayerWithId:@"TestPlayerId"];
        [self.gamemanager endTurn];
        
        [TestHelper swapBoardInGame:self.gamemanager.currentGame myCurrentGameBoardSide:kGameBoardLower];
        
        [self.gamemanager.currentGame deserializeGameData:data forPlayerWithId:@"TestPlayerId" allPlayers:@[@"TestPlayerId", @"TestPlayerId2"] onlyActions:NO onlyEnemyUnits:NO];
        
        XCTAssertFalse([defender1 isAffectedByAbility:kAbilityBribe], @"Pikeman should no longer be affected by bribe");
        XCTAssertTrue([defender1 isAffectedByAbility:kAbilityCoolDown], @"Pikeman should be affected by cooldown");
        XCTAssertFalse([diplomat isValidTarget:defender1], @"Diplomat shouldn't be able to bribe pikeman");
    }];
}

@end
