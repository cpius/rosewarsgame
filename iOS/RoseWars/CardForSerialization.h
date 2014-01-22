//
//  CardForSerialization.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/24/13.
//
//

#import <Foundation/Foundation.h>

@interface CardForSerialization : NSObject {
    
    NSDictionary *_cardSpecificStats;
}

@property (nonatomic, readonly) NSNumber *row;
@property (nonatomic, readonly) NSNumber *column;

@property (nonatomic, readonly) NSNumber *cardType;
@property (nonatomic, readonly) NSNumber *unitType;
@property (nonatomic, readonly) NSNumber *unitName;
@property (nonatomic, readonly) NSNumber *unitAttackType;
@property (nonatomic, readonly) NSNumber *cardColor;
@property (nonatomic, readonly) NSNumber *hitpoints;
@property (nonatomic, readonly) NSNumber *experience;
@property (nonatomic, readonly) NSString *identifier;

@property (nonatomic, readonly) NSNumber *attackBonus;
@property (nonatomic, readonly) NSNumber *defenseBonus;

@property (nonatomic, readonly) NSMutableArray *affectedByAbilities;

- (id)initWithCard:(Card*)card;
- (NSDictionary*)asDictionary;

@end
