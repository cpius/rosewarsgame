//
//  LeftPanel.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/24/13.
//
//

#import "LeftPanel.h"
#import "SoundManager.h"

@implementation LeftPanel

@synthesize delegate = _delegate;
@synthesize selectedAction = _selectedAction;

- (id)init {
    
    self = [super initWithFile:@"leftpanel.png"];
    
    if (self) {
        
        _attackButton = [CCSprite spriteWithFile:@"attackbutton.png"];
        _attackButton.position = ccp(self.contentSize.width / 2, self.contentSize.height - _attackButton.contentSize.height);
        
        _moveAttackButton = [CCSprite spriteWithFile:@"moveattackbutton.png"];
        _moveAttackButton.position = ccp(self.contentSize.width / 2, _attackButton.position.y - _moveAttackButton.contentSize.height - 10);
        
        _infoButton = [CCSprite spriteWithFile:@"infobutton.png"];
        _infoButton.position = ccp(self.contentSize.width / 2, _infoButton.contentSize.height);

        [self addChild:_attackButton];
        [self addChild:_moveAttackButton];
        [self addChild:_infoButton];
        
        [[CCDirector sharedDirector].touchDispatcher addTargetedDelegate:self priority:0 swallowsTouches:NO];
    }
    
    return self;
}

- (void)setSelectedAction:(Action *)selectedAction {
    
    _selectedAction = selectedAction;
    
    if (_selectedAction == nil || _selectedAction.cardInAction.isRanged) {
        [_attackButton runAction:[CCFadeOut actionWithDuration:0.2]];
        [_moveAttackButton runAction:[CCFadeOut actionWithDuration:0.2]];
    }
    else {
        [_attackButton runAction:[CCFadeIn actionWithDuration:0.2]];
        
        if (_selectedAction.cardInAction.movesRemaining > 0) {
            [_moveAttackButton runAction:[CCFadeIn actionWithDuration:0.2]];
        }
    }
}

- (BOOL)ccTouchBegan:(UITouch *)touch withEvent:(UIEvent *)event {
    
    if (CGRectContainsPoint(_attackButton.boundingBox, [self convertTouchToNodeSpace:touch])) {
        
        CCTexture2D* tex = [[CCTextureCache sharedTextureCache] addImage:@"attackbutton_selected.png"];
        [_attackButton setTexture:tex];
   //     [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
    }
    
    if (CGRectContainsPoint(_moveAttackButton.boundingBox, [self convertTouchToNodeSpace:touch])) {
        
        CCTexture2D* tex = [[CCTextureCache sharedTextureCache] addImage:@"moveattackbutton_selected.png"];
        [_moveAttackButton setTexture:tex];
   //     [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
    }
    
    if (CGRectContainsPoint(_infoButton.boundingBox, [self convertTouchToNodeSpace:touch])) {
        
        if (!_infoButtonSwitch) {
            CCTexture2D* tex = [[CCTextureCache sharedTextureCache] addImage:@"infobutton_selected.png"];
            [_infoButton setTexture:tex];
        }
        else {
            CCTexture2D* tex = [[CCTextureCache sharedTextureCache] addImage:@"infobutton.png"];
            [_infoButton setTexture:tex];
        }
        
        _infoButtonSwitch = !_infoButtonSwitch;
    //    [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
    }
    
    return YES;
}

- (void)ccTouchEnded:(UITouch *)touch withEvent:(UIEvent *)event {
    
    if (CGRectContainsPoint(_attackButton.boundingBox, [self convertTouchToNodeSpace:touch])) {
        if ([_delegate respondsToSelector:@selector(leftPanelAttackButtonPressed:)]) {
            [_delegate leftPanelAttackButtonPressed:self];
        }
    }
    
    if (CGRectContainsPoint(_moveAttackButton.boundingBox, [self convertTouchToNodeSpace:touch])) {        
        if ([_delegate respondsToSelector:@selector(leftPanelAttackAndConquerButtonPressed:)]) {
            [_delegate leftPanelAttackAndConquerButtonPressed:self];
        }
    }
    
    if (CGRectContainsPoint(_infoButton.boundingBox, [self convertTouchToNodeSpace:touch])) {
        
        if ([_delegate respondsToSelector:@selector(leftPanelInfoButtonPressed:)]) {
            [_delegate leftPanelInfoButtonPressed:self];
        }
    }
}

- (void)reset {
    
    [_attackButton setTexture:[[CCTextureCache sharedTextureCache] textureForKey:@"attackbutton.png"]];
    [_moveAttackButton setTexture:[[CCTextureCache sharedTextureCache] textureForKey:@"moveattackbutton.png"]];
    [_infoButton setTexture:[[CCTextureCache sharedTextureCache] textureForKey:@"infobutton.png"]];
}

@end
