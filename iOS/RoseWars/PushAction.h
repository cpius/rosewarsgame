//
//  PushAction.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/5/13.
//
//

#import "Action.h"

@interface PushAction : Action

- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card;

+ (void)performPushFromAction:(Action*)action gameManager:(GameManager*)gamemanager withCompletion:(void (^)())completion;

@end
