//
//  MinimumRequirementDeckStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/5/13.
//
//

#import "MinimumRequirementDeckStrategy.h"
#import "CardPool.h"
#import "Deck.h"

@interface MinimumRequirementDeckStrategy()

- (Card*)unitAtGridLocation:(GridLocation*)gridLocation;

- (BOOL)deckContainsRequiredUnits;
- (BOOL)deckPlacedAccordingToRequirements;

@end

@implementation MinimumRequirementDeckStrategy

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        _nonFrontLineUnits = @[@(kLightCavalry), @(kBallista), @(kCatapult), @(kArcher), @(kScout), @(kSaboteur), @(kDiplomat), @(kBerserker), @(kCannon), @(kWeaponSmith), @(kRoyalGuard)];
        
        _nonBackLineUnits = @[@(kPikeman), @(kBerserker), @(kLongSwordsMan), @(kRoyalGuard), @(kSamurai), @(kViking), @(kWarElephant)];
    }
    
    return self;
}

+ (id)strategy {
    
    return [[MinimumRequirementDeckStrategy alloc] init];
}

- (Card *)unitAtGridLocation:(GridLocation *)gridLocation {
    
    for (Card *card in _cards) {
        if ([card.cardLocation isEqual:gridLocation]) {
            return card;
        }
    }
    
    return nil;
}

/*def test_coloumn_blocks(player):
""" Tests whether there on each coloumn are at least two 'blocks'. A block is either a unit, or a Pikeman zoc tile other than the back line. """

cols = [pos[0] + x for x in [-1, +1] for pos, unit in player.units.items() if unit.name == "Pikeman"] + [pos[0] for pos in player.units]

return not any(cols.count(col) < 2 for col in [1,2,3,4,5] )
*/

- (Deck*)generateNewDeckWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType cardColor:(CardColors)cardColor {
    
    NSUInteger retries = 0;
    CardPool *cardPool = [[CardPool alloc] init];

    do {
        _cards = [[NSMutableArray alloc] init];
        
        NSInteger numberOfBasicTypes = 0;
        NSInteger numberOfSpecialTypes = 0;
        
        while (numberOfBasicTypes < basicType) {
            
            Card *drawnCard = [cardPool drawCardOfCardType:kCardTypeBasicUnit];
            
            drawnCard.cardColor = cardColor;
            
            if ([self cardIsAllowedInDeck:drawnCard]) {
                [_cards addObject:drawnCard];
                numberOfBasicTypes++;
            }
        }
        
        while (numberOfSpecialTypes < specialType) {
            
            Card *drawnCard = [cardPool drawCardOfCardType:kCardTypeSpecialUnit];
            
            drawnCard.cardColor = cardColor;
            
            if ([self cardIsAllowedInDeck:drawnCard]) {
                [_cards addObject:drawnCard];
                numberOfSpecialTypes++;
            }
        }
        
        retries++;
        
    } while (![self deckContainsRequiredUnits]);
    
    CCLOG(@"%d retries before deck contained required units", retries);
    
    return [[Deck alloc] initWithCards:_cards];
}

- (BOOL)deckContainsRequiredUnits {

    return [self deckContainsAtLeastOnePikeman] &&
            [self deckContainsMaxTwoSiegeWeapons];
}

- (BOOL)deckPlacedAccordingToRequirements {
    
    return [self deckContainsNoNonFrontLineUnitInFrontLine] &&
    [self deckContainsNoBackLineUnitsInBackLine] &&
    [self deckContainsMoreThanOneUnitOnBackLine] &&
    [self deckContainsMaxOnePikemanPerColumn];
}

- (BOOL)deckContainsMaxTwoSiegeWeapons {
    
    NSUInteger numberOfSiegeWeapons = 0;
    
    for (Card *card in _cards) {
        if (card.unitType == kSiege) {
            numberOfSiegeWeapons++;
        }
    }
    
    return numberOfSiegeWeapons <= 2;
}

- (BOOL)deckContainsAtLeastOnePikeman {
    
    for (Card *card in _cards) {
        if (card.unitName == kPikeman) {
            return YES;
        }
    }
    
    return NO;
}

- (BOOL)deckContainsNoNonFrontLineUnitInFrontLine {
    
    for (Card *card in _cards) {
        if (card.cardLocation.row == GetFrontlineForGameBoardSide(_placeCardsInSide) && [_nonFrontLineUnits containsObject:@(card.unitName)]) {
            return NO;
        }
    }
    
    return YES;
}

- (BOOL)deckContainsNoBackLineUnitsInBackLine {
    
    NSUInteger backline = GetBacklineForGameBoardSide(_placeCardsInSide);
    
    for (Card *card in _cards) {
        if (card.cardLocation.row == backline  && [_nonBackLineUnits containsObject:@(card.unitName)]) {
            return NO;
        }
    }
    
    return YES;
}

- (BOOL)deckContainsMoreThanOneUnitOnBackLine {
    
    NSUInteger unitsOnBackLine = 0;

    for (Card *card in _cards) {
        if (card.cardLocation.row == GetBacklineForGameBoardSide(_placeCardsInSide)) {
            unitsOnBackLine++;
        }
    }
    
    return unitsOnBackLine > 1;
}

- (BOOL)deckContainsMaxOnePikemanPerColumn {
    
    NSUInteger pikemen = 0;
    
    NSUInteger rowStart = _placeCardsInSide == kGameBoardLower ? GetFrontlineForGameBoardSide(_placeCardsInSide) : GetBacklineForGameBoardSide(_placeCardsInSide);
    NSUInteger rowEnd = _placeCardsInSide == kGameBoardLower ?  GetBacklineForGameBoardSide(_placeCardsInSide) : GetFrontlineForGameBoardSide(_placeCardsInSide);
    
    for (int column = 1; column <= 5; column++) {
        for (int row = rowStart; row <= rowEnd; row++) {
            
            Card *card = [self unitAtGridLocation:[GridLocation gridLocationWithRow:row column:column]];
            if (card != nil && card.unitName == kPikeman) {
                pikemen++;
                
                if (pikemen == 2) {
                    return NO;
                }
            }
        }
                          
        pikemen = 0;
    }
    
    return YES;
}


- (void)placeCardsInDeck:(Deck *)deck inGameBoardSide:(GameBoardSides)gameBoardSide {
    
    NSUInteger retries = 0;
    
    _placeCardsInSide = gameBoardSide;
    _cards = deck.cards.mutableCopy;
    
    do {
        for (Card *card in _cards) {
            
            BOOL cardInValidPosition = NO;
            
            while (!cardInValidPosition) {
                
                GridLocation *location;
                
                if (GetFrontlineForGameBoardSide(_placeCardsInSide) == UPPER_FRONTLINE) {
                    location = [GridLocation gridLocationWithRow:(arc4random() % 4) + 1 column:(arc4random() % 5) + 1];
                }
                else {
                    location = [GridLocation gridLocationWithRow:(arc4random() % 4) + 5 column:(arc4random() % 5) + 1];
                }
                
                if (![self deck:deck containsCardInLocation:location]) {
                    
                    card.cardLocation = location;
                    cardInValidPosition = YES;
                }
            }
        }
        
        retries++;
        
    } while (![self deckPlacedAccordingToRequirements]);
    
    CCLOG(@"%d retries before deck was placed according to requirements", retries);
}
@end
