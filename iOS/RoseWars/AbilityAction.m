//
//  AbilityAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/19/13.
//
//

#import "AbilityAction.h"
#import "AbilityFactory.h"
#import "GameManager.h"

@interface AbilityAction()

@end

@implementation AbilityAction

@synthesize actionType = _actionType;
@synthesize startLocation = _startLocation;
@synthesize availableAbilities = _availableAbilities;
@synthesize battleReport = _battleReport;
@synthesize gamemanager = _gamemanager;

- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card targetCard:(Card *)targetCard {
    
    self = [super initWithGameManager:gamemanager path:path andCardInAction:card enemyCard:targetCard];
    
    if (self) {
        _gamemanager = gamemanager;
        _actionType = kActionTypeAbility;
        _startLocation = card.cardLocation;
        
        _availableAbilities = [NSArray arrayWithArray:self.cardInAction.abilities];
    }
    
    return self;
}

- (BOOL)isAttack {
    
    return NO;
}

- (NSUInteger)cost {
    
    return 1;
}

- (ActionTypes)actionType {
    
    return kActionTypeAbility;
}

- (void)performActionWithCompletion:(void (^)())completion {
    
    _battleReport = [BattleReport battleReportWithAction:self];

    [self.gamemanager willUseAction:self];
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];
    
    if (_availableAbilities.count == 1) {
        _abilityUsed = [AbilityFactory addAbilityOfType:(AbilityTypes)[_availableAbilities[0] integerValue] onCard:self.enemyCard];
    }
        
    [self.gamemanager actionUsed:self];
    [self.cardInAction didPerformedAction:self];
    
    [self.gamemanager.currentGame addBattleReport:_battleReport forAction:self];
    
    [self.delegate afterPerformAction:self];
    
    if (completion != nil) {
        completion();
    }
}
@end
