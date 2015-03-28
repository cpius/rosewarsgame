//
//  HKSharedTestBaseExecuter.h
//  RoseWars
//
//  Created by Heine Kristensen on 05/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <XCTest/XCTest.h>
#import <Foundation/Foundation.h>
#import "HKSharedTestExecuter.h"

@interface HKSharedTestBaseExecuter : XCTestCase <HKSharedTestExecuter>

@property (nonatomic, strong) GameManager *gamemanager;

- (GridLocation*)convertLocation:(NSString*)location;
- (BOOL)evaluateOutcomeFromExpectedOutcome:(BOOL)expectedOutcome actualOutcome:(BOOL)actualOutcome;

- (void)setupBoardWithPlayer1Units:(NSDictionary*)player1UnitData player2Units:(NSDictionary*)player2UnitData;

@end
