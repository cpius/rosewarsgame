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

/*- (void)testTimedAbilityPersistsThroughEndTurn {
    
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
    
    [attacker addTimedAbility:[[ImproveWeapons alloc] initOnCard:attacker]];
    
    [[GameManager sharedManager] endTurn];

    NSData *data = [[GameManager sharedManager].currentGame serializeCurrentGame];
    
    STAssertTrue([attacker.attack calculateValue].lowerValue == 2, @"Pikeman attack should be 2-6");
    
    [[GameManager sharedManager].currentGame deserializeGameData:data];
    
    attacker = [[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0];
    
    STAssertTrue([attacker.attack calculateValue].lowerValue == 2, @"Pikeman attack should still be 2-6");

    [[GameManager sharedManager] endTurn];

    data = [[GameManager sharedManager].currentGame serializeCurrentGame];

    
    [[GameManager sharedManager].currentGame deserializeGameData:data];

    attacker = [[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0];

    STAssertTrue([attacker.attack calculateValue].lowerValue == 5, @"Pikeman attack should be 5-6");
}
*/
@end
