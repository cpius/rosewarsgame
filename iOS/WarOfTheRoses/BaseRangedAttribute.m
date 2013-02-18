//
//  BaseAttribute.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import "BaseRangedAttribute.h"

@implementation BaseRangedAttribute

@synthesize baseRange = _baseRange;
@synthesize attributeAbbreviation = _attributeAbbreviation;

- (id)initWithRange:(AttributeRange)range {
    
    self = [super init];
    
    if (self) {
        
        _baseRange = range;
    }
    
    return self;
}

@end
