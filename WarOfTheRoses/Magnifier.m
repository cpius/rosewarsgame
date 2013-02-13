/*
 * Magnifier - a magnifier glass for Cocos2D
 *
 * For details, visit the Rombos blog:
 * http://rombosblog.wordpress.com/2012/02/28/modal-alerts-for-cocos2d/ 
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

#import "Magnifier.h"
#import "cocos2d.h"

// this is the implemention of the UIKit view that hovers over the OpenGL-view
@implementation MagnifierView

@synthesize magnifiedImage=magnifiedImage_;

- (id)initWithLoupeImage: (UIImage *) loupeImg {
    self = [super initWithFrame:CGRectMake(0, 0, loupeImg.size.width, loupeImg.size.height)];
    if (self) {
        self.backgroundColor = [UIColor clearColor];
        loupeImage = [loupeImg retain];
    }
    return self;
}

- (void)setMagnifiedImage:(UIImage *)magnifiedImage {
    
    [magnifiedImage_ autorelease];
    magnifiedImage_ = [magnifiedImage retain];
    
    // redraw ourselves
    [self setNeedsDisplay];
}


// draw the magnified area and the loupe frame on top of each other
- (void)drawRect:(CGRect)rect {
    
    // draw the magnified area
    [magnifiedImage_ drawInRect:rect];
            
    // draw the loupe image on top
    [loupeImage drawInRect:rect];
}

- (void)dealloc {
    [loupeImage release];
    [magnifiedImage_ release];
    [super dealloc];
}

@end


/**
 The Magnifier class is a CCNode wrapper that host the UIView with the loupe image and the magnified are. It allows you to use it in a Cocos2D scene like any other object.
 This is a "light" implementation that will not react to scaling, rotation or setting opacity etc.
 It just considers position changes, because I felt that this is suffcient for a magnifying glass. Look for CCUIViewWrapper class if you need more than that.
 */
@implementation Magnifier

@synthesize magnifierView, magnification=magnification_;

- (id)initWithMagnification: (float) magnification {
    self = [super init];
    if (self) {
              
        // reference point for position is below bottom middle, and even a bit lower for iPhone/iPod 
        self.anchorPoint = ccp(0.5,(UI_USER_INTERFACE_IDIOM() == UIUserInterfaceIdiomPad) ? -0.1:-0.25); 

        magnification_ = magnification;
        
        // create the magnifier UIView from our loupe image
        self.magnifierView = [[[MagnifierView alloc] initWithLoupeImage:[UIImage imageNamed:@"loupe.png"]] autorelease];
                
        // put this couple on top of everything else
        [[[CCDirector sharedDirector] openGLView] addSubview:magnifierView];
    }
    return self;
}

/**
 Grabbing the OpenGL buffer and converting it to an UIImage is more or less taken from a pretty long Cocos2D forum thread:
 http://www.cocos2d-iphone.org/forum/topic/1722
 I took one of the (many) mods in that thread, but grabbing just a piece of the whole screen. I also added releasing the CGImageRef after drawing the final bitmap representation, because else it leaked galore
 */
- (UIImage *) grabUIImageFromRect: (CGRect) rect {
    
    // make sure we consider retina res. correctly
    rect.origin.x *= CC_CONTENT_SCALE_FACTOR();
    rect.origin.y *= CC_CONTENT_SCALE_FACTOR();
    rect.size.width *= CC_CONTENT_SCALE_FACTOR();
    rect.size.height *= CC_CONTENT_SCALE_FACTOR();
        
    CGSize size = rect.size; 
    
    //Create buffer for pixels
    GLuint bufferLength = size.width * size.height * 4;
    GLubyte* buffer = (GLubyte*)malloc(bufferLength);
    memset(buffer, 255, bufferLength); // everything outside the screen area shown white
    
    //Read Pixels from OpenGL
    glReadPixels(rect.origin.x, rect.origin.y, size.width, size.height, GL_RGBA, GL_UNSIGNED_BYTE, buffer);
    //Make data provider with data.
    CGDataProviderRef provider = CGDataProviderCreateWithData(NULL, buffer, bufferLength, NULL);
    
    //Configure image
    int bitsPerComponent = 8;
    int bitsPerPixel = 32;
    int bytesPerRow = 4 * size.width;
    CGColorSpaceRef colorSpaceRef = CGColorSpaceCreateDeviceRGB();
    CGBitmapInfo bitmapInfo = kCGBitmapByteOrderDefault | kCGImageAlphaLast;
    CGColorRenderingIntent renderingIntent = kCGRenderingIntentDefault;
    CGImageRef iref = CGImageCreate(size.width, size.height, bitsPerComponent, bitsPerPixel, bytesPerRow, colorSpaceRef, bitmapInfo, provider, NULL, NO, renderingIntent);
    
    uint32_t* pixels = (uint32_t*)malloc(bufferLength);
    CGContextRef context = CGBitmapContextCreate(pixels, size.width, size.height, 8, size.width * 4, CGImageGetColorSpace(iref), kCGImageAlphaPremultipliedLast | kCGBitmapByteOrder32Big);
    
    CGContextTranslateCTM(context, 0, size.height);
    CGContextScaleCTM(context, 1.0f, -1.0f);
    
#if COCOS2D_VERSION < 0x00020000
    switch ([CCDirector sharedDirector].deviceOrientation)
    {
        case CCDeviceOrientationPortrait:
            break;
        case CCDeviceOrientationPortraitUpsideDown:
            CGContextRotateCTM(context, CC_DEGREES_TO_RADIANS(180));
            CGContextTranslateCTM(context, -size.width, -size.height);
            break;
        case CCDeviceOrientationLandscapeLeft:
            CGContextRotateCTM(context, CC_DEGREES_TO_RADIANS(-90));
            CGContextTranslateCTM(context, -size.height, 0);
            break;
        case CCDeviceOrientationLandscapeRight:
            CGContextRotateCTM(context, CC_DEGREES_TO_RADIANS(90));
            CGContextTranslateCTM(context, size.width * 0.5f, -size.height);
            break;
    }
#endif
    
    CGContextDrawImage(context, CGRectMake(0.0f, 0.0f, size.width, size.height), iref);
    
    CGImageRef imgRef = CGBitmapContextCreateImage(context);  
    UIImage *outputImage = [UIImage imageWithCGImage: imgRef];
    CGImageRelease(imgRef); // HJR: added this to reclaim the allocated memory (leaked before)
    
    //Dealloc
    CGDataProviderRelease(provider);
    CGImageRelease(iref);
    CGContextRelease(context);
    free(buffer);
    free(pixels);
    
    return outputImage;
}

