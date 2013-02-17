//
//  GameBoardNode.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/8/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameBoardNode.h"


@implementation GameBoardNode

@synthesize hasCard, card = _card;
@synthesize nodeSprite = _nodeSprite;

- (id)initWithSprite:(CCSprite *)sprite {
    
    self = [super init];
    
    if (self) {
        
        self.anchorPoint = ccp(0.5, 0.5);
        
        self.contentSize = CGSizeMake(64, 87);
        
        _nodeSprite = sprite;
        
        _nodeSprite.position = ccp(self.contentSize.width / 2, self.contentSize.height / 2);
        
        [self addChild:_nodeSprite];
    }
    
    return self;
}

- (BOOL)hasCard {
    
    return _card != nil;
}

-(NSString *)description {
    
    return [NSString stringWithFormat:@"Location in grid: row: %d column: %d",
            self.locationInGrid.row,
            self.locationInGrid.column];
}

@end
