//
//  CardPool.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/25/12.
//
//

#import <SpriteKit/SpriteKit.h>
#import "HKCardProtocol.h"

@interface CardPool : SKNode {
    
    NSMutableArray *_basicTypesCardPool;
    NSMutableArray *_specialTypesCardPool;
}

- (id)initWithGameManager:(GameManager*)gamemanager;

+ (id)createCardOfName:(UnitName)unitName withCardColor:(CardColors)cardColor gamemanager:(GameManager*)gamemanager;
- (id<HKCardProtocol>)drawCardOfCardType:(CardType)cardType cardColor:(CardColors)cardColor;

@end
