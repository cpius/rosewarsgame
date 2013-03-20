//
//  Definitions.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#ifndef WarOfTheRoses_Definitions_h
#define WarOfTheRoses_Definitions_h

#define APP_FONT @"AppleGothic"

#define BOARDSIZE_ROWS 8
#define BOARDSIZE_COLUMNS 5

#define kEnemyActionDelayTime 1.0

typedef enum {
    kActionTypeMove = 0,
    kActionTypeMelee,
    kActionTypeRanged,
    kActionTypeAbility
} ActionTypes;

typedef enum {
    kMeleeAttackTypeNormal,
    kMeleeAttackTypeConquer
} MeleeAttackTypes;

typedef enum {
    kGameResultInProgress,
    kGameResultVictory,
    kGameResultDefeat
} GameResults;

typedef enum {
    kGameBoardUpper = 0,
    kGameBoardLower
} GameBoardSides;

typedef enum {
    kGameStateInitialState = 0,
    kGameStateFinishedPlacingCards = 1,
    kGameStateGameStarted = 2
} GameStates;

typedef enum {
    kCombatOutcomeAttackSuccessful = 0,
    kCombatOutcomeDefendSuccessful = 1,
    kCombatOutcomeDefendSuccessfulMissed = 2,
    kCombatOutcomePush = 3,
    kCombatOutcomeAttackSuccessfulAndPush = 4
    
} CombatOutcome;

NS_INLINE BOOL IsAttackSuccessful(CombatOutcome outcome) {
    
    return outcome == kCombatOutcomeAttackSuccessful || outcome == kCombatOutcomeAttackSuccessfulAndPush;
}

NS_INLINE BOOL IsDefenseSuccessful(CombatOutcome outcome) {
    
    return outcome == kCombatOutcomeDefendSuccessful || outcome == kCombatOutcomeDefendSuccessfulMissed;
}

NS_INLINE BOOL IsPushSuccessful(CombatOutcome outcome) {
    
    return outcome == kCombatOutcomePush || outcome == kCombatOutcomeAttackSuccessfulAndPush;
}

typedef enum {
    
    kAbilityImprovedWeapons = 0,
    kAbilityBribe,
    kAbilityHighMorale,
    kAbilityActionCoseLess
} AbilityTypes;

typedef enum {
    kCardTypeBasicUnit,
    kCardTypeSpecialUnit
} CardType;

typedef enum {
    kInfantry,
    kSiege,
    kCavalry,
    kSpecialUnit
} UnitType;

typedef enum {
    kUnitAttackTypeMelee = 0,
    kUnitAttackTypeRanged,
    kUnitAttackTypeCaster
} UnitAttackTypes;

typedef enum {
    kArcher = 0,
    kBallista,
    kCatapult,
    kPikeman,
    kLightCavalry,
    kHeavyCalavry,
    kChariot,
    kCannon,
    kBerserker,
    kScout,
    kLancer,
    kRoyalGuard,
    kViking,
    kSamurai,
    kLongSwordsMan,
    kCrusader,
    kFlagBearer,
    kWarElephant,
    kSaboteur,
    kAssassin,
    kWeaponSmith,
    kDiplomat,
    kUnitNameCount
} UnitName;

typedef enum {
    kCardColorGreen = 0,
    kCardColorRed = 1
} CardColors;

typedef enum {
    kPlayerGreen = 0,
    kPlayerRed = 1
} PlayerColors;

typedef enum {
    kGameTypeSinglePlayer = 0,
    kGameTypeMultiPlayer
} GameTypes;

#endif
