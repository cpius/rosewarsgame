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
@synthesize yOffset;

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

- (float)widthForColumn {
    
    float width = gridSize.width  / numberOfColumns;
    
    return width;
}

- (float)heightForRow {
    
    float height = (gridSize.height - (rowPadding * numberOfRows)) / numberOfRows;
    
    return height;
}

- (CGPoint)getPositionForRowNumber:(NSInteger)rowNumber columnNumber:(NSInteger)columnNumber {
    
    if (rowNumber > numberOfRows || columnNumber > numberOfColumns) {
        return CGPointZero;
    }
    
    float widthForColumn = [self widthForColumn];
    float heightForRow = [self heightForRow];
    
    NSInteger x = (columnPadding * columnNumber) + (widthForColumn * (columnNumber - 1));
    NSInteger y = yOffset - ((rowPadding * rowNumber) + (heightForRow * (rowNumber - 1)));
    
    return CGPointMake(x + (widthForColumn / 2) , y - (heightForRow / 2));
}

@end
