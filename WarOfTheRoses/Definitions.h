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
    kCombatOutcomeDefendSuccessful = 1
} CombatOutcome;

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
    kArcher,
    kBallista,
    kCatapult,
    kPikeman,
    kLightCavalry,
    kHeavyCalavry,
    kLongSwordsMan,
    kRoyalGuard,
    kBerserker,
    kSamurai,
    kViking,
    kChariot,
    kScout,
    kCrusader,
    kFlagBearer,
    kLancer,
    kWarElephant,
    kCannon,
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
