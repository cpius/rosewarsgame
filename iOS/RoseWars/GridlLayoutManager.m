//
//  GridlLayoutManager.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/6/12.
//
//

#import "GridlLayoutManager.h"

@interface GridlLayoutManager()


@end

@implementation GridlLayoutManager

@synthesize rowPadding, columnPadding;
@synthesize numberOfColumns, numberOfRows;
@synthesize gridSize;
@synthesize yOffset, xOffset;
@synthesize columnWidth, rowHeight;

+ (GridlLayoutManager*)sharedManager {
    
    static GridlLayoutManager* _instance = nil;
    
    @synchronized(self) {
        
        if (_instance == nil) {
            _instance = [[GridlLayoutManager alloc] init];
        }
    }
    
    return _instance;
}

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        self.rowPadding = 10;
        self.columnPadding = 10;
    }
    
    return self;
}

- (CGPoint)getPositionForRowNumber:(NSInteger)rowNumber columnNumber:(NSInteger)columnNumber {
    
    if (rowNumber > numberOfRows || columnNumber > numberOfColumns) {
        return CGPointZero;
    }
        
    NSInteger x = (columnPadding * columnNumber) + (self.columnWidth * (columnNumber - 1));
    NSInteger y = yOffset - ((rowPadding * rowNumber) + (self.rowHeight * (rowNumber - 1)));
    
    return CGPointMake(xOffset + x + (self.columnWidth / 2) , y - (self.rowHeight / 2));
}

@end
