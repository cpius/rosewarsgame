//
//  CardPool.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/25/12.
//
//

#import "CCNode.h"
#import "Card.h"

@interface CardPool : CCNode {
    
    NSMutableArray *_basicTypesCardPool;
    NSMutableArray *_specialTypesCardPool;
}

- (Card *)drawCardOfCardType:(CardType)cardType;

@end