/**
 The magnify method will grab an area right below the center of the loupe according to the current magnification setting, update the UIView and redraw it.
 It will automatically be called on position changes. If you want even more current changes for things happening below the loupe while it is not moved, you need to call "magnifiy" 
 */
- (void) magnify {

// this is the percentage of the actually magnified area within the loupe image (depending on the inner part size of the loupe graphics)
#define MAGNIFICATION_AREA_PCT 0.93 
    
    float magSize = magnifierView.frame.size.width; // I am sooo lazy -- works just for perfect squared loupe graphics!
    
    // create an internal bitmap to draw to
    UIGraphicsBeginImageContext(CGSizeMake(magSize, magSize));
    CGContextRef context = UIGraphicsGetCurrentContext();
    
    // setup clipping into inner area of magnifier
    CGContextBeginPath (context);
    CGContextAddArc(context, magSize/2, magSize/2, (magSize*MAGNIFICATION_AREA_PCT)/2, 0, 2*M_PI, 0);
    CGContextClosePath (context);
    CGContextClip (context);
    
    // now grab the source image according to magnification settings
    float sourceSize = magSize/magnification_;
    CGPoint center = ccp(self.position.x - magSize * self.anchorPoint.x + magSize/2, self.position.y - magSize * self.anchorPoint.y + magSize/2);
    UIImage *snapshotImage = [self grabUIImageFromRect: CGRectMake(center.x-sourceSize/2, center.y-sourceSize/2, sourceSize, sourceSize)];
    
    // draw the grabbed piece into the magnifer area. UIKit will be so nice to scale for us!
    [snapshotImage drawInRect:CGRectMake(0, 0, magSize, magSize)];    
    
    // set new magnified image
    magnifierView.magnifiedImage = UIGraphicsGetImageFromCurrentImageContext();
    
    UIGraphicsEndImageContext();
    
    // force redraw
    [magnifierView setNeedsDisplay];
}


/**
 If position is changed, also fix position of UIView, grab new area and redraw.
 The position is regarded as bottom middle of the loupe, so it will be above your finger. However, the magnification area will be beneath the center of the loupe area. However, you can easily set the anchorPoint to something different.
 */
- (void)setPosition:(CGPoint)position {
    [super setPosition:position];
    CGSize winSize = [CCDirector sharedDirector].winSize;
    
    // y-coord. is reversed for UIKit controls, and frame 0/0 is top left
    CGSize magSize = magnifierView.frame.size;
    magnifierView.frame = CGRectMake(position.x - magSize.width * self.anchorPoint.x, winSize.height - (position.y + magSize.height * (1-self.anchorPoint.y)), 
                                     magSize.width, magSize.height);
    
    [self magnify];    
}


/**
 If magnification is changed, we grab the underneath content anew and redraw the loupe
 */
- (void)setMagnification:(float)magnification {
    NSAssert(magnification != 0, @"Magnification can not be 0!");
    magnification_ = magnification;
    
    [self magnify];
}


- (void)dealloc {
    [magnifierView removeFromSuperview];
    [magnifierView release];
    [super dealloc];
}
@end
