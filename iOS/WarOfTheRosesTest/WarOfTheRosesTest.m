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

@class GameManager;
@implementation WarOfTheRosesTest

- (void)setUp
{
    [super setUp];
    
    _manager = [GameManager sharedManager];
    
    _attackerFixedStrategy = [FixedDiceStrategy strategy];
    _defenderFixedStrategy = [FixedDiceStrategy strategy];
    
    _attackerFixedDeckStrategy = [FixedDeckStrategy strategy];
    _defenderFixedDeckStrategy = [FixedDeckStrategy strategy];
    
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
    
    NSMutableDictionary *unitLayout = [[NSMutableDictionary alloc] init];
    [_attackerFixedDeckStrategy.fixedCards removeAllObjects];
    [_defenderFixedDeckStrategy.fixedCards removeAllObjects];
    
    LightCavalry *attacker = [LightCavalry card];
    Pikeman *defender1 = [Pikeman card];
    LightCavalry *defender2 = [LightCavalry card];
    
    [unitLayout setObject:attacker forKey:[GridLocation gridLocationWithRow:3 column:3]];
    [unitLayout setObject:defender1 forKey:[GridLocation gridLocationWithRow:6 column:3]];
    [unitLayout setObject:defender2 forKey:[GridLocation gridLocationWithRow:5 column:3]];
    
    [_attackerFixedDeckStrategy.fixedCards addObject:attacker];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    _manager.currentGame.myDeck = _manager.currentGame.myDeck = [_attackerFixedDeckStrategy generateNewDeckWithNumberOfBasicType:0 andSpecialType:0 cardColor:0];
    
    [_defenderFixedDeckStrategy.fixedCards removeAllObjects];
    
    [_defenderFixedDeckStrategy.fixedCards addObject:defender1];
    [_defenderFixedDeckStrategy.fixedCards addObject:defender2];
    
    _manager.currentGame.enemyDeck = [_defenderFixedDeckStrategy generateNewDeckWithNumberOfBasicType:0 andSpecialType:0 cardColor:0];
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    STAssertFalse([_manager shouldEndTurn], @"shouldEndTurn should return NO");
    
    [attacker consumeAllMoves];
    attacker.hasMovedThisRound = YES;
    _manager.currentGame.numberOfAvailableActions--;
    
    STAssertTrue([_manager shouldEndTurn], @"shouldEndTurn should return YES");
    
    
}

@end
