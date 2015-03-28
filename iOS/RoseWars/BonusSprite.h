//
//  BonusSprite.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>

@class HKAttribute;
@interface BonusSprite : SKSpriteNode {
    
}

@property (nonatomic, copy) NSString *bonusText;
@property (nonatomic, readonly) HKAttribute *attribute;

- (void)setBonusText:(NSString*)bonusText;

- (id)initWithAttribute:(HKAttribute*)attribute;

@end
