//
//  MoveTest.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/26/13.
//
//

#import "MoveTest.h"
#import "Definitions.h"
#import "GridLocation.h"
#import "Archer.h"
#import "Pikeman.h"
#import "LightCavalry.h"
#import "GameManager.h"
#import "TestHelper.h"
#import "PathFinder.h"
#import "PathFinderStrategyFactory.h"

@implementation MoveTest

- (void)setUp
{
    [super setUp];
    
    _manager = [GameManager sharedManager];
    
    _attackerFixedStrategy = [FixedDiceStrategy strategy];
    _defenderFixedStrategy = [FixedDiceStrategy strategy];    
}

- (void)testUnitShouldBeBlockedByZocUsingMoveStrategy {
    
    LightCavalry *attacker = [LightCavalry card];
    Pikeman *defender1 = [Pikeman card];
    Pikeman *defender2 = [Pikeman card];
    Archer *defender3 = [Archer card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:4 column:1];
    attacker.cardColor = kCardColorGreen;
    defender1.cardLocation = [GridLocation gridLocationWithRow:2 column:1];
    defender1.cardColor = kCardColorRed;
    defender2.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender2.cardColor = kCardColorRed;
    defender3.cardLocation = [GridLocation gridLocationWithRow:4 column:2];
    defender3.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, defender3, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender2.cardLocation usingStrategy:[PathFinderStrategyFactory getMoveStrategy] allLocations:_manager.currentGame.unitLayout];
    
    XCTAssertNil(path, @"Shouldn't be able to move to pikeman because of ZOC");
}

- (void)testUnitShouldBeBlockedByZocUsingMeleeStrategy {
    
    LightCavalry *attacker = [LightCavalry card];
    Pikeman *defender1 = [Pikeman card];
    Pikeman *defender2 = [Pikeman card];
    Archer *defender3 = [Archer card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:4 column:1];
    attacker.cardColor = kCardColorGreen;
    defender1.cardLocation = [GridLocation gridLocationWithRow:2 column:1];
    defender1.cardColor = kCardColorRed;
    defender2.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender2.cardColor = kCardColorRed;
    defender3.cardLocation = [GridLocation gridLocationWithRow:4 column:2];
    defender3.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, defender3, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender2.cardLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackWithConquerStrategy] allLocations:_manager.currentGame.unitLayout];
    
    XCTAssertNil(path, @"Shouldn't be able to move to pikeman because of ZOC");
    
}

@end
