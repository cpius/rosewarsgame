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
#import "CardPool.h"

@interface WarOfTheRosesTest()

@property (nonatomic) GameManager *gamemanager;

@end

@class GameManager;
@implementation WarOfTheRosesTest

- (void)setUp
{
    [super setUp];
    
    self.gamemanager = [[GameManager alloc] init];
    
    self.gamemanager.currentGame.myColor = kPlayerGreen;
    self.gamemanager.currentGame.enemyColor = kPlayerRed;
}

- (void)tearDown
{
    // Tear-down code here.
    
    [super tearDown];
}

- (void)testUnitDescriptionName {
    
    Diplomat *diplomant = [CardPool createCardOfName:kDiplomat withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    
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
    
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
        
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObjects:pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:archer]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:4 column:3]]] andCardInAction:pikeman enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
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
        
    LightCavalry *attacker = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    LightCavalry *defender2 = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    defender2.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    XCTAssertFalse([self.gamemanager shouldEndTurn], @"shouldEndTurn should return NO");
    
    attacker.hasPerformedActionThisRound = YES;
    
    XCTAssertTrue([self.gamemanager shouldEndTurn], @"shouldEndTurn should return YES");
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
    
    Diplomat *attacker = [CardPool createCardOfName:kDiplomat withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:UPPER_BACKLINE + 1 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObject:defender1]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    GameResults result = [self.gamemanager checkForEndGame];
    XCTAssertTrue(result == kGameResultInProgress, @"Game should be in progress");
    
    [self.gamemanager card:attacker movedToGridLocation:[GridLocation gridLocationWithRow:UPPER_BACKLINE column:3]];

    result = [self.gamemanager checkForEndGame];
    XCTAssertTrue(result == kGameResultVictory, @"Should result in victory");
}

- (void)testDefeatWhenUnitOnMyBackline {
    
    Diplomat *attacker = [CardPool createCardOfName:kDiplomat withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:LOWER_BACKLINE - 1 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObject:defender1]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    GameResults result = [self.gamemanager checkForEndGame];
    XCTAssertTrue(result == kGameResultInProgress, @"Game should be in progress");
    
    [self.gamemanager card:defender1 movedToGridLocation:[GridLocation gridLocationWithRow:LOWER_BACKLINE column:3]];
    
    result = [self.gamemanager checkForEndGame];
    XCTAssertTrue(result == kGameResultDefeat, @"Should result in victory");
}

- (void)testNoVictoryWhenUnitBribedOnEnemyBackline {
    Diplomat *attacker = [CardPool createCardOfName:kDiplomat withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:UPPER_BACKLINE + 1 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:UPPER_BACKLINE  column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObject:defender1]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    GameResults result = [self.gamemanager checkForEndGame];
    XCTAssertTrue(result == kGameResultInProgress, @"Game should be in progress");
    
    AbilityAction *action = [[AbilityAction alloc] initWithGameManager:self.gamemanager path:@[defender1.cardLocation] andCardInAction:attacker targetCard:defender1];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        
        GameResults result = [self.gamemanager checkForEndGame];
        XCTAssertTrue(result == kGameResultInProgress, @"Game should still be in progress");
    }];
}

@end
