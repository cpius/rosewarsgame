//
//  Lancer.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/8/13.
//
//

#import "Card.h"
#import "RawBonus.h"

@interface Lancer : Card {

    RawBonus *_bonusAgainstLancer;
}

+ (id)card;

@end
