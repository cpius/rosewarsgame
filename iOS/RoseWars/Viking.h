//
//  Viking.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "Card.h"
#import "RawBonus.h"

@interface Viking : Card {
    
    RawBonus *_bonusAgainstSiege;
}

+ (id)card;

@end
