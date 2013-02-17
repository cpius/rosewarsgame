//
//  Position.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/13/13.
//
//

#import "GridLocation.h"

@implementation GridLocation

@synthesize row = _row, column = _column;

- (id)initWithRow:(NSUInteger)row column:(NSUInteger)column {
    
    self = [super init];
    
    if (self) {
        _row = row;
        _column = column;
    }
    
    return self;
}

+ (id)gridLocationWithRow:(NSUInteger)row column:(NSUInteger)column {
    
    return [[GridLocation alloc] initWithRow:row column:column];
}

- (id)copyWithZone:(NSZone *)zone {
    
    GridLocation *copyLocation = [[GridLocation allocWithZone:zone] init];
    
    copyLocation.row = self.row;
    copyLocation.column = self.column;
    
    return copyLocation;
}

- (NSString *)description {
    
    return [NSString stringWithFormat:@"%d-%d", self.row, self.column];
}

- (NSUInteger)hash {
    
    return [[NSString stringWithFormat:@"%d%d", self.row, self.column] hash];
}

- (BOOL)isEqual:(id)object {
    
    if (![object isKindOfClass:[GridLocation class]]) {
        return NO;
    }
    
    GridLocation *location = object;
    
    BOOL isEqual = self.row == location.row &&
    self.column == location.column;
    
    return isEqual;
}

- (NSArray*)perpendicularLocationsFromLocation:(GridLocation*)location {
    
    return @[[GridLocation gridLocationWithRow:location.row + 1 column:location.column + 1],
    [GridLocation gridLocationWithRow:location.row - 1 column:location.column - 1]];
}

- (NSArray *)surroundingGridLocations {
    
    return @[[GridLocation gridLocationWithRow:self.row column:self.column - 1],
    [GridLocation gridLocationWithRow:self.row column:self.column + 1],
    [GridLocation gridLocationWithRow:self.row - 1 column:self.column],
    [GridLocation gridLocationWithRow:self.row + 1 column:self.column]];
}

@end
