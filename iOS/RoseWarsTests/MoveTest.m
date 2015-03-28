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
#import "CardPool.h"

@interface MoveTest()

@property (nonatomic) GameManager *gamemanager;

@end

@implementation MoveTest

- (void)setUp
{
    [super setUp];
    
    self.gamemanager = [[GameManager alloc] init];
}

- (void)testUnitShouldBeBlockedByZocUsingMoveStrategy {
    
    LightCavalry *attacker = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Pikeman *defender2 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *defender3 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:4 column:1];
    defender1.cardLocation = [GridLocation gridLocationWithRow:2 column:1];
    defender2.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender3.cardLocation = [GridLocation gridLocationWithRow:4 column:2];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, defender3, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender2.cardLocation usingStrategy:[PathFinderStrategyFactory getMoveStrategy]];
    
    XCTAssertNil(path, @"Shouldn't be able to move to pikeman because of ZOC");
}

- (void)testUnitShouldBeBlockedByZocUsingMeleeStrategy {
    
    LightCavalry *attacker = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Pikeman *defender2 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *defender3 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:4 column:1];
    defender1.cardLocation = [GridLocation gridLocationWithRow:2 column:1];
    defender2.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender3.cardLocation = [GridLocation gridLocationWithRow:4 column:2];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, defender3, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender2.cardLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackWithConquerStrategy]];
    
    XCTAssertNil(path, @"Shouldn't be able to move to pikeman because of ZOC");
    
}

@end
