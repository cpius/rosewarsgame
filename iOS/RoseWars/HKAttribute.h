//
//  HKAttribute.h
//  RoseWars
//
//  Created by Heine Kristensen on 09/02/15.
//  Copyright (c) 2015 Heine Skov Kristensen. All rights reserved.
//

#import <Foundation/Foundation.h>

@class HKAttribute;
@protocol AttributeDelegate <NSObject>

@optional

- (void)attribute:(HKAttribute*)attribute addedRawBonus:(RawBonus*)rawBonus;
- (void)attribute:(HKAttribute*)attribute addedTimedBonus:(TimedBonus*)timedBonus;

- (void)attribute:(HKAttribute*)attribute removedRawBonus:(RawBonus*)rawBonus;
- (void)attribute:(HKAttribute*)attribute removedTimedBonus:(TimedBonus*)timedBonus;

@end

@interface HKAttribute : NSObject

@property (nonatomic, weak) id<AttributeDelegate> delegate;

@property (nonatomic, copy) NSMutableArray *timedBonuses;
@property (nonatomic, copy) NSMutableArray *rawBonuses;

@property (nonatomic, readonly) NSInteger finalValue;
@property (nonatomic, readonly) NSInteger baseValue;
@property (nonatomic, assign) NSInteger valueLimit;

@property (nonatomic, copy) NSString *attributeAbbreviation;

- (RawBonus*)addRawBonus:(RawBonus*)rawBonus;
- (NSUInteger)getRawBonusValue;

- (TimedBonus*)addTimedBonus:(TimedBonus*)timedBonus;
- (NSUInteger)getTimedBonusValue;

- (NSUInteger)getTotalBonusValue;

- (void)removeRawBonus:(RawBonus*)rawBonus;
- (void)removeTimedBonus:(TimedBonus*)timedBonus;

- (NSInteger)calculateValue;

- (instancetype)initWithStartingValue:(NSInteger)startingValue;

@end
