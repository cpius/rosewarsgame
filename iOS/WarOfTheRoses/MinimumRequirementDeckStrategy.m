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
    
    _cards = [[NSMutableArray alloc] init];
    
    CardPool *cardPool = [[CardPool alloc] init];
    
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
    
    return [[Deck alloc] initWithCards:_cards];
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
        if (card.cardLocation.row == 4 && [_nonFrontLineUnits containsObject:@(card.unitName)]) {
            return NO;
        }
    }
    
    return YES;
}

- (BOOL)deckContainsNoBackLineUnitsInBackLine {
    
    for (Card *card in _cards) {
        if (card.cardLocation.row == 1 && [_nonBackLineUnits containsObject:@(card.unitName)]) {
            return NO;
        }
    }
    
    return YES;
}

- (BOOL)deckContainsMoreThanOneUnitOnBackLine {
    
    NSUInteger unitsOnBackLine = 0;

    for (Card *card in _cards) {
        if (card.cardLocation.row == 1) {
            unitsOnBackLine++;
        }
    }
    
    return unitsOnBackLine > 1;
}

- (BOOL)deckContainsMaxOnePikemanPerColumn {
    
    NSUInteger pikemen = 0;
    
    for (int column = 1; column <= 5; column++) {
        for (int row = 1; row <= 4; row++) {
            
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

- (BOOL)deckSetupMatchesRequirements {

    if ([self deckContainsAtLeastOnePikeman] &&
        [self deckContainsNoNonFrontLineUnitInFrontLine] &&
        [self deckContainsNoBackLineUnitsInBackLine] &&
        [self deckContainsMoreThanOneUnitOnBackLine] &&
        [self deckContainsMaxOnePikemanPerColumn]) {
        
        return YES;
    }
    
    return NO;
}

- (void)placeCardsInDeck:(Deck *)deck inGameBoardSide:(GameBoardSides)gameBoardSide {
    
    NSUInteger offset = 0;
    
    for (Card *card in deck.cards) {
        
        BOOL cardInValidPosition = NO;
        
        while (!cardInValidPosition) {
            
            GridLocation *location = [GridLocation gridLocationWithRow:(arc4random() % 4) + 1 + offset column:(arc4random() % 5) + 1];
            
            if (![self deck:deck containsCardInLocation:location]) {
                
                card.cardLocation = location;
                cardInValidPosition = YES;
            }
        }
    }
}
@end
