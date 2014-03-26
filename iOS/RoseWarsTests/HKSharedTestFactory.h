//
//  HKSharedTestFactory.h
//  RoseWars
//
//  Created by Heine Kristensen on 05/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "HKSharedTestExecuter.h"

@interface HKSharedTestFactory : NSObject

+ (id<HKSharedTestExecuter>)createSharedTestExecuterOfType:(NSString*)type;

@end
