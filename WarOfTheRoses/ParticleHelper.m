//
//  ParticleHelper.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import "ParticleHelper.h"

@implementation ParticleHelper

+ (void)highlightNode:(CCNode *)node forever:(BOOL)forever {
    
    CCCallBlockN *callBlock = [CCCallBlockN actionWithBlock:^(CCNode *node) {
        
        CCParticleSystem *particle = [CCParticleSystemQuad particleWithFile:@"sparks.plist"];
        particle.position = ccp(node.contentSize.width, 0);
        particle.scale = 0.5;
        particle.tag = PARTICLE_TAG;
        [node addChild:particle z:10];
        
        CCMoveTo *move1 = [CCMoveTo actionWithDuration:0.2 position:ccp(0, 0)];
        CCMoveTo *move2 = [CCMoveTo actionWithDuration:0.2 position:ccp(0, node.contentSize.height)];
        CCMoveTo *move3 = [CCMoveTo actionWithDuration:0.2 position:ccp(node.contentSize.width, node.contentSize.height)];
        CCMoveTo *move4 = [CCMoveTo actionWithDuration:0.2 position:ccp(node.contentSize.width, 0)];
        CCCallBlock *removeNodeBlock = [CCCallBlock actionWithBlock:^{
            [particle removeFromParentAndCleanup:YES];
        }];
        
        CCSequence *sequence = [CCSequence actions:move1, move2, move3, move4, nil];
        
        if (forever) {
            [particle runAction:[CCRepeatForever actionWithAction:sequence]];
        }
        else {
            [particle runAction:[CCSequence actions:sequence, removeNodeBlock, nil]];
        }
    }];
    
    callBlock.tag = HIGHLIGHT_ACTION_TAG;
    
    [node runAction:callBlock];
}

+ (void)stopHighlightingNode:(CCNode *)node {
    
    CCAction *action = [node getActionByTag:HIGHLIGHT_ACTION_TAG];
    
    if (action) {
        [action stop];
    }
    
    CCParticleSystem *particle = (CCParticleSystem*)[node getChildByTag:PARTICLE_TAG];
    [particle stopAllActions];
    [particle removeFromParentAndCleanup:YES];
}
@end
