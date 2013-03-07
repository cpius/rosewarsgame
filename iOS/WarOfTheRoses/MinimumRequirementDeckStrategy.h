//
//  MinimumRequirementDeckStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/5/13.
//
//

#import "BaseDeckStrategy.h"
#import "DeckStrategy.h"

@interface MinimumRequirementDeckStrategy : BaseDeckStrategy <DeckStrategy> {
    
    NSArray *_nonFrontLineUnits;
    NSArray *_nonBackLineUnits;
}

@end
