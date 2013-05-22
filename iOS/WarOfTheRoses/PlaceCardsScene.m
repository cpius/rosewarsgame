//
//  PlaceCardsScene.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/17/12.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
//

#import "PlaceCardsScene.h"
#import "GCTurnBasedMatchHelper.h"
#import "GameManager.h"
#import "GameScene.h"
#import "ParticleHelper.h"
#import "MinimumRequirementDeckStrategy.h"

@interface PlaceCardsScene()

- (void)toggleDetailForCard:(CardSprite*)card;
- (void)moveCardToHomePosition:(CardSprite*)card;
- (void)placeCard:(CardSprite*)card inGameBoardNode:(GameBoardNode *)node;

@end

@implementation PlaceCardsScene

@synthesize currentDeck = _currentDeck;

+ (id)scene {
    
    CCScene *scene = [CCScene node];
    
    PlaceCardsScene *layer = [[PlaceCardsScene alloc] init];

    [scene addChild:layer];
    
    return scene;
}

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        CGSize screenSize = [CCDirector sharedDirector].winSize;
        
        CCSprite *background = [CCSprite spriteWithFile:@"woddenbackground2.png"];
        background.anchorPoint = ccp(0, 0);
        [self addChild:background z:-1];

        _gameboard = [[GameBoard alloc] init];

        _gameboard.contentSize = CGSizeMake(320, 375);
        _gameboard.rows = 4;
        _gameboard.columns = 5;
        _gameboard.anchorPoint = ccp(0.5, 0.5);
        _gameboard.colorOfBottomPlayer = kPlayerGreen;
        _gameboard.colorOfTopPlayer = kPlayerGreen;
        _gameboard.scale = 0.9;
        
        _gameboard.position = ccp(screenSize.width / 2, (screenSize.height / 2) + 60);
        [self addChild:_gameboard];
        
        [_gameboard layoutBoard];
        
        _gridLayoutManager = [[GridlLayoutManager alloc] init];
        
        _gridLayoutManager.numberOfRows = 2;
        _gridLayoutManager.numberOfColumns = 5;
        _gridLayoutManager.gridSize = CGSizeMake(screenSize.width, 140);
        _gridLayoutManager.rowPadding = 0;
        _gridLayoutManager.columnPadding = 2;
        _gridLayoutManager.yOffset = 150;
        _gridLayoutManager.xOffset = 17;
        
        CardSprite *tempSprite = [[CardSprite alloc] initWithCard:[[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0]];
        
        _gridLayoutManager.columnWidth = tempSprite.contentSize.width * 0.45;
        _gridLayoutManager.rowHeight = tempSprite.contentSize.height * 0.45;
        
        CCMenuItem *autoButton = [CCMenuItemImage itemWithNormalImage:@"autobutton.png" selectedImage:@"autobutton.png" target:self selector:@selector(autoPressed:)];
        
        autoButton.anchorPoint = ccp(1, 0);
        autoButton.position = ccp(screenSize.width - 10, 10);
        
        CCMenu *menu = [CCMenu menuWithItems:autoButton, nil];
        menu.position = CGPointZero;
        menu.tag = AUTO_TAG;
        
        [self addChild:menu];
        
        _placedCards = [[NSMutableArray alloc] init];
        _homePositions = [[NSMutableDictionary alloc] init];
        
        [self presentCards];
        
        [[CCDirector sharedDirector].touchDispatcher addTargetedDelegate:self priority:0 swallowsTouches:YES];
    }
    
    return self;
}

- (void)presentCards {
    
    CGSize screenSize = [CCDirector sharedDirector].winSize;
    
    self.isTouchEnabled = YES;
        
    NSInteger row = 1, column = 1;
    float cardCounter = 1;
    
    _cardSprites = [[NSMutableArray alloc] initWithCapacity:[GameManager sharedManager].currentGame.myDeck.cards.count];
    
    for (Card *card in [GameManager sharedManager].currentGame.myDeck.cards) {
        
        CardSprite *cardSprite = [[CardSprite alloc] initWithCard:card];
        
        cardSprite.position = ccp(screenSize.width / 2, -200);
        cardSprite.model.cardLocation = [GridLocation gridLocationWithRow:row column:column];
        
        [_homePositions setObject:cardSprite.model.cardLocation forKey:card.cardIdentifier];
        
        [self addChild:cardSprite];
        [_cardSprites addObject:cardSprite];
        
        CGPoint cardPosition = [_gridLayoutManager getPositionForRowNumber:row columnNumber:column];
        
        CCScaleTo *scale = [CCScaleTo actionWithDuration:0.1 * cardCounter scale:0.45];
        CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.1 * cardCounter position:cardPosition];
        CCEaseIn *ease = [CCEaseIn actionWithAction:moveTo rate:2.0];
        CCSpawn *spawn = [CCSpawn actions:scale, ease, nil];
        [cardSprite runAction:spawn];
        
        cardCounter++;
        column++;
        
        if (column > _gridLayoutManager.numberOfColumns) {
            column = 1;
            row++;
        }
    }
}

