//
//  BasicUnitTest.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/24/13.
//
//

#import "BasicUnitTest.h"
#import "Definitions.h"
#import "Archer.h"
#import "Pikeman.h"
#import "LightCavalry.h"
#import "Knight.h"
#import "CardPool.h"

@interface BasicUnitTest()

@property (nonatomic, strong) GameManager *gamemanager;

@end

@implementation BasicUnitTest

- (void)setUp
{
    [super setUp];
    
    self.gamemanager = [[GameManager alloc] init];
}

- (void)testArcherBonusAgainstInfantry {
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    XCTAssertTrue([archer.attack calculateValue] == 2, @"Archer base atta2k should be 5");
    
    // Attacker has special against defender
    [archer combatStartingAgainstDefender:pikeman];
    
    XCTAssertTrue([archer.attack calculateValue] == 3, @"Archer should have +1 attack against infantry");
    
    [archer combatFinishedAgainstDefender:pikeman withOutcome:kCombatOutcomeAttackSuccessful];
    
    XCTAssertTrue([archer.attack calculateValue] == 2, @"Archer attack should again be reduced to 2 after attack against infantry");
}

- (void)testPikemanBonusAgainstLightCavalry {
    
    LightCavalry *lightCavalry = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    XCTAssertTrue([pikeman.attack calculateValue] == 2, @"Pikeman base attack should be 2");
    
    // Attacker has special against defender
    [pikeman combatStartingAgainstDefender:lightCavalry];
    
    XCTAssertTrue([pikeman.attack calculateValue] == 3, @"Pikeman should have +1 attack against cavalry");
    
    [pikeman combatFinishedAgainstDefender:pikeman withOutcome:kCombatOutcomeAttackSuccessful];
    
    XCTAssertTrue([pikeman.attack calculateValue] == 2, @"Pikeman attack should again be 2 after attack against cavalry");
}


@end
