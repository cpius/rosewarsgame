//
//  Deck.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"

@interface Deck : NSObject {
    
}

@property (nonatomic, strong) NSMutableArray *cards;

- (id)initWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType cardColor:(CardColors)cardColor;

- (void)generateNewDeckWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType cardColor:(CardColors)cardColor;

- (void)resetMoveCounters;

@end
