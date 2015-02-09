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

@implementation HKSharedTestFactory

+ (id<HKSharedTestExecuter>)createSharedTestExecuterOfType:(NSString*)type {
    
    if ([type isEqualToString:@"Does action exist"]) {
        return [HKSharedTestCheckActionExistence new];
    }
    
    if ([type isEqualToString:@"Is attack and defence correct"]) {
        return [HKSharedTestIsAttackAndDefenseCorrect new];
    }
    
    return nil;
}

@end
