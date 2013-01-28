//
//  Definitions.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#ifndef WarOfTheRoses_Definitions_h
#define WarOfTheRoses_Definitions_h

#define BUTTON_CLICK_SOUND @"buttonclick.wav"
#define BOOM_SOUND @"boom.wav"
#define SWOOSH_SOUND @"swoosh.wav"

typedef struct _GridLocation {
    NSUInteger row;
    NSUInteger column;
} GridLocation;

NS_INLINE GridLocation MakeGridLocation(NSUInteger row, NSUInteger column) {
    GridLocation cl;
    cl.row = row;
    cl.column = column;
    return cl;
}

typedef enum {
    kGameStateInitialState = 0,
    kGameStateFinishedPlacingCards = 1,
    kGameStateGameStarted = 2
} GameStates;


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
