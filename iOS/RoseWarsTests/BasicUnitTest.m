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
#import "HeavyCavalry.h"

@implementation BasicUnitTest

- (void)testArcherBonusAgainstInfantry {
    
    Archer *archer = [Archer card];
    Pikeman *pikeman = [Pikeman card];
    
    XCTAssertTrue([archer.attack calculateValue].lowerValue == 5, @"Archer lowerValye base attack should be 5");
    
    // Attacker has special against defender
    [archer combatStartingAgainstDefender:pikeman];
    
    XCTAssertTrue([archer.attack calculateValue].lowerValue == 4, @"Archer should have +1 attack against infantry");
    
    [archer combatFinishedAgainstDefender:pikeman withOutcome:kCombatOutcomeAttackSuccessful];
    
    XCTAssertTrue([archer.attack calculateValue].lowerValue == 5, @"Archer lowerValue attack should again be reduced to 5 after attack against infantry");
}

- (void)testPikemanBonusAgainstLightCavalry {
    
    LightCavalry *lightCavalry = [LightCavalry card];
    Pikeman *pikeman = [Pikeman card];
    
    XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 5, @"Pikeman lowerValue base attack should be 5");
    
    // Attacker has special against defender
    [pikeman combatStartingAgainstDefender:lightCavalry];
    
    XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 4, @"Pikeman should have +1 attack against cavalry");
    
    [pikeman combatFinishedAgainstDefender:pikeman withOutcome:kCombatOutcomeAttackSuccessful];
    
    XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 5, @"Pikeman lowerValue attack should again be 5 after attack against cavalry");
}


@end
