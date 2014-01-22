//
//  CardPool.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/25/12.
//
//

#import <SpriteKit/SpriteKit.h>
#import "Card.h"

@interface CardPool : SKNode {
    
    NSMutableArray *_basicTypesCardPool;
    NSMutableArray *_specialTypesCardPool;
}

+ (Card *)createCardOfName:(UnitName)unitName withCardColor:(CardColors)cardColor;
- (Card *)drawCardOfCardType:(CardType)cardType cardColor:(CardColors)cardColor;

@end
