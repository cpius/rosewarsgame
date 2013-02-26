//
//  LeftPanel.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/24/13.
//
//

#import "CCSprite.h"
#import "Card.h"

@class LeftPanel;
@protocol LeftPanelProtocol <NSObject>

@optional
- (void)leftPanelAttackButtonPressed:(LeftPanel*)leftPanel;
- (void)leftPanelAttackAndConquerButtonPressed:(LeftPanel*)leftPanel;
- (void)leftPanelInfoButtonPressed:(LeftPanel*)leftPanel;

@end

@interface LeftPanel : CCSprite <CCTargetedTouchDelegate> {
    
    CCSprite *_attackButton;
    CCSprite *_moveAttackButton;
    CCSprite *_infoButton;
    
    BOOL _infoButtonSwitch;
}

@property (nonatomic, weak) id<LeftPanelProtocol> delegate;
@property (nonatomic, strong) Card *selectedCard;

- (void)reset;

@end
