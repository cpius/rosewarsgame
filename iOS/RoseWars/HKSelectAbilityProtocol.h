//
//  HKSelectAbilityProtocol.h
//  RoseWars
//
//  Created by Heine Skov Kristensen on 10/2/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import <Foundation/Foundation.h>

@protocol SelectAbilityProtocol <NSObject>

- (void)layer:(SelectAbilityLayer*)layer selectedAbilityRaiseType:(AbilityRaiseTypes)type forCard:(Card*)card;

@end
