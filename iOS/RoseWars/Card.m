//
//  Card.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "Card.h"
#import "Action.h"
#import "GameManager.h"
#import "StandardBattleStrategy.h"
#import "RandomLevelIncreaseStrategy.h"
#import "PromptLevelIncreaseStrategy.h"

const NSInteger kNumberOfExperiencePointsToIncreaseLevel = 4;

@implementation Card

@synthesize frontImageSmall = _frontImageSmall;
@synthesize frontImageLarge = _frontImageLarge;
@synthesize backImage = _backImage;
@synthesize cardColor = _cardColor;
@synthesize cardLocation = _cardLocation;
@synthesize isShowingDetail;
@synthesize attack = _attack, defence = _defence;
@synthesize movesConsumed;
@synthesize move;
@synthesize experience;
@synthesize range;
@synthesize isRanged, isMelee, isCaster;
@synthesize dead;
@synthesize moveActionCost;
@synthesize attackActionCost;
@synthesize hasReceivedExperiencePointsThisRound;
@synthesize numberOfLevelsIncreased;
@synthesize delegate = _delegate;
@synthesize attackSound = _attackSound, defeatSound = _defenceSound, moveSound = _moveSound;
@synthesize currentlyAffectedByAbilities = _currentlyAffectedByAbilities;
@synthesize hitpoints;
@synthesize battleStrategy = _battleStrategy;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        self.isShowingDetail = NO;
        
        _currentlyAffectedByAbilities = [NSMutableArray array];
    }
    
    return self;
}

- (void)commonInit {
    
    self.attack.attributeAbbreviation = @"A";
    self.attack.valueAffectedByBonuses = kRangedAttributeLowerValue;
    
    self.defence.attributeAbbreviation = @"D";
    self.defence.valueAffectedByBonuses = kRangedAttributeUpperValue;
    self.defence.valueLimit = 4;
    
    self.numberOfLevelsIncreased = 0;
    self.experience = 0;
    
    _cardIdentifier = [self createCardIdentifier];
}

- (void)setCardColor:(CardColors)cardColor {
    
    _cardColor = cardColor;

    if ([self isOwnedByMe]) {
        _levelIncreaseStrategy = [[PromptLevelIncreaseStrategy alloc] init];
    }
    else {
        _levelIncreaseStrategy = [[RandomLevelIncreaseStrategy alloc] init];
    }
}

- (NSString *)unitDescriptionName {
    
    return NSStringFromClass(self.class);
}

- (NSString*)createCardIdentifier {
    
    CFUUIDRef uuid = CFUUIDCreate(NULL);
    NSString *uuidStr = (__bridge_transfer NSString *)CFUUIDCreateString(NULL, uuid);
    CFRelease(uuid);
    
    return uuidStr;
}

- (BaseBattleStrategy*)newBattleStrategy {
    
    return [StandardBattleStrategy strategy];
}

- (id<BattleStrategy>)battleStrategy {
    
    if (_battleStrategy == nil) {
        _battleStrategy = [self newBattleStrategy];
    }
    
    return _battleStrategy;
}

- (void)resetAfterNewRound {
    
    self.movesConsumed = 0;
    self.hasReceivedExperiencePointsThisRound = NO;
    self.hasPerformedActionThisRound = NO;
    self.hasPerformedAttackThisRound = NO;
}

- (NSArray*)abilities {
    
    return nil;
}

- (BOOL)isCaster {
    
    return self.unitAttackType == kUnitAttackTypeCaster;
}

- (BOOL)isMelee {
    
    return self.unitAttackType == kUnitAttackTypeMelee;
}

- (BOOL)isRanged {
    
    return self.unitAttackType == kUnitAttackTypeRanged;
}

- (NSUInteger)meleeRange {
    
    return 1;
}

- (NSString *)description {
    
    NSString *description = [NSString stringWithFormat:@"Unit: %@ - with color: %@ boardlocation: row %d column %d",
                             UnitNameAsString(self.unitName),
                             CardColorAsString(self.cardColor),
                             self.cardLocation.row,
                             self.cardLocation.column];
    
    return description;
}

- (void)addTimedAbility:(TimedAbility*)timedAbility {
    
    timedAbility.delegate = self;
    timedAbility.card = self;
    
    [_currentlyAffectedByAbilities addObject:timedAbility];
}

- (void)timedAbilityDidStop:(TimedAbility *)timedAbility {
    
    if ([_currentlyAffectedByAbilities containsObject:timedAbility]) {
        [_currentlyAffectedByAbilities removeObject:timedAbility];
    }
}

- (void)applyAoeEffectIfApplicableWhilePerformingAction:(Action *)action {
    
}

// Must be overloaded in subclasses
- (BOOL)specialAbilityTriggersVersus:(Card *)opponent {
    
    return NO;
}

- (void)addSpecialAbilityVersusOpponent:(Card *)opponent {
    
}

- (BOOL)zoneOfControlAgainst:(Card *)opponent {
    
    return NO;
}

- (void)combatStartingAgainstDefender:(Card *)defender {
    
}

- (void)combatStartingAgainstAttacker:(Card *)attacker {
    
}

- (void)combatFinishedAgainstAttacker:(Card *)attacker withOutcome:(CombatOutcome)combatOutcome {
    
    if (IsAttackSuccessful(combatOutcome)) {
        self.dead = YES;
    }
}

- (void)combatFinishedAgainstDefender:(Card *)defender withOutcome:(CombatOutcome)combatOutcome {
    
}

- (NSInteger)numberOfExperienceToIncreaseLevel {
    
    return kNumberOfExperiencePointsToIncreaseLevel;
}

