//
//  HKConstructDeckScene.m
//  RoseWars
//
//  Created by Heine Skov Kristensen on 8/16/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import "HKConstructDeckScene.h"
#import "GridlLayoutManager.h"
#import "CardSprite.h"
#import "HKImageButton.h"
#import "HKPlaceCardsScene.h"

@interface HKConstructDeckScene() {
    
    CGSize _cardSize;
    NSMutableArray *_cardSprites;
    SKSpriteNode *_deck;
}

@end

@implementation HKConstructDeckScene

- (void)didMoveToView:(SKView *)view {
    
    self.userInteractionEnabled = YES;

    SKSpriteNode *backgroundNode = [SKSpriteNode spriteNodeWithImageNamed:@"woddenbackground"];
    
    backgroundNode.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMidY(self.frame));
    backgroundNode.size = self.size;
    [self addChild:backgroundNode];
    
    _deck = [SKSpriteNode spriteNodeWithImageNamed:@"DeckGreenCard"];
    
    _deck.anchorPoint = CGPointMake(0, 0);
    _deck.position = CGPointMake(20, 20);
    [self addChild:_deck];
    
    CardSprite *tempSprite = [[CardSprite alloc] initWithCard:[[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0]];
    _cardSize = CGSizeMake(tempSprite.calculateAccumulatedFrame.size.width * 0.5, tempSprite.calculateAccumulatedFrame.size.height * 0.5);
    
    [self runAction:[SKAction sequence:@[[SKAction waitForDuration:1.0], [SKAction performSelector:@selector(presentCards) onTarget:self]]]];
}

- (void)presentCards {
    
    CGSize screenSize = self.size;
    
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
        
        NSLog(@"Cardtype: %@", NSStringFromClass([card class]));
        
        CardSprite *cardSprite = [[CardSprite alloc] initWithCard:card];
        
        cardSprite.name = @"CardSprite";
        [cardSprite setScale:0.45];
        cardSprite.position = _deck.position;
        cardSprite.zRotation = DegreesToRadians(-10);
        cardSprite.model.cardLocation = [GridLocation gridLocationWithRow:row column:column];
        
        [self addChild:cardSprite];
        [_cardSprites addObject:cardSprite];
        
        CGPoint cardPosition = [gridLayoutManager getPositionForRowNumber:row columnNumber:column];
        
        SKAction *scale = [SKAction scaleTo:0.45 duration:0.1 * (cardCounter + 1)];
        SKAction *moveTo = [SKAction moveTo:cardPosition duration:0.1 * (cardCounter + 1)];
        SKAction *rotate = [SKAction rotateToAngle:0 duration:0.1 * (cardCounter + 1)];

        SKAction *group = [SKAction group:@[scale, moveTo, rotate]];
        SKAction *delay = [SKAction waitForDuration:0.1];

        SKAction *checkFinished = [SKAction runBlock:^{
            if (cardCounter + 1 == [GameManager sharedManager].currentGame.myDeck.cards.count) {
                [self finishedDealingCards];
            }
        }];
        
        SKAction *sequence = [SKAction sequence:@[group, checkFinished, delay]];
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
    
    CGSize screenSize = self.size;
    
    [self addBonusToCard:[[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:0] withDrawNumber:@1];
    [self addBonusToCard:[[GameManager sharedManager].currentGame.myDeck.cards objectAtIndex:1] withDrawNumber:@2];
    
    HKImageButton *nextArrow = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Next" block:^(id sender) {
        
        [self runAction:[SKAction playSoundFileNamed:@"buttonclick.wav" waitForCompletion:NO]];

        HKPlaceCardsScene *scene = [HKPlaceCardsScene sceneWithSize:self.size];
        scene.scaleMode = SKSceneScaleModeAspectFill;

        [self.view presentScene:scene transition:[SKTransition fadeWithDuration:0.5]];
    }];
    
    nextArrow.position = CGPointMake(screenSize.width - (nextArrow.size.width / 2) - 10, (nextArrow.size.height / 2) + 10);

    SKAction *scaleup = [SKAction scaleTo:1.5 duration:0.2];
    SKAction *scaledown = [SKAction scaleTo:1.0 duration:0.2];
    
    [self addChild:nextArrow];
    [nextArrow runAction:[SKAction sequence:@[scaleup, scaledown]]];
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


@end
