//
//  AttackPathFinderStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/15/13.
//
//

#import "MeleeAttackPathFinderStrategy.h"
#import "Card.h"

@implementation MeleeAttackPathFinderStrategy

- (id)initWithMeleeAttackType:(MeleeAttackTypes)meleeAttackType {
    
    self = [super init];
    
    if (self) {
        _meleeAttackType = meleeAttackType;
    }
    
    return self;
}

+ (id)strategy {
    
    return [[MeleeAttackPathFinderStrategy alloc] initWithMeleeAttackType:kMeleeAttackTypeConquer];
}

+ (id)strategyWithMeleeAttackType:(MeleeAttackTypes)attackType {
    
    return [[MeleeAttackPathFinderStrategy alloc] initWithMeleeAttackType:attackType];
}

- (NSArray*)getReachableLocationsForCard:(Card*)card fromLocation:(GridLocation*)fromLocation targetLocation:(GridLocation*)targetLocation allLocations:(NSDictionary *)allLocations {
    
    Card *targetCard = [allLocations objectForKey:targetLocation];

    NSMutableArray *adjacentLocations = [NSMutableArray array];
    NSArray *surroundingGridLocations = [fromLocation surroundingGridLocations];
    
    for (GridLocation *gridLocation in surroundingGridLocations) {

        if ([gridLocation isInsideGameBoard]) {
            Card *cardAtToLocation = [allLocations objectForKey:gridLocation];
            
            if (cardAtToLocation == nil || cardAtToLocation == targetCard) {
                
                // Only melee attacks with conquer check for ZOC
                if (_meleeAttackType == kMeleeAttackTypeConquer) {
                    if (![self card:card blockedByZoneOfControlUnitWhenMovingFromLocation:fromLocation toLocation:gridLocation allLocations:allLocations]) {
                        [adjacentLocations addObject:gridLocation];
                    }
                }
                else {
                    [adjacentLocations addObject:gridLocation];
                }
            }
        }
    }

    return [NSArray arrayWithArray:adjacentLocations];
}

@end
