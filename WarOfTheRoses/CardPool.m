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
        UnitName unitName = (arc4random() % 5);
        drawnCard = [self createCardOfName:unitName];
    }
    else if (cardType == kCardTypeSpecialUnit) {
        UnitName unitName = (arc4random() % (kUnitNameCount - 1) + 5);
        drawnCard = [self createCardOfName:unitName];
    }
    
    return drawnCard;
}

@end
