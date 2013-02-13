//
//  BoardFrame.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/6/13.
//
//

#import "BoardFrame.h"

@implementation BoardFrame

- (id)initWithXCount:(int)xCount yCount:(int)yCount frameWidth:(float)frameWidth frameHeight:(float)frameHeight margin:(float)margin scale:(float)scale perimeterScale:(float)perimeterScale {

    self = [super init];
    
    if (self) {
        _xCount = xCount;
        _yCount = yCount;
        
        float boardScale = frameHeight / frameWidth;
        
        float x = 1 * xCount;
        float y = scale * yCount;
        
        float cardSumScale = y / x;
        
        BOOL xPrimary = boardScale > cardSumScale;
        if (xPrimary) {
            _xOffset = (frameWidth - (2.0f * margin)) / (xCount);
            _yOffset = _xOffset * scale;
        } else {
            _yOffset = (frameHeight - (2.0f * margin)) / (yCount);
            _xOffset = _yOffset / scale;
            _xCenterOffset = frameWidth - (_yOffset * yCount) / 2;
        }
        
        _xPerimeterSize = _xOffset * perimeterScale;
        _yPerimeterSize = _yOffset * perimeterScale;
        
        _yMove = frameHeight - (_yOffset * yCount);
    }
    
    return self;
}

- (CGPoint)getPositionWithX:(int)x andY:(int)y {
    
    float xPos = (((float) (x + 1)) * (float) _xOffset) - _xOffset / 2 + _xCenterOffset;
    float yPos = (((float) (y + 1)) * (float) _yOffset) - _yOffset / 2;
    
    return ccp(xPos, yPos + _yMove);
}

- (CGRect)getPerimeterWithX:(int)x andY:(int)y {
    
    CGPoint position = [self getPositionWithX:x andY:y];
    
    float rectX = position.x - _xPerimeterSize / 2;
    float recty = position.y - _yPerimeterSize / 2;
    
    return CGRectMake(rectX, recty, _xPerimeterSize, _yPerimeterSize);
}

- (GridLocation)getGridLocationInPoint:(CGPoint)point {
    
    for (int x = 0; x < _xCount; x++) {
        for (int y = 0; y < _yCount; y++) {
            
            CGRect perimeter = [self getPerimeterWithX:x andY:y];
            
            if (CGRectContainsPoint(perimeter, point)) {
                return MakeGridLocation(x, y);
            }
        }
    }
    return GridLocationEmpty;
}

- (float)getLaneWidth {
    
    return _xOffset;
}

@end
