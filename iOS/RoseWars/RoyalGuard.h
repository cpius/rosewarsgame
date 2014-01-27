//
//  RoyalGuard.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/10/13.
//
//

#import "Card.h"
#import "RawBonus.h"

@interface RoyalGuard : Card {
    
    RawBonus *_bonusAgainstMelee;
}

+ (id)card;

@end
