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
#import "HeavyCavalry.h"

#import "Chariot.h"
#import "Canon.h"
#import "Berserker.h"
#import "Scout.h"
#import "Lancer.h"
#import "RoyalGuard.h"
#import "Samurai.h"
#import "Viking.h"
#import "LongSwordsMan.h"
#import "Crusader.h"
#import "FlagBearer.h"
#import "WarElephant.h"
#import "WeaponSmith.h"
#import "Diplomat.h"

@interface CardPool()

-(NSArray*)shuffle:(NSArray *)array;

- (Card*)createCardOfName:(UnitName)unitName;

@end

@implementation CardPool

- (id)init {
    
    self = [super init];
    
    if (self) {
    
    }
    
    return self;
}

- (Card *)createCardOfName:(UnitName)unitName {
    
    switch (unitName) {
        case kArcher:
            return [Archer card];
        case kBallista:
            return [Ballista card];
        case kCatapult:
            return [Catapult card];
        case kHeavyCalavry:
            return [HeavyCavalry card];
        case kLightCavalry:
            return [LightCavalry card];
        case kPikeman:
            return [Pikeman card];
        case kChariot:
            return [Chariot card];
        case kCannon:
            return [Canon card];
        case kBerserker:
            return [Berserker card];
        case kScout:
            return [Scout card];
        case kLancer:
            return [Lancer card];
        case kRoyalGuard:
            return [RoyalGuard card];
        case kSamurai:
            return [Samurai card];
        case kViking:
            return [Viking card];
        case kLongSwordsMan:
            return [LongSwordsMan card];
        case kCrusader:
            return [Crusader card];
        case kFlagBearer:
            return [FlagBearer card];
        case kWarElephant:
            return [WarElephant card];
        case kWeaponSmith:
            return [WeaponSmith card];
        case kDiplomat:
            return [Diplomat card];
        default:
            CCLOG(@"Unknown cardname: %d", unitName);
    }
    
    return nil;
}

-(NSArray*)shuffle:(NSArray *)array {
    
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

- (Card *)drawCardOfCardType:(CardType)cardType {
    
    Card *drawnCard;
    
    if (cardType == kCardTypeBasicUnit) {
        UnitName unitName = (arc4random() % 6);
        drawnCard = [self createCardOfName:unitName];
    }
    else if (cardType == kCardTypeSpecialUnit) {
        UnitName unitName = kDiplomat;//(arc4random() % 13) + 6;
        drawnCard = [self createCardOfName:unitName];
    }
    
    return drawnCard;
}

@end
