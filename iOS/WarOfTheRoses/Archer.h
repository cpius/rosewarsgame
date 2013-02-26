//
//  Archer.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "Card.h"
#import "RawBonus.h"

@interface Archer : Card {
    
    RawBonus *_bonusAgainstInfantry;
}

+ (id)card;

@end
