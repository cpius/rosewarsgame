//
//  GCTurnBasedMatchHelper.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/18/12.
//
//

#import "GCTurnBasedMatchHelper.h"

@implementation GCTurnBasedMatchHelper

@synthesize gameCenterAvailable = _gameCenterAvailable;
@synthesize currentMatch = _currentMatch;
@synthesize delegate = _delegate;

+ (GCTurnBasedMatchHelper *)sharedInstance {
    
    static GCTurnBasedMatchHelper *_instance = nil;
    static dispatch_once_t onceToken;
    
    dispatch_once(&onceToken, ^{
        _instance = [[GCTurnBasedMatchHelper alloc] init];
    });
    
    return _instance;
}

- (id)init {
    
    self = [super init];
    
    if (self) {
        _gameCenterAvailable = [self isGameCenterAvailable];
        
        if (_gameCenterAvailable) {
 //           [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(authenticationChanged) name:GKPlayerAuthenticationDidChangeNotificationName object:nil];
        }
    }
    
    return self;
}

- (void)handleInviteFromGameCenter:(NSArray *)playersToInvite {
    
    NSLog(@"New invite from players: %@", playersToInvite);
    
    [_presentingViewController dismissViewControllerAnimated:YES completion:nil];
    
    GKMatchRequest *request = [[GKMatchRequest alloc] init];
    
    request.playersToInvite = playersToInvite;
    request.minPlayers = 2;
    request.maxPlayers = 2;
    
    GKTurnBasedMatchmakerViewController *viewController = [[GKTurnBasedMatchmakerViewController alloc] initWithMatchRequest:request];
    
    viewController.showExistingMatches = NO;
    viewController.turnBasedMatchmakerDelegate = self;
    
    [_presentingViewController presentViewController:viewController animated:YES completion:nil];
}

- (NSArray *)currentPlayerIds {
    
    NSMutableArray *participants = [NSMutableArray array];
    
    for (GKTurnBasedParticipant *participant in [GCTurnBasedMatchHelper sharedInstance].currentMatch.participants) {
        [participants addObject:participant.playerID];
    }
    
    return [NSArray arrayWithArray:participants];
}

- (void)handleTurnEventForMatch:(GKTurnBasedMatch *)match {
    
    NSLog(@"Turn has happened in match: %@", match);
    
    if ([match.matchID isEqualToString:_currentMatch.matchID]) {
        if ([match.currentParticipant.playerID isEqualToString:[GKLocalPlayer localPlayer].playerID]) {
                        
            // It's the current match, and it's our turn now
            _currentMatch = match;
            [_delegate takeTurn:match];
        }
    }
    else {
        if ([match.currentParticipant.playerID isEqualToString:[GKLocalPlayer localPlayer].playerID]) {
            
            for (GKTurnBasedParticipant *participant in match.participants) {
                
                if (participant.matchOutcome == GKTurnBasedMatchOutcomeQuit) {
                    [_delegate sendNotice:[NSString stringWithFormat:@"%@ has quit your match", participant.playerID] forMatch:match];
                    return;
                }
            }
            
            // It's not the current match and it's our turn now
            [_delegate sendNotice:@"It's your turn for another match" forMatch:match];
        }
        else {
            // It's not the current match, and it's someone else's turn
        }
    }
}

- (void)gameCenterViewControllerDidFinish:(GKGameCenterViewController *)gameCenterViewController {
    
    [gameCenterViewController dismissViewControllerAnimated:YES completion:nil];
}


- (void)handleMatchEnded:(GKTurnBasedMatch *)match {
    
    NSLog(@"Game has ended: %@", match);
    [_delegate takeTurn:match];
}

- (void)turnBasedMatchmakerViewController:(GKTurnBasedMatchmakerViewController *)viewController didFailWithError:(NSError *)error {
    
    [viewController dismissViewControllerAnimated:YES completion:nil];
    
    NSLog(@"Error finding match: %@", error.localizedDescription);
}

