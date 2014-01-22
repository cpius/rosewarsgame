//
//  Definitions.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#ifndef WarOfTheRoses_Definitions_h
#define WarOfTheRoses_Definitions_h

#define APP_FONT @"Vollkorn-Regular"
#define APP_FONT_BOLD @"Vollkorn-Bold"

#define BOARDSIZE_ROWS 8
#define BOARDSIZE_COLUMNS 5

#define LOWER_BACKLINE 8
#define LOWER_FRONTLINE 5
#define UPPER_BACKLINE 1
#define UPPER_FRONTLINE 4

#define kEnemyActionDelayTime 1.0

#define ccp CGPointMake

#define NUMBER_OF_BASICUNITS 6
#define NUMBER_OF_SPECIALUNITS 3

#define GAMEEVENT_LEVEL_INCREASED   @"GameEventLevelIncreased"

#define RGB(r, g, b) [SKColor colorWithRed:r/255.0 green:g/255.0 blue:b/255.0 alpha:1]
#define RGBA(r, g, b, a) [SKColor colorWithRed:r/255.0 green:g/255.0 blue:b/255.0 alpha:a]

#define kGameBoardnodeZOrder 11
#define kCardSpriteZOrder 12
#define kCardSpriteDetailZOrder 13
#define kOverlayZOrder 20
#define kAttackingCardSpriteZOrder 21

typedef enum {
    kLevelIncreaseAbilityAttack = 0,
    kLevelIncreaseAbilityDefense,
    kLevelIncreaseAbilityIndeterminate
} LevelIncreaseAbilities;

typedef enum {
    kCardSnapshotStateBeforeAction = 0,
    kCardSnapshotStateAfterAction
} CardSnapshotStates;

typedef enum {
    kActionTypeMove = 0,
    kActionTypeMelee,
    kActionTypeRanged,
    kActionTypeAbility,
    kActionTypePush
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
    kGameBoardLower = 1
} GameBoardSides;

#define IS_IPHONE5 (([[UIScreen mainScreen] bounds].size.height-568)?NO:YES)

NS_INLINE CGPoint CGPointAdd(CGPoint p1, CGPoint p2) {
    return CGPointMake(p1.x + p2.x, p1.y + p2.y);
}

NS_INLINE CGPoint CGPointSubtract(CGPoint p1, CGPoint p2) {
    return CGPointMake(p1.x - p2.x, p1.y - p2.y);
}

NS_INLINE float DegreesToRadians(float degrees) {
    return degrees / 180.0f * M_PI;
}

NS_INLINE GameBoardSides OppositeGameBoardSideOf(GameBoardSides side) {
    
    if (side == kGameBoardUpper) {
        return kGameBoardLower;
    }
    else {
        return kGameBoardUpper;
    }
}

NS_INLINE NSUInteger GetFrontlineForGameBoardSide(GameBoardSides side) {

    if (side == kGameBoardUpper) {
        return UPPER_FRONTLINE;
    }
    else {
        return LOWER_FRONTLINE;
    }
}

NS_INLINE NSUInteger GetBacklineForGameBoardSide(GameBoardSides side) {
    
    if (side == kGameBoardUpper) {
        return UPPER_BACKLINE;
    }
    else {
        return LOWER_BACKLINE;
    }
}

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
    kAbilityActionCoseLess,
    kAbilityCoolDown
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
    kWeaponSmith,
    kDiplomat,
    kJuggernaut,
    kSaboteur,
    kAssassin,
    kUnitNameCount
} UnitName;

NS_INLINE NSString* UnitNameAsString(UnitName unitName) {
    
    switch (unitName) {
        case kArcher:
            return @"Archer";
        case kBallista:
            return @"Ballista";
        case kCatapult:
            return @"Catapult";
        case kPikeman:
            return @"Pikeman";
        case kLightCavalry:
            return @"LightCavalry";
        case kHeavyCalavry:
            return @"HeavyCavalry";
        case kChariot:
            return @"Chariot";
        case kCannon:
            return @"Cannon";
        case kBerserker:
            return @"Berserker";
        case kScout:
            return @"Scout";
        case kLancer:
            return @"Lancer";
        case kRoyalGuard:
            return @"RoyalGuard";
        case kViking:
            return @"Viking";
        case kSamurai:
            return @"Samurai";
        case kLongSwordsMan:
            return @"LongswordsMan";
        case kCrusader:
            return @"Crusader";
        case kFlagBearer:
            return @"Flagbearer";
        case kWarElephant:
            return @"WarElephant";
        case kWeaponSmith:
            return @"WeaponSmith";
        case kDiplomat:
            return @"Diplomat";
        case kSaboteur:
            return @"Saboteur";
        case kAssassin:
            return @"Assassin";
        case kJuggernaut:
            return @"Juggernaut";
        default:
            break;
    }
    
    return nil;
}

typedef enum {
    kCardColorGreen = 0,
    kCardColorRed = 1
} CardColors;

NS_INLINE NSString* CardColorAsString(CardColors cardColor) {
    
    switch (cardColor) {
        case kCardColorGreen:
            return @"Green";
        case kCardColorRed:
            return @"Red";
        default:
            break;
    }
    
    return nil;
}

typedef enum {
    kPlayerGreen = 0,
    kPlayerRed = 1
} PlayerColors;

NS_INLINE CardColors OppositeColorOfCardColor(CardColors cardColor) {
    
    if (cardColor == kCardColorGreen) {
        return kCardColorRed;
    }
    else {
        return kCardColorGreen;
    }
}

NS_INLINE PlayerColors OppositeColorOf(PlayerColors playerColor) {
    
    if (playerColor == kPlayerGreen) {
        return kPlayerRed;
    }
    else {
        return kPlayerGreen;
    }
}

typedef enum {
    kGameTypeSinglePlayer = 0,
    kGameTypeMultiPlayer
} GameTypes;

#endif
