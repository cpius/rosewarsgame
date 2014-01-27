//
//  HKDialogNodeProtocol.h
//  RoseWars
//
//  Created by Heine Kristensen on 16/01/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <Foundation/Foundation.h>

@class HKDialogNode;
@protocol HKDialogNodeProtocol <NSObject>

@optional
- (void)dialogNodeDidDismiss:(HKDialogNode*)dialogNode;

@end