- (void)turnBasedMatchmakerViewController:(GKTurnBasedMatchmakerViewController *)viewController didFindMatch:(GKTurnBasedMatch *)match {
    
    [viewController dismissViewControllerAnimated:YES completion:nil];
    
    NSLog(@"Did find match: %@", match);
    
    _currentMatch = match;
    
    GKTurnBasedParticipant *firstParticipant = [match.participants objectAtIndex:0];
    
    if (firstParticipant.lastTurnDate == nil) {
        [_delegate enterNewGame:match];
    }
    else {
        
        if ([match.currentParticipant.playerID isEqualToString:[GKLocalPlayer localPlayer].playerID]) {
            [_delegate takeTurn:match];
        }
        else {
            [_delegate layoutMatch:match];
        }
    }
}

- (void)endMatchWithData:(NSData*)data gameResult:(GameResults)gameResult {
    
    NSUInteger currentIndex = [_currentMatch.participants
                               indexOfObject:_currentMatch.currentParticipant];
    
    GKTurnBasedParticipant *nextParticipant = [_currentMatch.participants objectAtIndex:
                                               ((currentIndex + 1) % [_currentMatch.participants count ])];
    
    if (gameResult != kGameResultInProgress) {
        if (gameResult == kGameResultVictory) {
            _currentMatch.currentParticipant.matchOutcome = GKTurnBasedMatchOutcomeWon;
            nextParticipant.matchOutcome = GKTurnBasedMatchOutcomeLost;
            
            [self submitScoreForPlayer:_currentMatch.currentParticipant];
            
            _currentMatch.message = [NSString stringWithFormat:@"You lost the game against %@", [GKLocalPlayer localPlayer].alias];
        }
        else if (gameResult == kGameResultDefeat) {
            _currentMatch.currentParticipant.matchOutcome = GKTurnBasedMatchOutcomeLost;
            nextParticipant.matchOutcome = GKTurnBasedMatchOutcomeWon;
            
            _currentMatch.message = [NSString stringWithFormat:@"You won the game against %@", [GKLocalPlayer localPlayer].alias];
        }
        
        [_currentMatch endMatchInTurnWithMatchData:data completionHandler:^(NSError *error) {
            
            if (error) {
                NSLog(@"%@", error);
            }
        }];
    }
}

- (void)endTurnWithData:(NSData *)data {
    
    NSUInteger currentIndex = [_currentMatch.participants
                               indexOfObject:_currentMatch.currentParticipant];
    
    GKTurnBasedParticipant *nextParticipant = [_currentMatch.participants objectAtIndex:
                                               ((currentIndex + 1) % [_currentMatch.participants count ])];
    
    NSLog(@"Send Turn, %@, %@", data, nextParticipant);
    
    _currentMatch.message = [NSString stringWithFormat:@"It's your turn against %@", [GKLocalPlayer localPlayer].alias];
    
    [_currentMatch endTurnWithNextParticipants:@[nextParticipant] turnTimeout:60*24*7 matchData:data completionHandler:^(NSError *error) {
        if (error) {
            [GKNotificationBanner showBannerWithTitle:@"Notice!" message:@"Couldn't end turn. Maybe your opponent has quit the match" completionHandler:^{
                
            }];
        }
    }];
}

- (void)submitScoreForPlayer:(GKTurnBasedParticipant*)player {
    
    [GKLeaderboard loadLeaderboardsWithCompletionHandler:^(NSArray *leaderboards, NSError *error) {
        
        // We only have one leaderboard
        GKLeaderboard *defaultLeaderBoard = leaderboards[0];
        
        [defaultLeaderBoard loadScoresWithCompletionHandler:^(NSArray *scores, NSError *error) {
            
            GKScore *scoreReporter = [[GKScore alloc] initWithLeaderboardIdentifier:kLeaderBoardCategory];
            
            scoreReporter.value = defaultLeaderBoard.localPlayerScore.value + 1;
            
            [GKScore reportScores:@[scoreReporter] withCompletionHandler:^(NSError *error) {
                if (error) {
                    NSLog(@"Error reporting score: %@", error);
                }
            }];
        }];
    }];
    
}

