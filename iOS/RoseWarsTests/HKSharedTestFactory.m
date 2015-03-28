//
//  HKSharedTestFactory.m
//  RoseWars
//
//  Created by Heine Kristensen on 05/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKSharedTestFactory.h"

#import "HKSharedTestCheckActionExistence.h"
#import "HKSharedTestIsAttackAndDefenseCorrect.h"
#import "HKSharedTestIsOutcomeCorrect.h"
#import "HKSharedTestIsTheGameOver.h"

@implementation HKSharedTestFactory

+ (id<HKSharedTestExecuter>)createSharedTestExecuterOfType:(NSString*)type {
    
    if ([type isEqualToString:@"Does action exist"]) {
        return [HKSharedTestCheckActionExistence new];
    }
    
    if ([type isEqualToString:@"Is attack and defence correct"]) {
        return [HKSharedTestIsAttackAndDefenseCorrect new];
    }
    
    if ([type isEqualToString:@"Is outcome correct"]) {
        return [HKSharedTestIsOutcomeCorrect new];
    }
    
    if ([type isEqualToString:@"Is the game over"]) {
        return [HKSharedTestIsTheGameOver new];
    }
    
    return nil;
}

@end
