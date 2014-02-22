//
//  LeftPanel.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/24/13.
//
//

#import "LeftPanel.h"
#import "MeleeAttackAction.h"
#import "Action.h"
#import "HKImageButton.h"

@implementation LeftPanel

@synthesize delegate = _delegate;
@synthesize selectedAction = _selectedAction;

- (id)init {
    
    self = [super initWithImageNamed:@"leftpanel.png"];
    
    if (self) {
        
        self.userInteractionEnabled = YES;
        
        _infoButton = [HKImageButton imageButtonWithImage:@"infobutton.png" selectedImage:@"infobutton_selected.png" block:^(id sender) {
            _infoButtonSwitch = !_infoButtonSwitch;
            if ([_delegate respondsToSelector:@selector(leftPanelInfoButtonPressed:)]) {
                [_delegate leftPanelInfoButtonPressed:self];
            }
        }];

        _infoButton.position = CGPointMake(0, (-self.size.height / 2) + (_infoButton.size.height / 2) + 10);

        [self addChild:_infoButton];
    }
    
    return self;
}

- (void)setSelectedAction:(Action *)selectedAction {
    
    _selectedAction = selectedAction;
    
}



- (void)reset {

    _infoButton.selected = NO;
}

@end
