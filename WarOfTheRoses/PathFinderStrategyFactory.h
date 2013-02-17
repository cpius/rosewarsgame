//
//  PathFinderStrategyFactory.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import <Foundation/Foundation.h>
#import "BasePathFinderStrategy.h"
#import "Card.h"

@interface PathFinderStrategyFactory : NSObject

+ (BasePathFinderStrategy *)getStrategyFromCard:(Card *)fromCard toCard:(Card*)toCard myColor:(PlayerColors)myColor;

@end
