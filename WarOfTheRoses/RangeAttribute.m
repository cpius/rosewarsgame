//
//  Attribute.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import "RangeAttribute.h"

@interface RangeAttribute()

- (AttributeRange)calculateFinalRange:(AttributeRange)finalRange fromBonus:(NSUInteger)bonus;

@end

@implementation RangeAttribute

@synthesize finalRange = _finalRange;
@synthesize delegate = _delegate;
@synthesize valueAffectedByBonuses = _valueAffectedByBonuses;

- (id)initWithStartingRange:(AttributeRange)startingRange {
    
    self = [super initWithRange:startingRange];
    
    if (self) {
        
        _rawBonuses = [[NSMutableArray alloc] init];
        _timedBonuses = [[NSMutableArray alloc] init];
        
        _valueAffectedByBonuses = kRangedAttributeLowerValue;
        
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

- (NSUInteger)getRawBonusValue {
    
    // Add values from raw bonuses
    NSUInteger rawBonusValue = 0;
    
    for (RawBonus *rawbonus in _rawBonuses) {
        
        rawBonusValue += rawbonus.bonusValue;
    }
    
    return rawBonusValue;
}

- (NSUInteger)getTimedBonusValue {
    
    // Add values from final bonuses
    NSUInteger timedBonusValue = 0;
    
    for (TimedBonus *timedbonus in _timedBonuses) {
        
        timedBonusValue += timedbonus.bonusValue;
    }
    
    return timedBonusValue;
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

- (AttributeRange)calculateFinalRange:(AttributeRange)finalRange fromBonus:(NSUInteger)bonus {
    
    AttributeRange calculatedFinalRange;
    
    if (_valueAffectedByBonuses == kRangedAttributeLowerValue) {
        calculatedFinalRange = MakeAttributeRange(finalRange.lowerValue - bonus, finalRange.upperValue);
    }
    else if (_valueAffectedByBonuses == kRangedAttributeUpperValue) {
        calculatedFinalRange = MakeAttributeRange(finalRange.lowerValue, finalRange.upperValue + bonus);
    }
    
    return calculatedFinalRange;
}

- (AttributeRange)calculateValue {
    
    _finalRange = self.baseRange;
    
    NSUInteger rawBonusValue = [self getRawBonusValue];
    
    _finalRange = [self calculateFinalRange:_finalRange fromBonus:rawBonusValue];

    NSUInteger timedBonusValue = [self getTimedBonusValue];
    
    _finalRange = [self calculateFinalRange:_finalRange fromBonus:timedBonusValue];
        
    return _finalRange;
}

- (AttributeRange)finalValue {

    return [self calculateValue];
}

@end