- (void)turnBasedMatchmakerViewController:(GKTurnBasedMatchmakerViewController *)viewController playerQuitForMatch:(GKTurnBasedMatch *)match {
        
    NSUInteger currentIndex = [match.participants indexOfObject:match.currentParticipant];
    
    GKTurnBasedParticipant *participant;
    
    for (int i = 0; i < match.participants.count; i++) {
        participant = [match.participants objectAtIndex:(currentIndex + 1 + i) % match.participants.count];
        
        if (participant.matchOutcome != GKTurnBasedMatchOutcomeQuit) {
            break;
        }
    }
    
    NSLog(@"Player: %@ quit for match: %@", match.currentParticipant, match);
    
    [match participantQuitInTurnWithOutcome:GKTurnBasedMatchOutcomeQuit nextParticipants:@[participant] turnTimeout:60*24*7 matchData:match.matchData completionHandler:^(NSError *error) {
        
    }];
}

- (void)turnBasedMatchmakerViewControllerWasCancelled:(GKTurnBasedMatchmakerViewController *)viewController {
    
    [viewController dismissViewControllerAnimated:YES completion:nil];
    
    NSLog(@"Has cancelled");
}

-(void)authenticateLocalUser {
    NSLog(@"Authenticating local user ...");
    if(!_gameCenterAvailable) {
        return;
    }
    
    GKLocalPlayer *localPlayer = [GKLocalPlayer localPlayer];
    localPlayer.authenticateHandler = ^(UIViewController *viewController, NSError *error){
        if (viewController != nil)
        {
            NSLog(@"viewController != nil");
            _userAuthenticated = YES;
            _localUserId = [GKLocalPlayer localPlayer].playerID;
        }
        else
        {
            _userAuthenticated = NO;
        }
    };
}

- (void)setLastError:(NSError *)lastError {
    
    _lastError = [lastError copy];
    
    if (_lastError) {
        NSLog(@"GameKitHelper error: %@", [[_lastError userInfo] description]);
    }
}

- (UIViewController*)getRootViewController {
    
    return [UIApplication sharedApplication].keyWindow.rootViewController;
}

- (void)presentViewController:(UIViewController*)viewControllerToPresent {
    
    UIViewController *root = [self getRootViewController];
    
    [root presentViewController:viewControllerToPresent animated:YES completion:nil];
}

- (BOOL)isGameCenterAvailable {
    
    Class gcClass = NSClassFromString(@"GKLocalPlayer");
    NSString *RequiredSystemVersion = @"4.1";
    NSString *currentSystemVersion = [[UIDevice currentDevice] systemVersion];
    
    BOOL osVersionSupported =  [currentSystemVersion compare:RequiredSystemVersion options:NSNumericSearch] != NSOrderedAscending;
    
    return (gcClass && osVersionSupported);
}

- (void)findMatchWithMinPlayers:(NSUInteger)minPlayers maxPlayers:(NSUInteger)maxPlayers presentingViewController:(UIViewController *)viewController {
    
    if (!_gameCenterAvailable) {
        return;
    }
    
    _presentingViewController = viewController;
        
    GKMatchRequest *matchRequest = [[GKMatchRequest alloc] init];
    matchRequest.minPlayers = minPlayers;
    matchRequest.maxPlayers = maxPlayers;
    
    GKTurnBasedMatchmakerViewController *mmvc = [[GKTurnBasedMatchmakerViewController alloc] initWithMatchRequest:matchRequest];
    
    mmvc.turnBasedMatchmakerDelegate = self;
    mmvc.showExistingMatches = YES;
    
    [viewController presentViewController:mmvc animated:YES completion:nil];
}

- (void)showLeaderboardWithPresentingViewController:(UIViewController *)viewController
{
    _presentingViewController = viewController;
    
    GKGameCenterViewController *leaderboardController = [[GKGameCenterViewController alloc] init];
    if (leaderboardController != NULL)
    {
        leaderboardController.leaderboardIdentifier = @"wotr";
        leaderboardController.gameCenterDelegate = self;
        [_presentingViewController presentViewController:leaderboardController animated:YES completion:nil];
    }
}


@end
