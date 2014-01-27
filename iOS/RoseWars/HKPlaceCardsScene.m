//
//  HKPlaceCardsScene.m
//  RoseWars
//
//  Created by Heine Skov Kristensen on 9/27/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import "HKPlaceCardsScene.h"
#import "HKImageButton.h"
#import "GCTurnBasedMatchHelper.h"
#import "HKGameScene.h"

static NSString* const nextArrowTag = @"NEXT_ARROW_TAG";

@implementation HKPlaceCardsScene

- (void)didMoveToView:(SKView *)view {
    
    CGSize screenSize = self.size;
    
    SKSpriteNode *background = [SKSpriteNode spriteNodeWithImageNamed:@"woddenbackground2.png"];
    background.anchorPoint = CGPointMake(0.0f, 0.0f);
    background.size = screenSize;
    [background setZPosition:-1];
    [self addChild:background];
    
    _gameboard = [[GameBoard alloc] init];
    
    _gameboard.size = CGSizeMake(320, 375);
    _gameboard.rows = 4;
    _gameboard.columns = 5;
    _gameboard.colorOfBottomPlayer = [GameManager sharedManager].currentGame.myColor;
    _gameboard.colorOfTopPlayer = [GameManager sharedManager].currentGame.myColor;
    _gameboard.scale = 0.8;
    
    _gameboard.position = CGPointMake((self.size.width - _gameboard.size.width) / 2, self.size.height - _gameboard.size.height + 45);
    [self addChild:_gameboard];
    
    [_gameboard layoutBoard];
    
    _gridLayoutManager = [[GridlLayoutManager alloc] init];
    
    _gridLayoutManager.numberOfRows = 2;
    _gridLayoutManager.numberOfColumns = 5;
    _gridLayoutManager.gridSize = CGSizeMake(screenSize.width, 140);
    _gridLayoutManager.rowPadding = -5;
    _gridLayoutManager.columnPadding = 2;
    _gridLayoutManager.yOffset = 185;
    _gridLayoutManager.xOffset = 30;
    
    CardSprite *tempSprite = [[CardSprite alloc] initWithCard:[[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0]];
    
    _gridLayoutManager.columnWidth = tempSprite.calculateAccumulatedFrame.size.width * 0.45;
    _gridLayoutManager.rowHeight = tempSprite.calculateAccumulatedFrame.size.height * 0.45;
    
    HKImageButton *autoButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Auto" block:^(id sender) {
        [self autoPressed:sender];
    }];
    
    autoButton.position = CGPointMake(screenSize.width - (autoButton.size.width / 2) - 10, (autoButton.size.height / 2) + 10);
    
    [self addChild:autoButton];

    _placedCards = [[NSMutableArray alloc] init];
    _homePositions = [[NSMutableDictionary alloc] init];
    
    [self presentCards];
}

- (void)autoPressed:(id)sender {
    
    SKNode *button = sender;
    [button removeFromParent];
    
    [[GameManager sharedManager].deckStrategy placeCardsInDeck:[GameManager sharedManager].currentGame.myDeck inGameBoardSide:kGameBoardLower];
    
    for (CardSprite *card in _cardSprites) {
        
        GridLocation *boardLocation = [[GridLocation gridLocationWithRow:card.model.cardLocation.row column:card.model.cardLocation.column] flipBacklineFromCurrentBackline:LOWER_BACKLINE];
        
        GameBoardNode *node = [_gameboard getGameBoardNodeForGridLocation:boardLocation];
        
        [self placeCard:card inGameBoardNode:node];
    }
}


- (void)presentCards {
    
    CGSize screenSize = self.size;
    
    self.userInteractionEnabled = YES;
    
    NSInteger row = 1, column = 1;
    float cardCounter = 1;
    
    _cardSprites = [[NSMutableArray alloc] initWithCapacity:[GameManager sharedManager].currentGame.myDeck.cards.count];
    
    for (Card *card in [GameManager sharedManager].currentGame.myDeck.cards) {
        
        CardSprite *cardSprite = [[CardSprite alloc] initWithCard:card];
        
        [cardSprite setScale:0.40];
        cardSprite.position = [_gridLayoutManager getPositionForRowNumber:row columnNumber:column];
        cardSprite.model.cardLocation = [GridLocation gridLocationWithRow:row column:column];
        
        [_homePositions setObject:cardSprite.model.cardLocation forKey:card.cardIdentifier];
        
        [self addChild:cardSprite];
        [_cardSprites addObject:cardSprite];
        
//        CGPoint cardPosition = [_gridLayoutManager getPositionForRowNumber:row columnNumber:column];
        
//        SKAction *scale = [SKAction scaleTo:0.45 duration:0.1 * cardCounter];
/*        SKAction *moveTo = [SKAction moveTo:cardPosition duration:0.1 * cardCounter];
        moveTo.timingMode = SKActionTimingEaseIn;
        [cardSprite runAction:[SKAction group:@[moveTo]]];
  */              
        cardCounter++;
        column++;
        
        if (column > _gridLayoutManager.numberOfColumns) {
            column = 1;
            row++;
        }
    }
}

