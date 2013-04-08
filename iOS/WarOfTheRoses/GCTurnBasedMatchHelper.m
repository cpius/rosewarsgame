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
            [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(authenticationChanged) name:GKPlayerAuthenticationDidChangeNotificationName object:nil];
        }
    }
    
    return self;
}

- (void)handleInviteFromGameCenter:(NSArray *)playersToInvite {
    
    CCLOG(@"New invite from players: %@", playersToInvite);
    
    [_presentingViewController dismissModalViewControllerAnimated:YES];
    
    GKMatchRequest *request = [[GKMatchRequest alloc] init];
    
    request.playersToInvite = playersToInvite;
    request.minPlayers = 2;
    request.maxPlayers = 2;
    
    GKTurnBasedMatchmakerViewController *viewController = [[GKTurnBasedMatchmakerViewController alloc] initWithMatchRequest:request];
    
    viewController.showExistingMatches = NO;
    viewController.turnBasedMatchmakerDelegate = self;
    
    [_presentingViewController presentModalViewController:viewController animated:YES];
}

- (void)handleTurnEventForMatch:(GKTurnBasedMatch *)match {
    
    CCLOG(@"Turn has happened in match: %@", match);
    
    if ([match.matchID isEqualToString:_currentMatch.matchID]) {
        if ([match.currentParticipant.playerID isEqualToString:[GKLocalPlayer localPlayer].playerID]) {
            
            // It's the current match, and it's our turn now
            _currentMatch = match;
            [_delegate takeTurn:match];
        }
    }
    else {
        if ([match.currentParticipant.playerID isEqualToString:[GKLocalPlayer localPlayer].playerID]) {
            
            // It's not the current match and it's our turn now
            [_delegate sendNotice:@"It's your turn for another match" forMatch:match];
        }
        else {
            // It's not the current match, and it's someone else's turn
        }
    }
}

- (void)handleMatchEnded:(GKTurnBasedMatch *)match {
    
    CCLOG(@"Game has ended: %@", match);
}

- (void)turnBasedMatchmakerViewController:(GKTurnBasedMatchmakerViewController *)viewController didFailWithError:(NSError *)error {
    
    [viewController dismissModalViewControllerAnimated:YES];
    
    CCLOG(@"Error finding match: %@", error.localizedDescription);
}

- (void)turnBasedMatchmakerViewController:(GKTurnBasedMatchmakerViewController *)viewController didFindMatch:(GKTurnBasedMatch *)match {
    
    [viewController dismissModalViewControllerAnimated:YES];
    
    CCLOG(@"Did find match: %@", match);
    
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
    
    [_currentMatch endTurnWithNextParticipant:nextParticipant
                                    matchData:data completionHandler:^(NSError *error) {
                                        
                                        if (error) {
                                            NSLog(@"%@", error);
                                        }
                                    }];
}

- (void)submitScoreForPlayer:(GKTurnBasedParticipant*)player {
    
    GKScore *scoreReporter = [[GKScore alloc] initWithCategory:kLeaderBoardCategory];
    
    scoreReporter.value = 1;
    
    [scoreReporter reportScoreWithCompletionHandler:^(NSError *error) {
        
        CCLOG(@"Error reporting score");
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
    
    CCLOG(@"Player: %@ quit for match: %@", match.currentParticipant, match);
    
    [match participantQuitInTurnWithOutcome:GKTurnBasedMatchOutcomeQuit nextParticipant:participant matchData:match.matchData completionHandler:nil];
}

- (void)turnBasedMatchmakerViewControllerWasCancelled:(GKTurnBasedMatchmakerViewController *)viewController {
    
    [viewController dismissModalViewControllerAnimated:YES];
    
    CCLOG(@"Has cancelled");
}

- (void)authenticationChanged {
    
    if ([GKLocalPlayer localPlayer].isAuthenticated && !_userAuthenticated) {
        NSLog(@"Authentication changed - user authenticared");
        _userAuthenticated = YES;
        
        _localUserId = [GKLocalPlayer localPlayer].playerID;
    }
    else if (![GKLocalPlayer localPlayer].isAuthenticated && _userAuthenticated) {
        NSLog(@"Authentication changed - user not authenticated");
        _userAuthenticated = NO;
    }
}

- (void)authenticateLocalUser {
    
    if (!_gameCenterAvailable) {
        return;
    }
        
    NSLog(@"Authenticating local user...");
    
    if (![GKLocalPlayer localPlayer].authenticated) {
        [[GKLocalPlayer localPlayer] authenticateWithCompletionHandler:^(NSError *error) {
            
            [GKTurnBasedEventHandler sharedTurnBasedEventHandler].delegate = self;
        }];
    }
    else {
        NSLog(@"Already authenticated");
        [GKTurnBasedEventHandler sharedTurnBasedEventHandler].delegate = nil;
    }
}

- (void)setLastError:(NSError *)lastError {
    
    _lastError = [lastError copy];
    
    if (_lastError) {
        CCLOG(@"GameKitHelper error: %@", [[_lastError userInfo] description]);
    }
}

- (UIViewController*)getRootViewController {
    
    return [UIApplication sharedApplication].keyWindow.rootViewController;
}

- (void)presentViewController:(UIViewController*)viewControllerToPresent {
    
    UIViewController *root = [self getRootViewController];
    
    [root presentModalViewController:viewControllerToPresent animated:YES];
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
    
    [viewController presentModalViewController:mmvc animated:YES];
}

- (void)showLeaderboardWithPresentingViewController:(UIViewController *)viewController
{
    _presentingViewController = viewController;
    
    GKLeaderboardViewController *leaderboardController = [[GKLeaderboardViewController alloc] init];
    if (leaderboardController != NULL)
    {
        leaderboardController.category = @"wotr";
        leaderboardController.timeScope = GKLeaderboardTimeScopeWeek;
        leaderboardController.leaderboardDelegate = self;
        [_presentingViewController presentModalViewController: leaderboardController animated: YES];
    }
}
- (void)leaderboardViewControllerDidFinish:(GKLeaderboardViewController *)viewController
{
    [_presentingViewController dismissModalViewControllerAnimated: YES];
}

@end
