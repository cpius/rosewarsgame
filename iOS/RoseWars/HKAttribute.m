//
//  HKAttribute.m
//  RoseWars
//
//  Created by Heine Kristensen on 09/02/15.
//  Copyright (c) 2015 Heine Skov Kristensen. All rights reserved.
//

#import "HKAttribute.h"

@implementation HKAttribute

@synthesize finalValue = _finalValue;

- (instancetype)initWithStartingValue:(NSInteger)startingValue {
    self = [super init];
    if (self) {
        _baseValue = startingValue;
        _rawBonuses = [[NSMutableArray alloc] init];
        _timedBonuses = [[NSMutableArray alloc] init];
    }
    
    return self;
}

- (TimedBonus*)addTimedBonus:(TimedBonus *)timedBonus {
    [self.timedBonuses addObject:timedBonus];
    
    [timedBonus startTimedBonus:self];
    
    if ([_delegate respondsToSelector:@selector(attribute:addedTimedBonus:)]) {
        [_delegate attribute:self addedTimedBonus:timedBonus];
    }
    
    return timedBonus;
}

- (RawBonus*)addRawBonus:(RawBonus *)rawBonus {
    [self.rawBonuses addObject:rawBonus];
    
    if ([_delegate respondsToSelector:@selector(attribute:addedRawBonus:)]) {
        [_delegate attribute:self addedRawBonus:rawBonus];
    }
    
    return rawBonus;
}

- (NSUInteger)getRawBonusValue {
    // Add values from raw bonuses
    NSUInteger rawBonusValue = 0;
    
    for (RawBonus *rawbonus in self.rawBonuses) {
        rawBonusValue += rawbonus.bonusValue;
    }
    
    return rawBonusValue;
}

- (NSUInteger)getTimedBonusValue {
    // Add values from final bonuses
    NSUInteger timedBonusValue = 0;
    
    for (TimedBonus *timedbonus in self.timedBonuses) {
        timedBonusValue += timedbonus.bonusValue;
    }
    
    return timedBonusValue;
}

- (void)removeTimedBonus:(TimedBonus *)timedBonus {
    if ([self.timedBonuses containsObject:timedBonus]) {
        [self.timedBonuses removeObject:timedBonus];
        
        if ([_delegate respondsToSelector:@selector(attribute:removedTimedBonus:)]) {
            [_delegate attribute:self removedTimedBonus:timedBonus];
        }
    }
}

- (void)removeRawBonus:(RawBonus *)rawBonus {
    if ([self.rawBonuses containsObject:rawBonus]) {
        [self.rawBonuses removeObject:rawBonus];
        
        if ([_delegate respondsToSelector:@selector(attribute:removedRawBonus:)]) {
            [_delegate attribute:self removedRawBonus:rawBonus];
        }
    }
}

- (NSInteger)calculateFinalValue:(NSInteger)finalValue fromBonus:(NSUInteger)bonus {
    NSInteger calculatedFinalValue = finalValue + bonus;
    
        if (self.valueLimit != 0) {
            calculatedFinalValue = MIN(self.valueLimit, calculatedFinalValue);
        }
    
    return calculatedFinalValue;
}

- (NSInteger)calculateValue {
    _finalValue = self.baseValue;
    
    NSUInteger rawBonusValue = [self getRawBonusValue];
    
    _finalValue = [self calculateFinalValue:_finalValue fromBonus:rawBonusValue];
    
    NSUInteger timedBonusValue = [self getTimedBonusValue];
    
    _finalValue = [self calculateFinalValue:_finalValue fromBonus:timedBonusValue];
    
    return _finalValue;
}

- (NSUInteger)getTotalBonusValue {
    
    return [self getRawBonusValue] + [self getTimedBonusValue];
}

- (NSInteger)finalValue {
    return [self calculateValue];
}

@end
