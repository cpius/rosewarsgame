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

@interface PlaceCardsScene()

- (void)toggleDetailForCard:(Card*)card;
- (void)moveCardToHomePosition:(Card*)card;

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

        _gameboard = [[GameBoard alloc] initWithPlayerColor:kPlayerGreen];

        _gameboard.contentSize = CGSizeMake(320, 375);
        _gameboard.rows = 4;
        _gameboard.columns = 5;
        _gameboard.anchorPoint = ccp(0.5, 0.5);
        _gameboard.colorOfBottomPlayer = kPlayerGreen;
        _gameboard.colorOfTopPlayer = kPlayerGreen;
        
        _gameboard.position = ccp(screenSize.width / 2, (screenSize.height / 2) + 50);
        [self addChild:_gameboard];
        
        [_gameboard layoutBoard];
        
        _gridLayoutManager = [[GridlLayoutManager alloc] init];
        
        _gridLayoutManager.numberOfRows = 2;
        _gridLayoutManager.numberOfColumns = 5;
        _gridLayoutManager.gridSize = CGSizeMake(screenSize.width, 140);
        _gridLayoutManager.rowPadding = -8;
        _gridLayoutManager.columnPadding = 0;
        _gridLayoutManager.yOffset = 135;
        
        _placedCards = [[NSMutableArray alloc] init];
        
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
    
    for (Card *card in [GameManager sharedManager].currentGame.myDeck.cards) {
        
        card.position = ccp(screenSize.width / 2, -200);
        card.cardLocation = MakeGridLocation(row, column);
        
        [self addChild:card];
        
        CGPoint cardPosition = [_gridLayoutManager getPositionForRowNumber:row columnNumber:column];
        
        CCScaleTo *scale = [CCScaleTo actionWithDuration:0.1 * cardCounter scale:0.40];
        CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.1 * cardCounter position:cardPosition];
        CCEaseIn *ease = [CCEaseIn actionWithAction:moveTo rate:2.0];
        CCSpawn *spawn = [CCSpawn actions:scale, ease, nil];
        [card runAction:spawn];
        
        cardCounter++;
        column++;
        
        if (column > _gridLayoutManager.numberOfColumns) {
            column = 1;
            row++;
        }
    }
}

- (void)selectSpriteForTouch:(CGPoint)touchLocation {
    Card * newCard = nil;
    for (Card *card in [GameManager sharedManager].currentGame.myDeck.cards) {
        if (CGRectContainsPoint(card.boundingBox, touchLocation)) {
            newCard = card;
            break;
        }
    }
    if (newCard != _selectedCard) {
        [_selectedCard stopAllActions];
        _selectedCard = newCard;
        [_selectedCard setZOrder:100];
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

- (void)ccTouchEnded:(UITouch *)touch withEvent:(UIEvent *)event {
        
    CGPoint location = [touch locationInView:touch.view];
    CGPoint convLoc = [[CCDirector sharedDirector] convertToGL:location];
    
    GameBoardNode *gameboardNode = [_gameboard getGameBoardNodeForPosition:[_gameboard convertTouchToNodeSpace:touch]];
    
    if (_detailCard == nil) {
        if (gameboardNode != nil && !gameboardNode.hasCard && _selectedCard != nil) {
            
            [_gameboard placeCard:_selectedCard inGameBoardNode:gameboardNode useHighLighting:YES];
            
            if (![_placedCards containsObject:_selectedCard]) {
                [_placedCards addObject:_selectedCard];
            }
            
            if (_placedCards.count == [GameManager sharedManager].currentGame.myDeck.cards.count) {
                [self finishedPlacingCards];
            }

            [_selectedCard setZOrder:0];
            _selectedCard = nil;
            _isMovingCard = NO;
            
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
                
                gameboardNode.card = nil;
                
                return;
            }
        }
    }

    for (Card *card in [GameManager sharedManager].currentGame.myDeck.cards) {
        
		if(CGRectContainsPoint(card.boundingBox, convLoc)) {
            
            [self toggleDetailForCard:card];
            
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
    
    [GameManager sharedManager].currentGame.state = kGameStateFinishedPlacingCards;
    
    [self removeAllChildrenWithCleanup:YES];
        
    [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
    
    [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[GameScene scene]]];
}

- (void)moveCardToHomePosition:(Card *)card {
    
    CCMoveTo *moveAction = [CCMoveTo actionWithDuration:0.2 position:[_gridLayoutManager getPositionForRowNumber:card.cardLocation.row columnNumber:card.cardLocation.column]];
    
    [card runAction:moveAction];
}


- (void)toggleDetailForCard:(Card *)card {
    
    CGSize screenSize = [CCDirector sharedDirector].winSize;

    CCCallFunc *sound = [CCCallFunc actionWithTarget:self selector:@selector(playSwooshSound)];
    
    if (card.isShowingDetail) {
        
        CGPoint location = [_gridLayoutManager getPositionForRowNumber:card.cardLocation.row columnNumber:card.cardLocation.column];
        
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
