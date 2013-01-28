//
//  Attribute.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import "RangeAttribute.h"

@implementation RangeAttribute

@synthesize finalRange = _finalRange;
@synthesize delegate = _delegate;

- (id)initWithStartingRange:(AttributeRange)startingRange {
    
    self = [super initWithRange:startingRange];
    
    if (self) {
        
        _rawBonuses = [[NSMutableArray alloc] init];
        _timedBonuses = [[NSMutableArray alloc] init];
        
        _finalRange = self.baseRange;
    }
    
    return self;
}

- (void)addTimedBonus:(TimedBonus *)timedBonus {
    
    [_timedBonuses addObject:timedBonus];
    
    if ([_delegate respondsToSelector:@selector(rangeAttribute:addedTimedBonus:)]) {
        [_delegate rangeAttribute:self addedTimedBonus:timedBonus];
    }
}

- (void)addRawBonus:(RawBonus *)rawBonus {
    
    [_rawBonuses addObject:rawBonus];
    
    if ([_delegate respondsToSelector:@selector(rangeAttribute:addedRawBonus:)]) {
        [_delegate rangeAttribute:self addedRawBonus:rawBonus];
    }
}

- (void)removeTimedBonus:(TimedBonus *)timedBonus {
    
    if ([_timedBonuses containsObject:timedBonus]) {
        [_timedBonuses removeObject:timedBonus];
        
        if ([_delegate respondsToSelector:@selector(rangeAttribute:removedTimedBonus:)]) {
            [_delegate rangeAttribute:self removedTimedBonus:timedBonus];
        }
    }
}

- (void)removeRawBonus:(RawBonus *)rawBonus {
    
    if ([_rawBonuses containsObject:rawBonus]) {
        [_rawBonuses removeObject:rawBonus];
        
        if ([_delegate respondsToSelector:@selector(rangeAttribute:removedRawBonus:)]) {
            [_delegate rangeAttribute:self removedRawBonus:rawBonus];
        }
    }
}

- (AttributeRange)calculateValue {
    
    _finalRange = self.baseRange;
    
    // Add values from raw bonuses
    NSUInteger rawBonusValue = 0;
    
    for (RawBonus *rawbonus in _rawBonuses) {
        
        rawBonusValue += rawbonus.bonusValue;
    }
    
    _finalRange = MakeAttributeRange(_finalRange.lowerValue - rawBonusValue, _finalRange.upperValue);

    // Add values from final bonuses
    NSUInteger finalBonusValue = 0;
    
    for (TimedBonus *finalbonus in _timedBonuses) {
        
        finalBonusValue += finalbonus.bonusValue;
    }
    
    _finalRange = MakeAttributeRange(_finalRange.lowerValue - rawBonusValue, _finalRange.upperValue);
    
    return _finalRange;
}

- (AttributeRange)finalValue {

    return [self calculateValue];
}

@end
