#pragma once

#include "Board.h"

extern bool isRunning;
extern bool isInGame;
extern Board board;

bool isGamePaused();
bool useAIControls(const bool& = true);
void updateAI();
void handleInput();
void exitGame(const int&);

class Fps
{
public:
	Fps(const int&);
	void limit();
	float measure();
private:
	float lastSecondFPS;
	int frameDuration;
	int fps;
	int frameCounter;
	int lastRefresh;
	int lastSecondTicks;
};