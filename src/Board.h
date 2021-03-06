#pragma once

#include <SDL2/SDL.h>
#include "Graphics.h"
#include "Map.h"
#include "MobileObject.h"
#include "Ghost.h"

class Player : public MobileObject
{
public:
	Player(const int&, const int&);
	virtual void move(Map&);
	void turn(const unsigned char&);
	void reset(const Map&);
	static void loadAnimations();
	std::string getState(const int& version) const;

	unsigned int score;
	unsigned char lives = 3;
	unsigned char streak = 1;
	unsigned short dotsEaten;
private:
	static Animation walk;
	void tryTurn(const Map&);
	static bool isPlayerWalkable(const char&);
};

class Board
{
private:
	Map map;
public:
	Board();
	void update();
	void draw(SDL_Renderer*);
	void onPillCollected();
	void lostLive();
	void initTimers();
    int getGameTime() const;
	static void loadTextures(); 
	std::string getState(const int& version) const;

	Player player;
	Pinky pinky; // TODO: Put the ghosts in an array/map and use polymorphism or do data oriented
	Inky inky;
	Blinky blinky;
	Clyde clyde;
	pos drawLocation;
private:
	Text score;
    int gameTime;
	unsigned char cherries = 2;
	static Texture cherry;
	static Texture live;

	void drawScore(SDL_Renderer*);
	void drawIngameInfo(SDL_Renderer*);
};
