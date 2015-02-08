//
//  AbilityAction.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/19/13.
//
//

#import "Action.h"

@class GameManager;
@interface AbilityAction : Action

@property (nonatomic, readonly) NSArray *availableAbilities;
@property (nonatomic, readonly) TimedAbility *abilityUsed;

- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card targetCard:(Card *)targetCard;

@end
