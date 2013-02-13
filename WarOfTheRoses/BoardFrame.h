//
//  BoardFrame.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/6/13.
//
//

#import <Foundation/Foundation.h>

@interface BoardFrame : NSObject {
    
    float _xOffset;
	float _yOffset;
	float _yMove;
    
	int _xCount;
	int _yCount;
    
	float _xCenterOffset;
	float _xPerimeterSize;
	float _yPerimeterSize;

}

- (CGPoint)getPositionWithX:(int)x andY:(int)y;
- (CGRect)getPerimeterWithX:(int)x andY:(int)y;
- (GridLocation)getGridLocationInPoint:(CGPoint)point;
- (float)getLaneWidth;

- (id)initWithXCount:(int)xCount yCount:(int)yCount frameWidth:(float)frameWidth frameHeight:(float)frameHeight margin:(float)margin scale:(float)scale perimeterScale:(float)perimeterScale;

@end