- (void)selectSpriteForTouch:(CGPoint)touchLocation {
    
    SKNode* card = [self nodeAtPoint:touchLocation];
    
    if ([card isKindOfClass:[CardSprite class]]) {
        GameBoardNode *gameboardNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertPoint:touchLocation toNode:_gameboard]];
        
        if (gameboardNode != nil) {
            gameboardNode.card = nil;
        }
        
        if (card != _selectedCard) {
            [_selectedCard removeAllActions];
            _selectedCard = (CardSprite*)card;
            [_selectedCard setZPosition:100];
            [_selectedCard runAction:[SKAction scaleTo:0.8 duration:0.2]];
        }
        else {
            _selectedCard = nil;
        }
    }
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    
    UITouch *touch = touches.anyObject;
    CGPoint touchLocation = [touch locationInNode:self];

    [self selectSpriteForTouch:touchLocation];
}


- (void)panForTranslation:(CGPoint)translation {
    if (_selectedCard) {
        CGPoint newPos = CGPointAdd(_selectedCard.position, translation);
        _selectedCard.position = newPos;
    }
}

- (void)touchesMoved:(NSSet *)touches withEvent:(UIEvent *)event {
    
    if (_selectedCard == nil) {
        return;
    }
    
    UITouch *touch = touches.anyObject;
    
    CGPoint touchLocation = [touch locationInNode:self];
    CGPoint oldTouchLocation = [touch previousLocationInNode:self];
    
    CGPoint translation = CGPointSubtract(touchLocation, oldTouchLocation);
    [self panForTranslation:translation];

    GameBoardNode *gameboardNode = [_gameboard getGameBoardNodeForPosition:[self convertPoint:touchLocation toNode:_gameboard]];
    
    if (gameboardNode != nil) {
        if (gameboardNode != _hoveringOverGameBoardNode && !gameboardNode.hasCard) {
            
            SKAction *scaleUpAction = [SKAction scaleTo:1.1 duration:0.2];
            [gameboardNode runAction:scaleUpAction];
            
            if (_hoveringOverGameBoardNode != nil) {
                [_hoveringOverGameBoardNode runAction:[SKAction scaleTo:1.0 duration:0.2]];
            }
            
            _hoveringOverGameBoardNode = gameboardNode;
        }
    }
    else {
        if (_hoveringOverGameBoardNode != nil) {
            [_hoveringOverGameBoardNode runAction:[SKAction scaleTo:1.0 duration:0.2]];
        }
    }
    
    _isMovingCard = YES;
}

- (void)placeCard:(CardSprite*)card inGameBoardNode:(GameBoardNode *)node {
    
    [_gameboard placeCard:card withCardScale:0.4 inGameBoardNode:node useHighLighting:YES onCompletion:^{
        
        // TODO: Only laying out cards for the lower part of board
        card.model.cardLocation = [GridLocation gridLocationWithRow:card.model.cardLocation.row + 4
                                                             column:card.model.cardLocation.column];
        
        [self runAction:[SKAction playSoundFileNamed:@"pageflip.mp3" waitForCompletion:NO]];
        
        if (![_placedCards containsObject:card]) {
            [_placedCards addObject:card];
        }
        
        if (_placedCards.count == [GameManager sharedManager].currentGame.myDeck.cards.count) {
            [self finishedPlacingCards];
        }
        
        [card setZPosition:0];
        
        _selectedCard = nil;
        _isMovingCard = NO;
    }];
}

- (void)touchesEnded:(NSSet *)touches withEvent:(UIEvent *)event {
    
    if (_selectedCard == nil) {
        return;
    }
    
    UITouch *touch = touches.anyObject;
    CGPoint touchLocation = [touch locationInNode:self];
    GameBoardNode *gameboardNode = [_gameboard getGameBoardNodeForPosition:[self convertPoint:touchLocation toNode:_gameboard]];
    
    if (_detailCard == nil) {
        if (gameboardNode != nil && !gameboardNode.hasCard && _selectedCard != nil) {
            
            [self placeCard:_selectedCard inGameBoardNode:gameboardNode];
            return;
        }
        else {
            
            if (_isMovingCard) {
                
                if ([_placedCards containsObject:_selectedCard]) {
                    [_placedCards removeObject:_selectedCard];
                }
                
                SKNode *nextArrow = [self childNodeWithName:nextArrowTag];
                
                if (nextArrow != nil) {
                    [nextArrow removeFromParent];
                }
                
                [self moveCardToHomePosition:_selectedCard];
                _isMovingCard = NO;
                _selectedCard = nil;
                
                return;
            }
        }
    }
    
    for (CardSprite *cardSprite in _cardSprites) {
        
		if(CGRectContainsPoint(cardSprite.frame, touchLocation)) {
            
            [self toggleDetailForCard:cardSprite];
            
			return;
		}
	}
}

