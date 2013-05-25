//
//  BaseAttribute.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import <Foundation/Foundation.h>

typedef struct _AttributeRange {
    NSInteger lowerValue;
    NSInteger upperValue;
} AttributeRange;

NS_INLINE AttributeRange MakeAttributeRange(NSInteger lower, NSInteger upper) {
    AttributeRange r;
    r.lowerValue = lower;
    r.upperValue = upper;
    return r;
}

NS_INLINE NSString* AttributeRangeToNSString(AttributeRange range) {
    
    return [NSString stringWithFormat:@"%d - %d", range.lowerValue, range.upperValue];
}

@interface BaseRangedAttribute : NSObject {
    
}

- (id)initWithRange:(AttributeRange)range;

@property (nonatomic, readonly) AttributeRange baseRange;
@property (nonatomic, copy) NSString *attributeAbbreviation;

@end
