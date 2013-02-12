//
//  ParticleHelper.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import <Foundation/Foundation.h>

#define HIGHLIGHT_ACTION_TAG    1000
#define PARTICLE_TAG            100

@interface ParticleHelper : NSObject

+ (void)highlightNode:(CCNode*)node forever:(BOOL)forever;
+ (void)stopHighlightingNode:(CCNode*)node;

+ (void)applyBurstToNode:(CCNode*)node;

@end
