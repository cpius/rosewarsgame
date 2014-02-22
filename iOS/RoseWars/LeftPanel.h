//
//  LeftPanel.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/24/13.
//
//

#import <SpriteKit/SpriteKit.h>

@class LeftPanel;
@class Action;
@class HKImageButton;
@protocol LeftPanelProtocol <NSObject>

@optional
- (void)leftPanelAttackButtonPressed:(LeftPanel*)leftPanel;
- (void)leftPanelAttackAndConquerButtonPressed:(LeftPanel*)leftPanel;
- (void)leftPanelInfoButtonPressed:(LeftPanel*)leftPanel;

@end

@interface LeftPanel : SKSpriteNode {
    
    HKImageButton *_infoButton;
    
    BOOL _infoButtonSwitch;
}

@property (nonatomic, weak) id<LeftPanelProtocol> delegate;
@property (nonatomic, strong) Action *selectedAction;

- (void)reset;

@end
