//
//  ConstructDeckScene.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/20/12.
//
//

#import "ConstructDeckScene.h"
#import "GridlLayoutManager.h"
#import "PlaceCardsScene.h"
#import "TimedBonus.h"
#import "BonusSprite.h"
#import "ParticleHelper.h"
#import "GameManager.h"
#import "CardSprite.h"
#import "RandomDeckStrategy.h"

@interface ConstructDeckScene()

- (void)presentCards;
- (void)moveCardToHomePosition:(CardSprite*)card;

@end

@implementation ConstructDeckScene

@synthesize currentDeck = _currentDeck;

+ (id)scene {
    
    CCScene *scene = [CCScene node];
    
    ConstructDeckScene *layer = [ConstructDeckScene node];
    
    [scene addChild:layer];
    
    return scene;
}

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        _screenSize = [CCDirector sharedDirector].winSize;
                
        CCSprite *background = [CCSprite spriteWithFile:@"woddenbackground2.png"];
        background.position = ccp(_screenSize.width / 2, _screenSize.height / 2);
        [self addChild:background z:-1];

        _deckOfCards = [CCSprite spriteWithFile:@"deckgreencard.png"];
        _deckOfCards.anchorPoint = ccp(0, 1);
        _deckOfCards.position = ccp(20, [_deckOfCards contentSize].height + 20);
        [self addChild:_deckOfCards];
        
        CCMenuItem *refreshButton = [CCMenuItemImage itemWithNormalImage:@"refreshbutton.png" selectedImage:@"refreshbutton.png" target:self selector:@selector(refreshButtonPressed:)];
        
        refreshButton.anchorPoint = ccp(1, 0);
        refreshButton.position = ccp(_screenSize.width - 20, 60);
        
        CCMenu *menu = [CCMenu menuWithItems:refreshButton, nil];
        menu.position = CGPointZero;
        [self addChild:menu];
        
        CardSprite *tempSprite = [[CardSprite alloc] initWithCard:[[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0]];
        _cardSize = CGSizeMake(tempSprite.contentSize.width * 0.5, tempSprite.contentSize.height * 0.5);
        
        CCDelayTime *delayAction = [CCDelayTime actionWithDuration:1.0];
        CCCallFunc *funcAction = [CCCallFunc actionWithTarget:self selector:@selector(presentCards)];
        [self runAction:[CCSequence actions:delayAction, funcAction, nil]];
    }
    
    return self;
}

- (void)refreshButtonPressed:(id)sender {
    
    for (CCSprite *cardSprite in self.children) {
        
        if ([cardSprite isKindOfClass:[CardSprite class]]) {
            [cardSprite removeFromParentAndCleanup:YES];
        }
    }
    
    [GameManager sharedManager].currentGame.myDeck = [[RandomDeckStrategy strategy] generateNewDeckWithNumberOfBasicType:6 andSpecialType:1 cardColor:[GameManager sharedManager].currentGame.myColor];
    
    [self presentCards];
}

- (void)nextScenePressed:(id)sender {
    
    [self removeAllChildrenWithCleanup:YES];
    
    PlaceCardsScene *scene = [PlaceCardsScene scene];
    
    [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
    
    [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:(CCScene*)scene]];
}

- (void)presentCards {
        
    CGSize screenSize = [CCDirector sharedDirector].winSize;
    
    self.isTouchEnabled = YES;
    
    GridlLayoutManager *gridLayoutManager = [[GridlLayoutManager alloc] init];
    
    gridLayoutManager.numberOfRows = 2;
    gridLayoutManager.numberOfColumns = 5;
    gridLayoutManager.columnPadding = 4;
    gridLayoutManager.columnWidth = _cardSize.width;
    gridLayoutManager.rowHeight = _cardSize.height;
    gridLayoutManager.gridSize = CGSizeMake(screenSize.width, screenSize.height / 2);

    gridLayoutManager.yOffset = screenSize.height;
    gridLayoutManager.xOffset = 8;
    
    NSInteger row = 1, column = 1;
    float cardCounter = 1;
    
    _cardSprites = [[NSMutableArray alloc] initWithCapacity:[GameManager sharedManager].currentGame.myDeck.cards.count];
    
    for (Card *card in [GameManager sharedManager].currentGame.myDeck.cards) {
        
        CCLOG(@"Cardtype: %@", NSStringFromClass([card class]));
        
        CardSprite *cardSprite = [[CardSprite alloc] initWithCard:card];
        
        cardSprite.tag = 100;
        cardSprite.scale = 0.8;
        cardSprite.position = ccp(_deckOfCards.position.x + 30, _deckOfCards.position.y - 40);
        cardSprite.rotation = -10;
        cardSprite.model.cardLocation = [GridLocation gridLocationWithRow:row column:column];
        
        [self addChild:cardSprite];
        [_cardSprites addObject:cardSprite];
        
        CGPoint cardPosition = [gridLayoutManager getPositionForRowNumber:row columnNumber:column];
        
        CCScaleTo *scale = [CCScaleTo actionWithDuration:0.1 * (cardCounter + 1) scale:0.5];
        CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.1 * (cardCounter + 1) position:cardPosition];
        CCRotateTo *rotate = [CCRotateTo actionWithDuration:0.1 * (cardCounter + 1) angle:0];
        CCSpawn *spawn = [CCSpawn actions:scale, moveTo, rotate, nil];
        CCDelayTime *delay = [CCDelayTime actionWithDuration:0.1];
        
        CCCallBlock *checkFinished = [CCCallBlock actionWithBlock:^{
            
            if (cardCounter + 1 == [GameManager sharedManager].currentGame.myDeck.cards.count) {
                
                [self finishedDealingCards];
            }
        }];
        
        CCSequence *sequence = [CCSequence actions:spawn, checkFinished, delay, nil];
        [cardSprite runAction:sequence];
        
        cardCounter++;
        column++;
        
        if (column > 5) {
            column = 1;
            row++;
        }
    }
}