- (void)levelIncreased {
    
    NSLog(@"Card: %@ advanced in level", self);
    
    self.numberOfLevelsIncreased++;
    
    LevelIncreaseAbilities abilityIncreased = [_levelIncreaseStrategy cardIncreasedInLevel:self];
    
    if ([_delegate respondsToSelector:@selector(cardIncreasedInLevel:withAbilityIncreased:)]) {
        [_delegate cardIncreasedInLevel:self withAbilityIncreased:abilityIncreased];
    }
}

- (void)willPerformAction:(Action *)action {
    
    NSArray *cards;
    
    if ([action.cardInAction isOwnedByMe]) {
        cards = [GameManager sharedManager].currentGame.myDeck.cards;
    }
    else {
        cards = [GameManager sharedManager].currentGame.enemyDeck.cards;
    }
    
    for (Card *card in cards) {
        [card applyAoeEffectIfApplicableWhilePerformingAction:action];
    }
}

- (void)didPerformedAction:(Action *)action {

    self.hasPerformedActionThisRound = YES;
    
    // An attack consumes all remaining moves of an unit
    if (action.isAttack) {
        self.hasPerformedAttackThisRound = YES;
        [self consumeAllMoves];
    }

    if (!self.hasReceivedExperiencePointsThisRound) {
        self.experience++;
        
        // Unit can only receive experience point once every round
        self.hasReceivedExperiencePointsThisRound = YES;
        
        if ((self.experience % kNumberOfExperiencePointsToIncreaseLevel) == 0) {
            [self levelIncreased];
        }
    }
}

- (void)didResolveCombatDuringAction:(Action *)action {
    
}

- (BOOL)isValidTarget:(Card*)targetCard {
    
    return YES;
}

- (BOOL)allowAction:(Action *)action allLocations:(NSDictionary*)allLocations {
    
    BOOL allowAction = [self allowPath:action.path forActionType:action.actionType allLocations:allLocations];

    // Check if card is affected by any abilities that doesn't allow this action
    for (TimedAbility *ability in _currentlyAffectedByAbilities) {
        
        if (![ability allowPerformAction:action]) {
            allowAction = NO;
        }
    }
    
    return allowAction;
}

- (BOOL)allowPath:(NSArray *)path forActionType:(ActionTypes)actionType allLocations:(NSDictionary *)allLocations {
    
    BOOL allowPath = NO;
    
    if (actionType == kActionTypeMove) {
        if (path != nil && path.count > 0 && path.count <= self.movesRemaining) {
            allowPath = YES;
        }
    }
    else if (actionType == kActionTypeMelee) {
        if ((path != nil && path.count > 0) && path.count <= self.movesRemaining) {
            allowPath = YES;
        }
    }
    else if (actionType == kActionTypeRanged) {
        if ((path != nil && path.count > 0) && path.count <= self.range) {
            allowPath = YES;
        }
    }
    else if (actionType == kActionTypeAbility) {
        if ((path != nil && path.count > 0) && path.count <= self.range) {
            allowPath = YES;
        }
    }
    
    return allowPath;
}

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount {
    
    if (self.hasPerformedActionThisRound) {
        return NO;
    }
    
    switch (actionType) {
            
        case kActionTypeMove:
            return self.moveActionCost <= remainingActionCount && self.movesRemaining > 0;
                        
        case kActionTypeMelee:
            if (self.movesRemaining == 0 || self.hasPerformedAttackThisRound) {
                return NO;
            }
            else {
                // Unit cannot move and attack the same round
                return (self.attackActionCost <= remainingActionCount) && !self.isRanged;
            }
            
        case kActionTypeRanged:
            
            if (self.movesRemaining == 0 || self.hasPerformedAttackThisRound) {
                return NO;
            }
            else {
                // Unit cannot move and attack the same round
                return (self.attackActionCost <= remainingActionCount) && self.isRanged;
            }
            
        case kActionTypeAbility:
            
            if (self.movesRemaining == 0 || self.hasPerformedActionThisRound) {
                return NO;
            }
            else {
                return (self.attackActionCost <= remainingActionCount) && self.abilities.count > 0;
            }
            
        case kActionTypePush:
            break;
    }
    
    return NO;
}

- (void)consumeAllMoves {
    
    movesConsumed = move;
}

- (void)consumeMove {
    
    [self consumeMoves:1];
}

- (void)consumeMoves:(NSUInteger)moves {
    
    movesConsumed += moves;
}

- (NSInteger)movesRemaining {
    
    return move - movesConsumed;
}

- (BOOL)isOfType:(UnitName)type {
    
    return self.unitName == type;
}

- (BOOL)isOwnedByMe {
    
    return (self.cardColor == kCardColorGreen && [GameManager sharedManager].currentGame.myColor == kPlayerGreen) ||
        (self.cardColor == kCardColorRed && [GameManager sharedManager].currentGame.myColor == kPlayerRed);
}

- (BOOL)isOwnedByEnemy {
    
    return ![self isOwnedByMe];
}

- (BOOL)isOwnedByPlayerWithColor:(PlayerColors)playerColor {
    
    return (self.cardColor == kCardColorGreen && playerColor == kPlayerGreen) ||
    (self.cardColor == kCardColorRed && playerColor == kPlayerRed);
}

- (BOOL)isAffectedByAbility:(AbilityTypes)abilityType {
    
    for (TimedAbility *ability in _currentlyAffectedByAbilities) {
        if (ability.abilityType == abilityType) {
            return YES;
        }
    }
    return NO;
}

- (NSDictionary *)asDictionary {
    
    return [NSDictionary dictionary];
}

- (void)fromDictionary:(NSDictionary*)dictionary {
    
}

@end
