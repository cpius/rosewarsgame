//
//  WarOfTheRosesTest.m
//  WarOfTheRosesTest
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "WarOfTheRosesTest.h"
#import "GridLocation.h"
#import "Definitions.h"
#import "Archer.h"
#import "Pikeman.h"
#import "LightCavalry.h"
#import "GameManager.h"
#import "MoveAction.h"
#import "TestHelper.h"
#import "MeleeAttackAction.h"
#import "PathFinderStep.h"
#import "Diplomat.h"
#import "AbilityAction.h"
#import "GameBoardMockup.h"

@class GameManager;
@implementation WarOfTheRosesTest

- (void)setUp
{
    [super setUp];
    
    _manager = [GameManager sharedManager];
    
    _manager.currentGame.myColor = kPlayerGreen;
    _manager.currentGame.enemyColor = kPlayerRed;

    _attackerFixedStrategy = [FixedDiceStrategy strategy];
    _defenderFixedStrategy = [FixedDiceStrategy strategy];
}

- (void)tearDown
{
    // Tear-down code here.
    
    [super tearDown];
}

- (void)testUnitDescriptionName {
    
    Diplomat *diplomant = [Diplomat card];
    
    XCTAssertTrue([diplomant.unitDescriptionName isEqualToString:@"Diplomat"], @"UnitDescription should be Diplomat");
}

- (void)testGridLocationHash {
    
    GridLocation *location1 = [GridLocation gridLocationWithRow:1 column:1];
    GridLocation *location2 = [GridLocation gridLocationWithRow:1 column:1];
    
    NSMutableDictionary *dic = [NSMutableDictionary dictionaryWithCapacity:2];
    
    NSString *string1 = @"string1";
    NSString *string2 = @"string2";
    
    [dic setObject:string1 forKey:location1];
    [dic setObject:string2 forKey:location2];
    
    NSString *test = [dic objectForKey:location1];
    NSString *test2 = [dic objectForKey:location2];
    
    XCTAssertTrue([test isEqualToString:string2], @"Wrong");
    XCTAssertTrue([test2 isEqualToString:string2], @"Wrong");
}

- (void)testValidPushLocation {
    
    GridLocation *myLocation = [GridLocation gridLocationWithRow:1 column:3];
    GridLocation *enemyLocation = [GridLocation gridLocationWithRow:2 column:3];
    GridLocation *pushLocation = [enemyLocation getPushLocationForGridLocationWhenComingFromGridLocation:myLocation];
    
    XCTAssertTrue(pushLocation.row == 3, @"Should push unit to row 3");
    XCTAssertTrue(pushLocation.column == 3, @"Should push unit to row 3");
}

- (void)testInvalidPushLocation {
    
    GridLocation *myLocation = [GridLocation gridLocationWithRow:1 column:4];
    GridLocation *enemyLocation = [GridLocation gridLocationWithRow:1 column:5];
    GridLocation *pushLocation = [enemyLocation getPushLocationForGridLocationWhenComingFromGridLocation:myLocation];

    XCTAssertNil(pushLocation, @"Push location should be nil, because it's outside gameboard");
}


- (void)testGridLocationEntryPointWithOnlyOneStepInPath {
    
    Pikeman *pikeman = [Pikeman card];
    Archer *archer = [Archer card];
        
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObjects:pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:archer]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:4 column:3]]] andCardInAction:pikeman enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
    GridLocation *entryLocation = [meleeAction getEntryLocationInPath];
    
    XCTAssertTrue(entryLocation.row == 3, @"Entry location should be pikemans current cardlocation");
    XCTAssertTrue(entryLocation.column == 3, @"Entry location should be pikemans current cardlocation");

    GridLocation *lastLocation = [meleeAction getLastLocationInPath];
    
    XCTAssertTrue(lastLocation.row == 4, @"Last location should be archers cardlocation");
    XCTAssertTrue(lastLocation.column == 3, @"Last location should be archers cardlocation");
    
    GridLocation *firstLocation = [meleeAction getFirstLocationInPath];

    XCTAssertTrue(firstLocation.row == 4, @"First location should be archers cardlocation");
    XCTAssertTrue(firstLocation.column == 3, @"First location should be archers cardlocation");
}

