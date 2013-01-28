//
//  RawBonus.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import "BaseRangedAttribute.h"

@interface RawBonus : NSObject

@property (nonatomic, readonly) NSUInteger bonusValue;

- (id)initWithValue:(NSUInteger)bonusValue;

@end