- (void)autoPressed:(id)sender {
    
    CCMenuItem *menu = sender;
    [menu removeFromParentAndCleanup:YES];
    
    [[GameManager sharedManager].deckStrategy placeCardsInDeck:[GameManager sharedManager].currentGame.myDeck inGameBoardSide:kGameBoardLower];
    
    for (CardSprite *card in _cardSprites) {
        
        GridLocation *boardLocation = [[GridLocation gridLocationWithRow:card.model.cardLocation.row column:card.model.cardLocation.column] flipBacklineFromCurrentBackline:LOWER_BACKLINE];
        
        GameBoardNode *node = [_gameboard getGameBoardNodeForGridLocation:boardLocation];
        
        [self placeCard:card inGameBoardNode:node];
    }
}

- (void)selectSpriteForTouch:(CGPoint)touchLocation {
    CardSprite * newCard = nil;
    for (CardSprite *cardSprite in _cardSprites) {
        if (CGRectContainsPoint(cardSprite.boundingBox, touchLocation)) {
            newCard = cardSprite;
            break;
        }
    }
    
    GameBoardNode *gameboardNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertToNodeSpace:touchLocation]];
    
    if (gameboardNode != nil) {
        gameboardNode.card = nil;
    }

    if (newCard != _selectedCard) {
        [_selectedCard stopAllActions];
        _selectedCard = newCard;
        [_selectedCard setZOrder:100];
        [_selectedCard runAction:[CCScaleTo actionWithDuration:0.2 scale:0.8]];
    }
}

- (BOOL)ccTouchBegan:(UITouch *)touch withEvent:(UIEvent *)event {
    CGPoint touchLocation = [self convertTouchToNodeSpace:touch];
    [self selectSpriteForTouch:touchLocation];
    return TRUE;
}


- (void)panForTranslation:(CGPoint)translation {
    if (_selectedCard) {
        CGPoint newPos = ccpAdd(_selectedCard.position, translation);
        _selectedCard.position = newPos;
    } 
}

- (void)ccTouchMoved:(UITouch *)touch withEvent:(UIEvent *)event {
    CGPoint touchLocation = [self convertTouchToNodeSpace:touch];
    
    CGPoint oldTouchLocation = [touch previousLocationInView:touch.view];
    oldTouchLocation = [[CCDirector sharedDirector] convertToGL:oldTouchLocation];
    oldTouchLocation = [self convertToNodeSpace:oldTouchLocation];
    
    CGPoint translation = ccpSub(touchLocation, oldTouchLocation);
    [self panForTranslation:translation];
    
    GameBoardNode *gameboardNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertTouchToNodeSpace:touch]];
    
    if (gameboardNode != nil) {
        if (gameboardNode != _hoveringOverGameBoardNode && !gameboardNode.hasCard) {
                        
            CCScaleTo *scaleUpAction = [CCScaleTo actionWithDuration:0.2 scale:1.1];
            [gameboardNode runAction:scaleUpAction];
            
            if (_hoveringOverGameBoardNode != nil) {
                CCScaleTo *scaleDownAction = [CCScaleTo actionWithDuration:0.2 scale:1.0];
                [_hoveringOverGameBoardNode runAction:scaleDownAction];
            }
            
            _hoveringOverGameBoardNode = gameboardNode;
        }
    }
    else {
        if (_hoveringOverGameBoardNode != nil) {
            CCScaleTo *scaleDownAction = [CCScaleTo actionWithDuration:0.2 scale:1.0];
            [_hoveringOverGameBoardNode runAction:scaleDownAction];
        }
    }
    
    _isMovingCard = YES;
}

