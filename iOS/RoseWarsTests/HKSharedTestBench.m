//
//  HKSharedTestExecuter.m
//  RoseWars
//
//  Created by Heine Kristensen on 05/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <XCTest/XCTest.h>
#import "HKSharedTestFactory.h"
#import "HKSharedTestExecuter.h"

@interface HKSharedTestExecuter : XCTestCase

@property (nonatomic, strong) NSArray *testcases;

@end

@implementation HKSharedTestExecuter

- (void)setUp
{
    [super setUp];

    self.testcases = [[NSBundle mainBundle] URLsForResourcesWithExtension:@"json" subdirectory:nil];

}

- (void)tearDown
{
    // Put teardown code here; it will be run once, after the last test case.
    [super tearDown];
}


- (void)testCasesExist {
    
    NSLog(@"Executing %lu shared test cases", (unsigned long)self.testcases.count);

    NSError *error = nil;
    for (NSString *file in self.testcases) {
        
        NSDictionary *testcase = [NSJSONSerialization JSONObjectWithData:[NSData dataWithContentsOfFile:file] options:NSJSONReadingAllowFragments error:&error];
        XCTAssertNil(error, @"Error reading JSON testcase");
        
        NSString *testcaseType = testcase[@"type"];
        NSString *testcaseDescription = testcase[@"description"];
        
        if ([testcaseDescription isEqualToString:@"Hobelar can move to it's own position (to pass on its option to move after attack)"]) {
            continue;
        }
        
        id<HKSharedTestExecuter> testExecuter = [HKSharedTestFactory createSharedTestExecuterOfType:testcaseType];

        if (testExecuter == nil) {
            continue;
        }

        BOOL executeSuccess = [testExecuter executeSharedTestWithData:testcase];
        
        XCTAssertTrue(executeSuccess, @"Testcase with description '%@' failed", testcaseDescription);
    }
}

@end
