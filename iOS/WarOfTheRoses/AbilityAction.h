//
//  AbilityAction.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/19/13.
//
//

#import "Action.h"

@interface AbilityAction : Action

@property (nonatomic, readonly) NSArray *availableAbilities;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card targetCard:(Card *)targetCard;

@end
