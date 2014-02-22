//
//  HKGameOptionsDialogProtocol.h
//  RoseWars
//
//  Created by Heine Kristensen on 07/02/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef NS_ENUM(NSInteger, GameOptionsDialogResult) {
    GameOptionsDialogResume,
    GameOptionsDialogOptions,
    GameOptionsDialogMainMenu
};

@class HKGameOptionsDialog;
@protocol HKGameOptionsDialogProtocol <NSObject>

- (void)dialogNodeDidDismiss:(HKGameOptionsDialog*)dialogNode withSelectedResult:(GameOptionsDialogResult)result;

@end
