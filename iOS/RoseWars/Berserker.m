//
//  Berserker.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/4/13.
//
//

#import "Berserker.h"
#import "PathFinderStep.h"
#import "GameManager.h"

@implementation Berserker

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kSpecialUnit;
        self.unitName = kBerserker;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(2, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 1)];
        
        self.range = 1;
        self.move = 1;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.defeatSound = @"infantry_defeated_sound.mp3";

        self.frontImageSmall = @"berserker_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"berserker_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Berserker alloc] init];
}

- (BOOL)allowPath:(NSArray *)path forActionType:(ActionTypes)actionType allLocations:(NSDictionary *)allLocations {
    
    BOOL allowPath = [super allowPath:path forActionType:actionType allLocations:allLocations];
    
    if (actionType == kActionTypeMelee) {
        
        PathFinderStep *endLocation = path.lastObject;
        Card *cardAtEndLocation = [allLocations objectForKey:endLocation.location];
        
        if (cardAtEndLocation != nil && cardAtEndLocation.cardColor != [GameManager sharedManager].currentGame.myColor) {
            if (path.count <= 4) {
                allowPath = YES;
            }
        }
    }
    
    return allowPath;
}

@end
