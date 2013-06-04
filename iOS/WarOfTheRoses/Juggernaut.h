//
//  Juggernaut.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 5/26/13.
//
//

#import "Card.h"
#import "RawBonus.h"

@interface Juggernaut : Card {
    
    RawBonus *_bonusAgainstRanged;
}

+ (id)card;

@end
