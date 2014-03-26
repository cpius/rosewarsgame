//
//  HKSharedTestExecuter.h
//  RoseWars
//
//  Created by Heine Kristensen on 05/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <Foundation/Foundation.h>

@protocol HKSharedTestExecuter <NSObject>

- (BOOL)executeSharedTestWithData:(NSDictionary*)data;

@end
