//
//  ShortestPathStep.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import <Foundation/Foundation.h>

@interface PathFinderStep : NSObject

@property (nonatomic, strong) GridLocation *location;
@property (nonatomic, assign) int gScore;
@property (nonatomic, assign) int hScore;
@property (nonatomic, assign) PathFinderStep *parent;

- (id)initWithLocation:(GridLocation*)loc;
- (int)fScore;

@end
