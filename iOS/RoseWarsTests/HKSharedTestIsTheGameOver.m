//
//  HKSharedTestIsTheGameOver.m
//  RoseWars
//
//  Created by Heine Kristensen on 27/03/15.
//  Copyright (c) 2015 Heine Skov Kristensen. All rights reserved.
//

#import "HKSharedTestIsTheGameOver.h"
#import "Definitions.h"

@implementation HKSharedTestIsTheGameOver

- (BOOL)executeSharedTestWithData:(NSDictionary *)data {
    [super executeSharedTestWithData:data];
    
    self.gamemanager.currentGame.myColor = kPlayerRed;
    
    BOOL expected = [data[@"result"] boolValue];
    
    return ([self.gamemanager checkForEndGame] != kGameResultInProgress) == expected;
}

@end
