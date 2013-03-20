//
//  Lancer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/8/13.
//
//

#import "Lancer.h"
#import "Action.h"
#import "PathFinderStep.h"
#import "GameManager.h"
#import "TimedBonus.h"

@implementation Lancer

-(id)init {
    self = [super init];
    
    if (self) {
        
        self.cardType = kCardTypeSpecialUnit;
        self.unitType = kCavalry;
        self.unitName = kFlagBearer;
        self.unitAttackType = kUnitAttackTypeMelee;
        
        self.attack = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(5, 6)];
        
        self.defence = [[RangeAttribute alloc] initWithStartingRange:MakeAttributeRange(1, 3)];
        
        self.range = 1;
        self.move = 3;
        self.moveActionCost = self.attackActionCost = 1;
        self.hitpoints = 1;
        
        self.attackSound = @"sword_sound.wav";
        self.frontImageSmall = @"lancer_icon.png";
        self.frontImageLarge = [NSString stringWithFormat:@"lancer_%d.png", self.cardColor];
        
        [self commonInit];
    }
    
    return self;
}

+ (id)card {
    
    return [[Lancer alloc] init];
}

- (void)willPerformAction:(Action *)action {
    
    [super willPerformAction:action];

    if (action.isAttack) {
        
        // If it starts with 2 empty tiles between lancer and the unit it attacks +2A
        if (action.path.count > 1) {
            GridLocation *firstLocation = [action.path[0] location];
            GridLocation *secondLocation = [action.path[1] location];
            
            if ([[GameManager sharedManager] cardLocatedAtGridLocation:firstLocation] == nil &&
                [[GameManager sharedManager] cardLocatedAtGridLocation:secondLocation] == nil) {
                
                CCLOG(@"Lancer gets +2A because 2 empty tiles exist between lancer and enemy");
                
                [self.attack addTimedBonus:[[TimedBonus alloc] initWithValue:2 forNumberOfRounds:1]];
            }
        }
        
        if (action.enemyCard.unitName == kLancer) {
            
            // +1A against lancer
            
            CCLOG(@"Lancer gets +1A because attacking enemy lancer");
            
            _bonusAgainstLancer = [[RawBonus alloc] initWithValue:1];
            [self.attack addRawBonus:_bonusAgainstLancer];
        }
    }
}

- (void)didPerformedAction:(Action *)action {
    
    [super didPerformedAction:action];
    
    if (action.isAttack) {
        
        if (action.enemyCard.unitName == kLancer) {
            
            [self.attack removeRawBonus:_bonusAgainstLancer];
        }
    }
}

@end
