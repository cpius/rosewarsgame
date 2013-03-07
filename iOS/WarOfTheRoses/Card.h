//
//  Card.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "CCSprite.h"
#import "RangeAttribute.h"
#import "GridLocation.h"
#import "TimedAbility.h"

@class Card;
@protocol CardDelegate <NSObject>

@optional
- (void)cardIncreasedInLevel:(Card*)card;

@end

@class Action;
@interface Card : CCNode <TimedAbilityDelegate> {

    BOOL hasSpecialAbility;
}

/*
 Angiver om der er tale om en basic unit eller en special unit
 */
@property (nonatomic, weak) id<CardDelegate> delegate;
@property (nonatomic, assign) CardType cardType;
@property (nonatomic, assign) UnitType unitType;
@property (nonatomic, assign) UnitName unitName;
@property (nonatomic, assign) CardColors cardColor;
@property (nonatomic, strong) NSString *frontImageLarge;
@property (nonatomic, strong) NSString *frontImageSmall;
@property (nonatomic, strong) NSString *backImage;
@property (nonatomic, strong) GridLocation *cardLocation;
@property (nonatomic, assign) BOOL isShowingDetail;
@property (nonatomic, assign) NSUInteger movesConsumed;
@property (nonatomic, readonly) NSInteger movesRemaining;

@property (nonatomic, copy) NSString *attackSound;
@property (nonatomic, copy) NSString *defenceSound;
@property (nonatomic, copy) NSString *moveSound;
/*
 Samme mekanisme som range, man kan bevæge sig til siden og fremad eller bagud. Man kan ikke bevæge sig ind I et felt som er optaget af en anden unit. Man kan heller ikke gå igennem egne eller modstanderens units.
 Eksempel: Hvis en unit har move 2 og range 1 har den unit følgende muligheder:
 Bevæge sig to squares
 Bevæge sig 1 square og angribe en tilstødende square
 Angribe en gang, et angreb konsumerer alle resterende moves
 
 */
@property (nonatomic, assign) NSUInteger move;


/*
 Angiver hvilket interval på en d6 hvori unit laver et succesfuldt angreb. Et succesfuldt angreb medfører at den angrebne unit skal lave et defense roll. Hvis defense roll ikke lykkes dør den forsvarende unit og den angribende unit tilføres et experience point. Ydermere kan den angribende unit overtage den forsvarende units plads. Hvis den forsvarende unit klarer sit defense roll overlever den. Et attack tæller som et move og konsumerer alle restenrende moves, se nedenfor under Move
 */
@property (nonatomic, strong) RangeAttribute *attack;

/*
 Angiver hvilket interval på en d6 hvori unit laver et succesfuldt forsvar. Reglerne er som beskrevet ovenfor under Attack.
 */
@property (nonatomic, strong) RangeAttribute *defence;

/*
 (sekundær stat som kun behøver at være tilgængelig når man zoomer ind på kortet):
 En unit modtager et experience point hver gang den slår en anden unit ihjel. Når en unit har to experience points bliver disse vekslet til enten +1 angreb eller +1 forsvar. Dette kan maximalt ske to gange for den samme unit.
 */
@property(nonatomic, assign) NSInteger experience;

/* Indikerer hvor mange gange enheden er gået op i level
 */
@property (nonatomic, assign) NSUInteger numberOfLevelsIncreased;


/*
 Angiver rækkevidden på en units angreb, hver square tæller for 1 range, dvs en unit med range 1 kan angribe de  felter umiddelbart ved siden af sig.
 */
@property(nonatomic, assign) NSUInteger range;
@property(nonatomic, readonly) BOOL isRanged;
@property(nonatomic, assign) BOOL dead;

/*
 Hver spiller har 2 actions hver tur. En action vil være et move eller et angreb, der er dog nogle units (catapult) hvis angreb tager 2 actions, derfor kan man ikke bevæge eller angribe med andre units hvis man burger catapult. Den samme unit kan ikke angribe OG bevæge sig I samme runde jo mindre andet er specificeret på kortet.
 */
@property(nonatomic, assign) NSUInteger attackActionCost;
@property(nonatomic, assign) NSUInteger moveActionCost;

@property(nonatomic, assign) BOOL hasReceivedExperiencePointsThisRound;
@property(nonatomic, assign) BOOL hasPerformedActionThisRound;
@property(nonatomic, assign) BOOL hasPerformedAttackThisRound;

@property(nonatomic, readonly) NSMutableArray *timedAbilities;

- (void)commonInit;

- (void)consumeAllMoves;
- (void)consumeMove;
- (void)consumeMoves:(NSUInteger)moves;

- (void)willPerformAction:(Action*)action;
- (void)didPerformedAction:(Action*)action;

- (BOOL)canPerformActionOfType:(ActionTypes)actionType withRemainingActionCount:(NSUInteger)remainingActionCount;
- (BOOL)allowPath:(NSArray*)path forActionType:(ActionTypes)actionType allLocations:(NSDictionary*)allLocations;

- (BOOL)zoneOfControlAgainst:(Card*)opponent;
- (BOOL)specialAbilityTriggersVersus:(Card*) opponent;
- (void)addSpecialAbilityVersusOpponent:(Card*)opponent;

- (void)levelIncreased;
- (BOOL)isOwnedByPlayerWithColor:(PlayerColors)playerColor;

- (void)combatFinishedAgainstDefender:(Card*)defender withOutcome:(CombatOutcome)combatOutcome;
- (void)combatFinishedAgainstAttacker:(Card*)attacker withOutcome:(CombatOutcome)combatOutcome;

- (void)addTimedAbility:(TimedAbility*)timedAbility;

@end
