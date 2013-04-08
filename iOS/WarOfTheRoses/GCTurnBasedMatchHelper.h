//
//  GCTurnBasedMatchHelper.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/18/12.
//
//

#import <Foundation/Foundation.h>
#import <GameKit/GameKit.h>
#import "Definitions.h"

#define kLeaderBoardCategory @"wotr"

@protocol GCTurnBasedMatchHelperDelegate <NSObject>

@optional
- (void)enterNewGame:(GKTurnBasedMatch*)match;
- (void)layoutMatch:(GKTurnBasedMatch*)match;
- (void)takeTurn:(GKTurnBasedMatch*)match;
- (void)recieveEndGame:(GKTurnBasedMatch*)match;
- (void)sendNotice:(NSString*)notice forMatch:(GKTurnBasedMatch*)match;

@end

@interface GCTurnBasedMatchHelper : NSObject <GKTurnBasedMatchmakerViewControllerDelegate, GKTurnBasedEventHandlerDelegate,GKLeaderboardViewControllerDelegate> {
    
    BOOL _userAuthenticated;
    UIViewController *_presentingViewController;
}

@property (nonatomic, weak) id<GCTurnBasedMatchHelperDelegate> delegate;
@property (nonatomic, readonly) BOOL gameCenterAvailable;
@property (nonatomic, readonly) NSError *lastError;

@property (nonatomic, readonly) GKTurnBasedMatch *currentMatch;
@property (nonatomic, readonly) NSString *localUserId;

+ (GCTurnBasedMatchHelper*)sharedInstance;

- (void)authenticateLocalUser;
- (void)findMatchWithMinPlayers:(NSUInteger)minPlayers maxPlayers:(NSUInteger)maxPlayers presentingViewController:(UIViewController*) viewController;

- (void)endTurnWithData:(NSData*)data;
- (void)endMatchWithData:(NSData*)data gameResult:(GameResults)gameResult;

- (void)submitScoreForPlayer:(GKTurnBasedParticipant*)player;
- (void)showLeaderboardWithPresentingViewController:(UIViewController *)viewController;

@end