- (void)testShouldEndTurnIfOnlyOneUnitLeftWithInsufficientActions {
        
    LightCavalry *attacker = [LightCavalry card];
    Pikeman *defender1 = [Pikeman card];
    LightCavalry *defender2 = [LightCavalry card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    attacker.cardColor = kCardColorGreen;
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    defender1.cardColor = kCardColorRed;
    defender2.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    defender2.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    XCTAssertFalse([_manager shouldEndTurn], @"shouldEndTurn should return NO");
    
    attacker.hasPerformedActionThisRound = YES;
    
    XCTAssertTrue([_manager shouldEndTurn], @"shouldEndTurn should return YES");
}

- (void)testFlipBackline {
    
    GridLocation *firstLocation = [[GridLocation gridLocationWithRow:3 column:3] flipBacklineFromCurrentBackline:UPPER_BACKLINE];
    XCTAssertTrue(firstLocation.column == 3, @"Column stays the same after flip");
    XCTAssertTrue(firstLocation.row == 6, @"Row should be 6 after flip");
    
    GridLocation *secondLocation = [[GridLocation gridLocationWithRow:8 column:1] flipBacklineFromCurrentBackline:LOWER_BACKLINE];
    XCTAssertTrue(secondLocation.column == 1, @"Column stays the same after flip");
    XCTAssertTrue(secondLocation.row == 1, @"Row should be 1 after flip");
}

- (void)testVictoryWhenUnitOnEnemyBackline {
    
    Diplomat *attacker = [Diplomat card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:UPPER_BACKLINE + 1 column:3];
    attacker.cardColor = kCardColorGreen;
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    defender1.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObject:defender1]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    GameResults result = [_manager checkForEndGame];
    XCTAssertTrue(result == kGameResultInProgress, @"Game should be in progress");
    
    [_manager card:attacker movedToGridLocation:[GridLocation gridLocationWithRow:UPPER_BACKLINE column:3]];

    result = [_manager checkForEndGame];
    XCTAssertTrue(result == kGameResultVictory, @"Should result in victory");
}

- (void)testDefeatWhenUnitOnMyBackline {
    
    Diplomat *attacker = [Diplomat card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardColor = kCardColorGreen;
    attacker.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    defender1.cardColor = kCardColorRed;
    defender1.cardLocation = [GridLocation gridLocationWithRow:LOWER_BACKLINE - 1 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObject:defender1]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    GameResults result = [_manager checkForEndGame];
    XCTAssertTrue(result == kGameResultInProgress, @"Game should be in progress");
    
    [_manager card:defender1 movedToGridLocation:[GridLocation gridLocationWithRow:LOWER_BACKLINE column:3]];
    
    result = [_manager checkForEndGame];
    XCTAssertTrue(result == kGameResultDefeat, @"Should result in victory");
}

- (void)testNoVictoryWhenUnitBribedOnEnemyBackline {
    
    Diplomat *attacker = [Diplomat card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardColor = kCardColorGreen;
    attacker.cardLocation = [GridLocation gridLocationWithRow:UPPER_BACKLINE + 1 column:3];
    
    defender1.cardColor = kCardColorRed;
    defender1.cardLocation = [GridLocation gridLocationWithRow:UPPER_BACKLINE  column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObject:defender1]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    GameResults result = [_manager checkForEndGame];
    XCTAssertTrue(result == kGameResultInProgress, @"Game should be in progress");
    
    AbilityAction *action = [[AbilityAction alloc] initWithPath:@[[GridLocation gridLocationWithRow:UPPER_BACKLINE column:3]] andCardInAction:attacker targetCard:defender1];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        
        GameResults result = [_manager checkForEndGame];
        XCTAssertTrue(result == kGameResultInProgress, @"Game should still be in progress");
    }];
}

@end
