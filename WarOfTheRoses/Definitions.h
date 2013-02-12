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

typedef struct _GridLocation {
    NSInteger row;
    NSInteger column;
} GridLocation;

NS_INLINE GridLocation MakeGridLocation(NSInteger row, NSInteger column) {
    GridLocation cl;
    cl.row = row;
    cl.column = column;
    return cl;
}

#define GridLocationEmpty MakeGridLocation(-1, -1);

/*NS_INLINE GridLocation GridLocationEmpty() {
    return MakeGridLocation(-1, -1);
}
*/
NS_INLINE BOOL GridLocationEqualToLocation(GridLocation location1, GridLocation location2) {
    
    return location1.row == location2.row && location1.column == location2.column;
}

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
