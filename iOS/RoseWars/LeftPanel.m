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
        
        _attackButton = [HKImageButton imageButtonWithImage:@"attackbutton.png" selectedImage:@"attackbutton_selected.png" block:^(id sender) {
            if ([_delegate respondsToSelector:@selector(leftPanelAttackButtonPressed:)]) {
                [_delegate leftPanelAttackButtonPressed:self];
            }
        }];
        
        _attackButton.position = CGPointMake(0, (self.size.height / 2) - _attackButton.size.height);
        
        _moveAttackButton = [HKImageButton imageButtonWithImage:@"moveattackbutton.png" selectedImage:@"moveattackbutton_selected.png" block:^(id sender) {
            if ([_delegate respondsToSelector:@selector(leftPanelAttackAndConquerButtonPressed:)]) {
                [_delegate leftPanelAttackAndConquerButtonPressed:self];
            }
        }];
        
        _moveAttackButton.position = CGPointMake(0, _attackButton.position.y - _moveAttackButton.size.height - 10);
        
        _infoButton = [HKImageButton imageButtonWithImage:@"infobutton.png" selectedImage:@"infobutton_selected.png" block:^(id sender) {
            _infoButtonSwitch = !_infoButtonSwitch;
            if ([_delegate respondsToSelector:@selector(leftPanelInfoButtonPressed:)]) {
                [_delegate leftPanelInfoButtonPressed:self];
            }
        }];

        _infoButton.position = CGPointMake(0, _moveAttackButton.position.y - _infoButton.size.height - 10);

        [self addChild:_attackButton];
        [self addChild:_moveAttackButton];
        [self addChild:_infoButton];
    }
    
    return self;
}

- (void)setSelectedAction:(Action *)selectedAction {
    
    _selectedAction = selectedAction;
    
    if (_selectedAction == nil || _selectedAction.cardInAction.isRanged) {
        _attackButton.alpha = 0.0;
        _moveAttackButton.alpha = 0.0;
    }
    else {
        [_attackButton runAction:[SKAction fadeInWithDuration:0.2]];
        
        if (_selectedAction.actionType == kActionTypeMelee) {
            
            MeleeAttackAction *meleeAction = (MeleeAttackAction*)_selectedAction;
            
            if (meleeAction.meleeAttackType == kMeleeAttackTypeConquer) {
                [_moveAttackButton runAction:[SKAction fadeInWithDuration:0.2]];
            }
        }
    }
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    
    NSLog(@"began");
}

- (void)reset {

    _attackButton.selected = NO;
    _moveAttackButton.selected = NO;
    _infoButton.selected = NO;
}

@end
