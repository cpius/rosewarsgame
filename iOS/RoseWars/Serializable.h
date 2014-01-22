//
//  Serializable.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/2/13.
//
//

#import <Foundation/Foundation.h>

@protocol Serializable <NSObject>

- (NSDictionary*)asDictionary;
- (void)fromDictionary:(NSDictionary*)dictionary;

@end