- (void)placeCard:(CardSprite*)card inGameBoardNode:(GameBoardNode *)node {
    
    [_gameboard placeCard:card inGameBoardNode:node useHighLighting:YES onCompletion:^{
        
        // TODO: Only laying out cards for the lower part of board
        card.model.cardLocation = [GridLocation gridLocationWithRow:card.model.cardLocation.row + 4
                                                             column:card.model.cardLocation.column];
        
        [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventCardDropped];
        
        if (![_placedCards containsObject:card]) {
            [_placedCards addObject:card];
        }
        
        if (_placedCards.count == [GameManager sharedManager].currentGame.myDeck.cards.count) {
            [self finishedPlacingCards];
        }
        
        [card setZOrder:0];
        
        _selectedCard = nil;
        _isMovingCard = NO;
    }];
}

- (void)ccTouchEnded:(UITouch *)touch withEvent:(UIEvent *)event {
    
    CGPoint location = [touch locationInView:touch.view];
    CGPoint convLoc = [[CCDirector sharedDirector] convertToGL:location];
    
    GameBoardNode *gameboardNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertTouchToNodeSpace:touch]];
    
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
                
                CCNode *nextArrow = [self getChildByTag:NEXT_ARROW_TAG];
                
                if (nextArrow != nil) {
                    [nextArrow removeFromParentAndCleanup:YES];
                }
                
                [self moveCardToHomePosition:_selectedCard];
                _isMovingCard = NO;
                _selectedCard = nil;
                
                return;
            }
        }
    }

    for (CardSprite *cardSprite in _cardSprites) {
        
		if(CGRectContainsPoint(cardSprite.boundingBox, convLoc)) {
            
            [self toggleDetailForCard:cardSprite];
            
			return;
		}
	}
}

- (void)finishedPlacingCards {
    
    if (![self getChildByTag:NEXT_ARROW_TAG]) {
        CGSize screenSize = [CCDirector sharedDirector].winSize;
        
        CCMenuItem *nextArrow = [CCMenuItemImage itemWithNormalImage:@"battle.png" selectedImage:@"battle.png" target:self selector:@selector(nextScenePressed:)];
        
        nextArrow.anchorPoint = ccp(1, 0);
        nextArrow.position = ccp(screenSize.width - 10, 10);
        
        CCMenu *menu = [CCMenu menuWithItems:nextArrow, nil];
        menu.position = CGPointZero;
        menu.tag = NEXT_ARROW_TAG;
        
        [self addChild:menu];
        
        CCScaleTo *scaleup = [CCScaleTo actionWithDuration:0.2 scale:1.5];
        CCScaleTo *scaledown = [CCScaleTo actionWithDuration:0.2 scale:1.0];
        CCCallBlock *highlight = [CCCallBlock actionWithBlock:^{
            
            [ParticleHelper highlightNode:nextArrow forever:NO];
        }];
        
        [nextArrow runAction:[CCSequence actions:scaleup, scaledown, highlight, nil]];
    }
}

- (void)nextScenePressed:(id)sender {
                    
    [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
    [[SoundManager sharedManager] playSoundEffectWithName:FANFARE];
    
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

            CCLOG(@"Take my first turn");
        }
        else {
            
            [[GCTurnBasedMatchHelper sharedInstance] endTurnWithData:[[GameManager sharedManager].currentGame serializeCurrentGameForPlayerWithId:[GKLocalPlayer localPlayer].playerID]];
        }
    }
    else {
        [GameManager sharedManager].currentGame.state = kGameStateGameStarted;
    }
    
    [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[GameScene scene]]];
}

- (void)moveCardToHomePosition:(CardSprite *)card {
    
    GridLocation *homeLocationForCard = [_homePositions objectForKey:card.model.cardIdentifier];
    
    CGPoint position = [_gridLayoutManager getPositionForRowNumber:homeLocationForCard.row columnNumber:homeLocationForCard.column];
    
    CCLOG(@"Card %@ moving to home position %@", card, NSStringFromCGPoint(position));
    
    CCMoveTo *moveAction = [CCMoveTo actionWithDuration:0.2 position:position];
    CCScaleTo *scaleAction = [CCScaleTo actionWithDuration:0.2 scale:0.45];
    
    [card runAction:[CCSpawn actions:moveAction, scaleAction, nil]];
}


- (void)toggleDetailForCard:(CardSprite *)card {
    
    CGSize screenSize = [CCDirector sharedDirector].winSize;

    CCCallFunc *sound = [CCCallFunc actionWithTarget:self selector:@selector(playSwooshSound)];
    
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
    
    [card toggleDetailWithScale:0.4];
}

- (void)playSwooshSound {
    
    [[SimpleAudioEngine sharedEngine] playEffect:SWOOSH_SOUND];
}

@end
