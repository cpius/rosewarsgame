/*
 * Magnifier - a magnifier glass for Cocos2D
 *
 * For details, visit the Rombos blog:
 * http://bit.ly/RombosBlogMagnifierGlass 
 *
 * Copyright (c) 2012 Hans-Juergen Richstein, Rombos
 * http://www.rombos.de
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */


#import <Foundation/Foundation.h>
#import "cocos2d.h"

@class Magnifier; // forward decl.

// this is the UIKit view that hovers over the OpenGL-view
@interface MagnifierView : UIView {
    UIImage *loupeImage, *magnifiedImage_;
}

- (id)initWithLoupeImage: (UIImage *) loupeImg;

@property(nonatomic, retain) UIImage *magnifiedImage;

@end

// this is the CCNode wrapper which allows you to use the magnifier within a Cocos2D scene
@interface Magnifier : CCNode {
    float magnification_;
    CGPoint lastGrabPosition;
    MagnifierView *magnifierView;
}

@property(retain) MagnifierView *magnifierView;
@property(nonatomic) float magnification;

- (id)initWithMagnification: (float) magnification;
- (void) magnify;

@end
