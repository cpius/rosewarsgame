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
#import "HighMorale.h"
#import "GameManager.h"

@implementation GameCenterTest

/*- (void)testSerializeCurrentGame {
    
    Archer *attacker = [Archer card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    [GameManager sharedManager].currentGame = [TestHelper setupGame:[GameManager sharedManager].currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    [defender1 addTimedAbility:[[HighMorale alloc] initOnCard:defender1]];
    
    NSData *data = [[GameManager sharedManager].currentGame serializeCurrentGame];

    NSString *json = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];    
    CCLOG(@"%@", json);
    
    STAssertNoThrow([[GameManager sharedManager].currentGame serializeCurrentGame], @"Game serialization shouldn't throw exception");
}*/

@end
