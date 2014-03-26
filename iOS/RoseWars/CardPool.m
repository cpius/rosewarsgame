//
//  CardPool.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/25/12.
//
//

#import "CardPool.h"
#import "Archer.h"
#import "Ballista.h"
#import "Catapult.h"
#import "Pikeman.h"
#import "LightCavalry.h"
#import "Knight.h"

#import "Hobelar.h"
#import "Canon.h"
#import "Berserker.h"
#import "Scout.h"
#import "Lancer.h"
#import "RoyalGuard.h"
#import "Samurai.h"
#import "Viking.h"
#import "Longswordsman.h"
#import "Crusader.h"
#import "FlagBearer.h"
#import "WarElephant.h"
#import "Weaponsmith.h"
#import "Diplomat.h"
#import "Juggernaut.h"

@interface CardPool()

-(NSArray*)shuffle:(NSArray *)array;


@end

@implementation CardPool

- (id)init {
    
    self = [super init];
    
    if (self) {
    
    }
    
    return self;
}

+ (Card *)createCardOfName:(UnitName)unitName withCardColor:(CardColors)cardColor {

    Card *createdCard;
    
    switch (unitName) {
        case kArcher:
            createdCard = [Archer card];
            break;
        case kBallista:
            createdCard = [Ballista card];
            break;
        case kCatapult:
            createdCard = [Catapult card];
            break;
        case kKnight:
            createdCard = [Knight card];
            break;
        case kLightCavalry:
            createdCard = [LightCavalry card];
            break;
        case kPikeman:
            createdCard = [Pikeman card];
            break;
        case kHobelar:
            createdCard = [Hobelar card];
            break;
        case kCannon:
            createdCard = [Canon card];
            break;
        case kBerserker:
            createdCard = [Berserker card];
            break;
        case kScout:
            createdCard = [Scout card];
            break;
        case kLancer:
            createdCard = [Lancer card];
            break;
        case kRoyalGuard:
            createdCard = [RoyalGuard card];
            break;
        case kSamurai:
            createdCard = [Samurai card];
            break;
        case kViking:
            createdCard = [Viking card];
            break;
        case kLongswordsman:
            createdCard = [Longswordsman card];
            break;
        case kCrusader:
            createdCard = [Crusader card];
            break;
        case kFlagBearer:
            createdCard = [FlagBearer card];
            break;
        case kWarElephant:
            createdCard = [WarElephant card];
            break;
        case kWeaponsmith:
            createdCard = [Weaponsmith card];
            break;
        case kDiplomat:
            createdCard = [Diplomat card];
            break;
        case kJuggernaut:
            createdCard = [Juggernaut card];
            break;
        default:
            NSLog(@"Unknown cardname: %d", unitName);
    }
    
    createdCard.cardColor = cardColor;
    
    return createdCard;
}

- (NSArray*)shuffle:(NSArray *)array {
    
    NSMutableArray *tempArray = [NSMutableArray arrayWithArray:array];
    
    NSUInteger count = [tempArray count];
    for (NSUInteger i = 0; i < count; ++i) {
        // Select a random element between i and end of array to swap with.
        int nElements = count - i;
        int n = (arc4random() % nElements) + i;
        [tempArray exchangeObjectAtIndex:i withObjectAtIndex:n];
    }
    
    return [NSArray arrayWithArray:tempArray];
}

- (Card *)drawCardOfCardType:(CardType)cardType cardColor:(CardColors)cardColor {
    
    Card *drawnCard;
    
    if (cardType == kCardTypeBasicUnit) {
        UnitName unitName = (arc4random() % 6);
        drawnCard = [CardPool createCardOfName:unitName withCardColor:cardColor];
    }
    else if (cardType == kCardTypeSpecialUnit) {
        UnitName unitName = (arc4random() % 15) + 6;
        drawnCard = [CardPool createCardOfName:unitName withCardColor:cardColor];
    }
    
    return drawnCard;
}

@end
