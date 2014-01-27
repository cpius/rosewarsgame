//
//  Pikeman.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "Card.h"
#import "RawBonus.h"

@interface Pikeman : Card {
    
    RawBonus *_bonusAgainstCavalry;
}

+ (id)card;

@end