- (void)finishedDealingCards {
    
    CGSize screenSize = [CCDirector sharedDirector].winSize;

    [self addBonusToCard:[[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0] withDrawNumber:@1];
    [self addBonusToCard:[[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:1] withDrawNumber:@2];

    CCMenuItem *nextArrow = [CCMenuItemImage itemWithNormalImage:@"right_arrow.png" selectedImage:@"right_arrow.png" target:self selector:@selector(nextScenePressed:)];
    
    nextArrow.anchorPoint = ccp(1, 0);
    nextArrow.position = ccp(screenSize.width - 20, 20);
    
    CCMenu *menu = [CCMenu menuWithItems:nextArrow, nil];
    menu.position = CGPointZero;
    [self addChild:menu];
    
    CCScaleTo *scaleup = [CCScaleTo actionWithDuration:0.2 scale:1.5];
    CCScaleTo *scaledown = [CCScaleTo actionWithDuration:0.2 scale:1.0];
    CCCallBlock *highlight = [CCCallBlock actionWithBlock:^{
        
        [ParticleHelper highlightNode:nextArrow forever:NO];
    }];
    
    [nextArrow runAction:[CCSequence actions:scaleup, scaledown, highlight, nil]];
}

- (void)particleOnSprite:(CCSprite*)sprite {
    
}

- (void)addBonusToCard:(Card*)card withDrawNumber:(NSNumber*)drawNumber {
    
    RawBonus *bonus = [[RawBonus alloc] initWithValue:1];

    if (drawNumber.integerValue == 1) {
        [card.attack addRawBonus:bonus];
    }
    
    if (drawNumber.integerValue == 2) {
        [card.defence addRawBonus:bonus];
    }
}

- (void)playBoomSound {
    
  //  [[SimpleAudioEngine sharedEngine] playEffect:BOOM_SOUND];
}

- (void)playSwooshSound {
    
//    [[SimpleAudioEngine sharedEngine] playEffect:SWOOSH_SOUND];
}

- (void)ccTouchesEnded:(NSSet *)touches withEvent:(UIEvent *)event {
    
    UITouch *touch = [touches anyObject];
    
    CGPoint location = [touch locationInView:touch.view];
    CGPoint convLoc = [[CCDirector sharedDirector] convertToGL:location];
    
    for (CardSprite *card in _cardSprites) {
        
		if(CGRectContainsPoint(card.boundingBox, convLoc)) {
            CGSize screenSize = [CCDirector sharedDirector].winSize;
            
            CCCallFunc *sound = [CCCallFunc actionWithTarget:self selector:@selector(playSwooshSound)];

            if (card.model.isShowingDetail) {
                
                [self moveCardToHomePosition:card];
            }
            else {
                CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.3 position:CGPointMake(screenSize.width / 2, screenSize.height / 2)];
                CCSpawn *spawn = [CCSpawn actions: moveTo, sound, nil];
                [card runAction:spawn];
            }
            
            [card toggleDetailWithScale:0.5];
		}
	}
}

- (void)moveCardToHomePosition:(CardSprite *)card {
    
    GridlLayoutManager *gridLayoutManager = [[GridlLayoutManager alloc] init];
    
    gridLayoutManager.numberOfRows = 2;
    gridLayoutManager.numberOfColumns = 5;
    gridLayoutManager.columnPadding = 4;
    gridLayoutManager.columnWidth = _cardSize.width;
    gridLayoutManager.rowHeight = _cardSize.height;
    gridLayoutManager.gridSize = CGSizeMake(_screenSize.width, _screenSize.height / 2);
    
    gridLayoutManager.yOffset = _screenSize.height;
    gridLayoutManager.xOffset = 8;
    
    CGPoint location = [gridLayoutManager getPositionForRowNumber:card.model.cardLocation.row columnNumber:card.model.cardLocation.column];
    
    CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.3 position:location];
    CCSpawn *spawn = [CCSpawn actions: moveTo, nil];
    [card runAction:spawn];
}

@end
