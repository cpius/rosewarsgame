//
//  CombatScene.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/3/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Card.h"

@interface CombatScene : CCLayer {
    
    
}

@property (nonatomic, readonly) Card *myCard;
@property (nonatomic, readonly) Card *enemyCard;

+ (id)sceneWithMyCard:(Card*)myCard enemyCard:(Card*)enemyCard;
- (id)initWithMyCard:(Card*)myCard enemyCard:(Card*)enemyCard;

@end
