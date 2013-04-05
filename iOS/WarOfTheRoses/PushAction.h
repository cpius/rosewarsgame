//
//  PushAction.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/5/13.
//
//

#import "Action.h"

@interface PushAction : Action

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card;

@end
