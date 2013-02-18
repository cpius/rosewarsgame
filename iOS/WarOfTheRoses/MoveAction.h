//
//  MoveAction.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import <Foundation/Foundation.h>
#import "Action.h"

@interface MoveAction : Action

- (id)initWithPath:(NSArray*)path andCardInAction:(Card*)card;

@end