- (void)finishedPlacingCards {
    
    if (![self childNodeWithName:nextArrowTag]) {
        CGSize screenSize = self.size;
        
        HKImageButton *nextArrow = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Battle" block:^(id sender) {
            [self nextScenePressed];
        }];
        
        nextArrow.position = CGPointMake(screenSize.width - (nextArrow.size.width / 2) - 10, (nextArrow.size.height / 2) + 10);
        nextArrow.name = nextArrowTag;
        
        [self addChild:nextArrow];
        
        SKAction *scaleup = [SKAction scaleTo:1.5 duration:0.2];
        SKAction *scaledown = [SKAction scaleTo:1.0 duration:0.2];
        SKAction *highlight = [SKAction runBlock:^{
//            [ParticleHelper highlightNode:nextArrow forever:NO];
        }];
        
        [nextArrow runAction:[SKAction sequence:@[scaleup, scaledown, highlight]]];
    }
}

- (void)nextScenePressed {
    
    [self runAction:[SKAction playSoundFileNamed:@"buttonclick.wav" waitForCompletion:NO]];
    [self runAction:[SKAction playSoundFileNamed:@"fanfare.mp3" waitForCompletion:NO]];
    
    if ([GameManager sharedManager].currentGame.gametype == kGameTypeMultiPlayer) {
        
        // If the player who initiated the game already has placed his cards, set the game as started
        if ([GameManager sharedManager].currentGame.state == kGameStateFinishedPlacingCards) {
            [GameManager sharedManager].currentGame.state = kGameStateGameStarted;
        }
        else {
            [GameManager sharedManager].currentGame.state = kGameStateFinishedPlacingCards;
        }
        
        // If game is started and it's my turn
        if ([GameManager sharedManager].currentGame.state == kGameStateGameStarted &&
            [GameManager sharedManager].currentPlayersTurn == [GameManager sharedManager].currentGame.myColor) {
            
            NSLog(@"Take my first turn");
        }
        else {
            
            [[GCTurnBasedMatchHelper sharedInstance] endTurnWithData:[[GameManager sharedManager].currentGame serializeCurrentGameForPlayerWithId:[GKLocalPlayer localPlayer].playerID]];
        }
    }
    else {
        [GameManager sharedManager].currentGame.state = kGameStateGameStarted;
    }
    
    HKGameScene *scene = [HKGameScene sceneWithSize:self.size];
    scene.scaleMode = SKSceneScaleModeAspectFill;
    [self.view presentScene:scene transition:[SKTransition crossFadeWithDuration:0.2]];
}

- (void)moveCardToHomePosition:(CardSprite *)card {
    
    GridLocation *homeLocationForCard = [_homePositions objectForKey:card.model.cardIdentifier];
    
    CGPoint position = [_gridLayoutManager getPositionForRowNumber:homeLocationForCard.row columnNumber:homeLocationForCard.column];
    
    NSLog(@"Card %@ moving to home position %@", card, NSStringFromCGPoint(position));
    
    SKAction *moveAction = [SKAction moveTo:position duration:0.2];
    SKAction *scaleAction = [SKAction scaleTo:0.45 duration:0.2];

    [card runAction:[SKAction group:@[moveAction, scaleAction]]];
}


- (void)toggleDetailForCard:(CardSprite *)card {
    
    CGSize screenSize = self.size;
    
 /*   CCCallFunc *sound = [CCCallFunc actionWithTarget:self selector:@selector(playSwooshSound)];
    
    if (card.model.isShowingDetail) {
        
        CGPoint location = [_gridLayoutManager getPositionForRowNumber:card.model.cardLocation.row columnNumber:card.model.cardLocation.column];
        
        CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.5 position:location];
        CCSpawn *spawn = [CCSpawn actions: moveTo, sound, nil];
        [card runAction:spawn];
        
        _detailCard = nil;
    }
    else {
        CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.5 position:CGPointMake(screenSize.width / 2, screenSize.height / 2)];
        CCSpawn *spawn = [CCSpawn actions: moveTo, sound, nil];
        [card runAction:spawn];
        
        _detailCard = card;
    }
    
    [card toggleDetailWithScale:0.4];*/
}

- (void)playSwooshSound {
    
 //   [self runAction:[SKAction playSoundFileNamed:@"" waitForCompletion:<#(BOOL)#>]]
 //   [[SimpleAudioEngine sharedEngine] playEffect:SWOOSH_SOUND];
}


@end
