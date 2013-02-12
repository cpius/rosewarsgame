//
//  CombatScene.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/3/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "CombatScene.h"

@implementation CombatScene

@synthesize myCard = _myCard;
@synthesize enemyCard = _enemyCard;

+ (id)sceneWithMyCard:(Card*)myCard enemyCard:(Card*)enemyCard {
    
    CCScene *scene = [CCScene node];
    
    CombatScene *layer = [[CombatScene alloc] initWithMyCard:myCard enemyCard:enemyCard];
    
    [scene addChild:layer];
    
    return scene;
}

- (id)initWithMyCard:(Card*)myCard enemyCard:(Card*)enemyCard {
    
    self = [super init];
    
    if (self) {
        
        _myCard = myCard;
        _enemyCard = enemyCard;
    }
    
    return self;
}

@end
