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
#import "CCBReader.h"
#import "TimedBonus.h"
#import "BonusSprite.h"
#import "ParticleHelper.h"
#import "GameManager.h"

@interface ConstructDeckScene()

- (void)presentCards;

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
        
        CGSize screenSize = [CCDirector sharedDirector].winSize;
                
        CCSprite *background = [CCSprite spriteWithFile:@"woddenbackground.png"];
        background.position = ccp(screenSize.width / 2, screenSize.height / 2);
        [self addChild:background z:-1];

        _deckOfCards = [CCSprite spriteWithFile:@"deckgreencard.png"];
        _deckOfCards.anchorPoint = ccp(0, 1);
        _deckOfCards.position = ccp(20, [_deckOfCards contentSize].height + 20);
        [self addChild:_deckOfCards];
        
        
        CCDelayTime *delayAction = [CCDelayTime actionWithDuration:1.0];
        CCCallFunc *funcAction = [CCCallFunc actionWithTarget:self selector:@selector(presentCards)];
        [self runAction:[CCSequence actions:delayAction, funcAction, nil]];
    }
    
    return self;
}

- (void)nextScenePressed:(id)sender {
    
    [self removeAllChildrenWithCleanup:YES];
    
    PlaceCardsScene *scene = [PlaceCardsScene scene];
    
    [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
    
    [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:(CCScene*)scene]];
}

- (void)presentCards {
        
    CGSize screenSize = [CCDirector sharedDirector].winSize;
    
    self.isTouchEnabled = YES;
    
    GridlLayoutManager *gridLayoutManager = [[GridlLayoutManager alloc] init];
    
    gridLayoutManager.numberOfRows = 3;
    gridLayoutManager.numberOfColumns = 4;
    gridLayoutManager.columnPadding = 0;
    gridLayoutManager.gridSize = CGSizeMake(screenSize.width, screenSize.height / 2);

    gridLayoutManager.yOffset = screenSize.height;
    
    NSInteger row = 1, column = 1;
    float cardCounter = 1;
    
    for (Card *card in [GameManager sharedManager].currentGame.myDeck.cards) {
        
        CCLOG(@"Cardtype: %@", NSStringFromClass([card class]));
        
        card.scale = 0.8;
        card.position = ccp(_deckOfCards.position.x + 30, _deckOfCards.position.y - 40);
        card.rotation = -10;
        card.cardLocation = MakeGridLocation(row, column);
        
        [self addChild:card];
        
        CGPoint cardPosition = [gridLayoutManager getPositionForRowNumber:row columnNumber:column];
        
        CCScaleTo *scale = [CCScaleTo actionWithDuration:0.5 scale:0.5];
        CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.5 position:cardPosition];
        CCRotateTo *rotate = [CCRotateTo actionWithDuration:0.5 angle:0];
        CCSpawn *spawn = [CCSpawn actions:scale, moveTo, rotate, nil];
        CCCallFunc *sound = [CCCallFunc actionWithTarget:self selector:@selector(playBoomSound)];
        CCDelayTime *delay = [CCDelayTime actionWithDuration:0.5];
        
        CCCallBlock *checkFinished = [CCCallBlock actionWithBlock:^{
            
            if (cardCounter + 1 == [GameManager sharedManager].currentGame.myDeck.cards.count) {
                
                [self finishedDealingCards];
            }
        }];
        
        CCSequence *sequence = [CCSequence actions:spawn, sound, checkFinished, delay, nil];
        [card runAction:sequence];
        
        cardCounter++;
        column++;
        
        if (column > 4) {
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
    
    TimedBonus *bonus = [[TimedBonus alloc] initWithValue:1 forNumberOfRounds:1];

    if (drawNumber.integerValue == 1) {
        [card.attack addTimedBonus:bonus];
    }
    
    if (drawNumber.integerValue == 2) {
        [card.defence addTimedBonus:bonus];
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
    
    for (Card *card in [GameManager sharedManager].currentGame.myDeck.cards) {
        
		if(CGRectContainsPoint(card.boundingBox, convLoc)) {
            CGSize screenSize = [CCDirector sharedDirector].winSize;
            
            CCCallFunc *sound = [CCCallFunc actionWithTarget:self selector:@selector(playSwooshSound)];

            if (card.isShowingDetail) {
                
                GridlLayoutManager *gridLayoutManager = [[GridlLayoutManager alloc] init];
                
                gridLayoutManager.numberOfRows = 3;
                gridLayoutManager.numberOfColumns = 4;
                gridLayoutManager.columnPadding = 0;
                gridLayoutManager.gridSize = CGSizeMake(screenSize.width, screenSize.height / 2);
                
                gridLayoutManager.yOffset = screenSize.height;
                
                CGPoint location = [gridLayoutManager getPositionForRowNumber:card.cardLocation.row columnNumber:card.cardLocation.column];
                
                CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.3 position:location];
                CCSpawn *spawn = [CCSpawn actions: moveTo, sound, nil];
                [card runAction:spawn];
            }
            else {
                CCMoveTo *moveTo = [CCMoveTo  actionWithDuration:0.3 position:CGPointMake(screenSize.width / 2, screenSize.height / 2)];
                CCSpawn *spawn = [CCSpawn actions: moveTo, sound, nil];
                [card runAction:spawn];
            }
            
            [card toggleDetailWithScale:0.5];
            
			break;
		}
	}
}

@end
