//
//  GridlLayoutManager.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/6/12.
//
//

#import "CCNode.h"

@interface GridlLayoutManager : CCNode

@property (nonatomic, assign) CGSize gridSize;
@property (nonatomic, assign) NSInteger yOffset;
@property (nonatomic, assign) NSInteger xOffset;
@property (nonatomic, assign) NSInteger numberOfRows;
@property (nonatomic, assign) NSInteger numberOfColumns;

@property (nonatomic, assign) NSInteger rowPadding;
@property (nonatomic, assign) NSInteger columnPadding;

@property (nonatomic, assign) NSUInteger columnWidth;
@property (nonatomic, assign) NSUInteger rowHeight;

+ (GridlLayoutManager*)sharedManager;

- (CGPoint)getPositionForRowNumber:(NSInteger)rowNumber columnNumber:(NSInteger)columnNumber;

@end
