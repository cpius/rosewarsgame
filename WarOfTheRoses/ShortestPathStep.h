//
//  ShortestPathStep.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import <Foundation/Foundation.h>

@interface ShortestPathStep : NSObject

@property (nonatomic, assign) GridLocation location;
@property (nonatomic, assign) int gScore;
@property (nonatomic, assign) int hScore;
@property (nonatomic, assign) ShortestPathStep *parent;

- (id)initWithLocation:(GridLocation)loc;
- (int)fScore;

@end
