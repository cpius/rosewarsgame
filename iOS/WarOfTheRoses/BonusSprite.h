//
//  BonusSprite.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "cocos2d.h"
#import "RangeAttribute.h"

@interface BonusSprite : CCSprite {
    
}

@property (nonatomic, copy) NSString *bonusText;
@property (nonatomic, readonly) RangeAttribute *attribute;

- (void)setBonusText:(NSString*)bonusText;

- (id)initWithAttribute:(RangeAttribute*)attribute;

@end
