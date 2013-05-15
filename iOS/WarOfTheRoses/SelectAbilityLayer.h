//
//  SelectAbilityLayer.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 5/10/13.
//
//

#import "CCLayer.h"

typedef enum {
    kAbilityRaiseTypeAttack = 0,
    kAbilityRaiseTypeDefense
} AbilityRaiseTypes;

@class SelectAbilityLayer;
@protocol SelectAbilityProtocol <NSObject>

- (void)layer:(SelectAbilityLayer*)layer selectedAbilityRaiseType:(AbilityRaiseTypes)type;

@end

@interface SelectAbilityLayer : CCLayerColor

@property (nonatomic, weak) id<SelectAbilityProtocol> delegate;

@end
