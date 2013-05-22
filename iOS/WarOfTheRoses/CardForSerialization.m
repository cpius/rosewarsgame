//
//  CardForSerialization.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/24/13.
//
//

#import "CardForSerialization.h"
#import "TimedAbilityForSerialization.h"
#import "Card.h"

#import "ImproveWeapons.h"

@implementation CardForSerialization

- (id)initWithCard:(Card*)card {

    self = [super init];
    
    if (self) {
        
        _affectedByAbilities = [NSMutableArray array];
        
        _row = @(card.cardLocation.row);
        _column = @(card.cardLocation.column);
        _unitName = @(card.unitName);
        _cardColor = @(card.cardColor);
        _hitpoints = @(card.hitpoints);
        _experience = @(card.experience);
        _identifier = card.cardIdentifier;
        
        _attackBonus = @([card.attack getRawBonusValue]);
        _defenseBonus = @([card.defence getRawBonusValue]);
        
        for (TimedAbility *ability in card.currentlyAffectedByAbilities) {
            [_affectedByAbilities addObject:[[[TimedAbilityForSerialization alloc] initWithTimedAbility:ability currentTurn:[GameManager sharedManager].currentGame.turnCounter] asDictionary]];
        }
        
        _cardSpecificStats = [NSDictionary dictionaryWithDictionary:[card asDictionary]];
    }
    
    return self;
}

- (NSDictionary *)asDictionary {
    
    NSMutableDictionary *gamedata = [NSMutableDictionary dictionaryWithObjectsAndKeys:_row, @"row",
            _column, @"column",
            _unitName, @"unitname",
            _cardColor, @"cardcolor",
            _attackBonus, @"attackbonus",
            _defenseBonus, @"defensebonus",
            _hitpoints, @"hitpoints",
            _experience, @"experience",
            _identifier, @"identifier",
            nil];
    
    [gamedata setValue:_affectedByAbilities forKey:@"abilities"];
    [gamedata setValue:_cardSpecificStats forKey:@"card_specific_stats"];
    
    return gamedata;
}

- (NSString *)description {
    
    return [NSString stringWithFormat:@"%d-%d", _row.integerValue, _column.integerValue];
} 

@end
