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

@class GameManager;
@implementation WarOfTheRosesTest

- (void)setUp
{
    [super setUp];
    
    _manager = [GameManager sharedManager];
    
    _attackerFixedStrategy = [FixedDiceStrategy strategy];
    _defenderFixedStrategy = [FixedDiceStrategy strategy];
    
    _manager.attackerDiceStrategy = _attackerFixedStrategy;
    _manager.defenderDiceStrategy = _defenderFixedStrategy;
}

- (void)tearDown
{
    // Tear-down code here.
    
    [super tearDown];
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
    
    STAssertTrue([test isEqualToString:string2], @"Wrong");
    STAssertTrue([test2 isEqualToString:string2], @"Wrong");
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
    
    STAssertFalse([_manager shouldEndTurn], @"shouldEndTurn should return NO");
    
    attacker.hasPerformedActionThisRound = YES;
    
    STAssertTrue([_manager shouldEndTurn], @"shouldEndTurn should return YES");
    
    
}

@end
