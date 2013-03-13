//
//  AppDelegate.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/18/12.
//  Copyright __MyCompanyName__ 2012. All rights reserved.
//

#import "cocos2d.h"

#import "AppDelegate.h"
#import "GCTurnBasedMatchHelper.h"
#import "MainMenuScene.h"
#import "GridlLayoutManager.h"
#import "SoundManager.h"

@implementation AppController

@synthesize window=window_, navController=navController_, director=director_;

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
	// Create the main window
	window_ = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];


	// Create an CCGLView with a RGB565 color buffer, and a depth buffer of 0-bits
	CCGLView *glView = [CCGLView viewWithFrame:[window_ bounds]
								   pixelFormat:kEAGLColorFormatRGB565	//kEAGLColorFormatRGBA8
								   depthFormat:0	//GL_DEPTH_COMPONENT24_OES
							preserveBackbuffer:NO
									sharegroup:nil
								 multiSampling:NO
							   numberOfSamples:0];

	director_ = (CCDirectorIOS*) [CCDirector sharedDirector];

	director_.wantsFullScreenLayout = YES;

	// Display FSP and SPF
	[director_ setDisplayStats:YES];

	// set FPS at 60
	[director_ setAnimationInterval:1.0/60];

	// attach the openglView to the director
	[director_ setView:glView];

	// for rotation and other messages
	[director_ setDelegate:self];

	// 2D projection
	[director_ setProjection:kCCDirectorProjection2D];
//	[director setProjection:kCCDirectorProjection3D];

	// Enables High Res mode (Retina Display) on iPhone 4 and maintains low res on all other devices
	if( ! [director_ enableRetinaDisplay:YES] )
		CCLOG(@"Retina Display Not supported");

	// Create a Navigation Controller with the Director
	navController_ = [[UINavigationController alloc] initWithRootViewController:director_];
	navController_.navigationBarHidden = YES;

	// set the Navigation Controller as the root view controller
//	[window_ setRootViewController:rootViewController_];
//	[window_ addSubview:navController_.view];
    window_.rootViewController = navController_;

	// make main window visible
	[window_ makeKeyAndVisible];

	// Default texture format for PNG/BMP/TIFF/JPEG/GIF images
	// It can be RGBA8888, RGBA4444, RGB5_A1, RGB565
	// You can change anytime.
	[CCTexture2D setDefaultAlphaPixelFormat:kCCTexture2DPixelFormat_RGBA8888];

	// If the 1st suffix is not found and if fallback is enabled then fallback suffixes are going to searched. If none is found, it will try with the name without suffix.
	// On iPad HD  : "-ipadhd", "-ipad",  "-hd"
	// On iPad     : "-ipad", "-hd"
	// On iPhone HD: "-hd"
	CCFileUtils *sharedFileUtils = [CCFileUtils sharedFileUtils];
	[sharedFileUtils setEnableFallbackSuffixes:NO];				// Default: NO. No fallback suffixes are going to be used
	[sharedFileUtils setiPhoneRetinaDisplaySuffix:@"-hd"];		// Default on iPhone RetinaDisplay is "-hd"
	[sharedFileUtils setiPadSuffix:@"-ipad"];					// Default on iPad is "ipad"
	[sharedFileUtils setiPadRetinaDisplaySuffix:@"-ipadhd"];	// Default on iPad RetinaDisplay is "-ipadhd"

	// Assume that PVR images have premultiplied alpha
	[CCTexture2D PVRImagesHavePremultipliedAlpha:YES];
    
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"archer_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"archer_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"archer_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"archer_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"ballista_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"ballista_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"ballista_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"ballista_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"catapult_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"catapult_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"catapult_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"catapult_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"pikeman_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"pikeman_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"pikeman_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"pikeman_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"lightcavalry_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"lightcavalry_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"lightcavalry_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"lightcavalry_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"heavycavalry_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"heavycavalry_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"heavycavalry_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"heavycavalry_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"chariot_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"chariot_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"chariot_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"chariot_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"cannon_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"cannon_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"cannon_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"cannon_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"berserker_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"berserker_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"berserker_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"berserker_icon.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"scout_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"scout_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"scout_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"scout_icon.png"];
    
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"flagbearer_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"flagbearer_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"flagbearer_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"flagbearer_icon.png"];

    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"lancer_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"lancer_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"lancer_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"lancer_icon.png"];

    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"royalguard_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"royalguard_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"royalguard_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"royalguard_icon.png"];

    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"samurai_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"samurai_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"samurai_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"samurai_icon.png"];

    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"viking_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"viking_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"viking_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"viking_icon.png"];

    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"longswordsman_0.png" rect:CGRectMake(0, 0, 236, 362)] name:@"longswordsman_0.png"];
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFrame:[CCSpriteFrame frameWithTextureFilename:@"longswordsman_icon.png" rect:CGRectMake(0, 0, 112, 152)] name:@"longswordsman_icon.png"];

    [[SoundManager sharedManager] preloadSoundEffects];
    
	// and add the scene to the stack. The director will run it when it automatically when the view is displayed.
	[director_ pushScene: [MainMenuScene scene]];
            
    [[GCTurnBasedMatchHelper sharedInstance] authenticateLocalUser];
    
    [glView setMultipleTouchEnabled:TRUE];
    
	return YES;
}

// Supported orientations: Landscape. Customize it for your own needs
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
	return UIInterfaceOrientationIsPortrait(interfaceOrientation);
}


// getting a call, pause the game
-(void) applicationWillResignActive:(UIApplication *)application
{
	if( [navController_ visibleViewController] == director_ )
		[director_ pause];
}

// call got rejected
-(void) applicationDidBecomeActive:(UIApplication *)application
{
	if( [navController_ visibleViewController] == director_ )
		[director_ resume];
}

-(void) applicationDidEnterBackground:(UIApplication*)application
{
	if( [navController_ visibleViewController] == director_ )
		[director_ stopAnimation];
}

-(void) applicationWillEnterForeground:(UIApplication*)application
{
	if( [navController_ visibleViewController] == director_ )
		[director_ startAnimation];
}

// application will be killed
- (void)applicationWillTerminate:(UIApplication *)application
{
	CC_DIRECTOR_END();
}

// purge memory
- (void)applicationDidReceiveMemoryWarning:(UIApplication *)application
{
	[[CCDirector sharedDirector] purgeCachedData];
}

// next delta time will be zero
-(void) applicationSignificantTimeChange:(UIApplication *)application
{
	[[CCDirector sharedDirector] setNextDeltaTimeZero:YES];
}

@end
