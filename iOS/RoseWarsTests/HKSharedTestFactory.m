//
//  HKSharedTestFactory.m
//  RoseWars
//
//  Created by Heine Kristensen on 05/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKSharedTestFactory.h"

#import "HKSharedTestCheckActionExistence.h"

@implementation HKSharedTestFactory

+ (id<HKSharedTestExecuter>)createSharedTestExecuterOfType:(NSString*)type {
    
    if ([type isEqualToString:@"Does action exist"]) {
        return [[HKSharedTestCheckActionExistence alloc] init];
    }
    
    return nil;
}

@end
