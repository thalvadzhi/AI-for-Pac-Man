#include <SDL2/SDL.h>
#include <SDL2/SDL_events.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <fcntl.h>
#include "Controls.h"

bool isRunning = true;
bool isPaused = false;
Board board;

static bool isAIControlled = false;
static int aiSocketFD = -1;

static const char* aiSocketAddress = "./pacman_ai_socket";

void handleInput()
{
	SDL_Event curEvent;
	while (SDL_PollEvent(&curEvent)) {
		switch (curEvent.type) 
		{
		case SDL_QUIT:
			isRunning = false;
			break;
		case SDL_KEYDOWN:
            switch (curEvent.key.keysym.sym) {
                case SDLK_p:
                    isPaused = !isPaused;
                    break;
            }
			if (!isAIControlled) {
                switch (curEvent.key.keysym.sym) {
                case SDLK_w:
                case SDLK_UP:
                    board.player.turn(Up);
                    break;
                case SDLK_s:
                case SDLK_DOWN:
                    board.player.turn(Down);
                    break;
                case SDLK_a:
                case SDLK_LEFT:
                    board.player.turn(Left);
                    break;
                case SDLK_d:
                case SDLK_RIGHT:
                    board.player.turn(Right);
                    break;
                }
			}
			break;
		}
	}
    if (isAIControlled) {
		char buffer;
		read(aiSocketFD, &buffer, sizeof(buffer));

		switch (buffer) {
			case aiUp:
				board.player.turn(Up);
				break;
			case aiDown:
				board.player.turn(Down);
				break;
			case aiLeft:
				board.player.turn(Left);
				break;
			case aiRight:
				board.player.turn(Right);
				break;
		}
	}
}

bool isGamePaused()
{
    return isPaused;
}

bool useAIControls(const bool& useAI)
{
	isAIControlled = useAI;
	if (aiSocketFD < 0)
	{
		if (!isAIControlled)
		{
			close(aiSocketFD);
			return true;
		}

		// Create socket
		int socketFD;
		if ((socketFD = socket(AF_LOCAL, SOCK_STREAM, 0)) < 0)
			return false;

		struct sockaddr_un serverAddress;
		memset((char *) &serverAddress, 0, sizeof(serverAddress));
		serverAddress.sun_family = AF_LOCAL;
		strcpy(serverAddress.sun_path, aiSocketAddress);
		socklen_t serverLength = strlen(serverAddress.sun_path) + sizeof(serverAddress.sun_family);

		if (bind(socketFD, (struct sockaddr *) &serverAddress, serverLength) < 0) {
			close(socketFD);
			return false;
		}

		listen(socketFD, 5);
		struct sockaddr_un clientAddress;
		socklen_t clientLength = sizeof(clientAddress);
		aiSocketFD = accept(socketFD, (struct sockaddr *) &clientAddress, &clientLength);

		unlink(aiSocketAddress);
		close(socketFD);

		if (aiSocketFD < 0)
			return false;

		// Make socket non blocking
		int flags = fcntl(aiSocketFD ,F_GETFL, 0);
		if (fcntl(aiSocketFD, F_SETFL, flags | O_NONBLOCK) < 0) {
			close(aiSocketFD);
			return false;
		}
	}
	return true;
}

void updateAI()
{
	if (!isAIControlled || aiSocketFD < 0)
		return;

	std::string boardState = board.getState(Version);
    size_t length = boardState.length() + 1;
	if (write(aiSocketFD, (void*) boardState.c_str(), length) < length) {
		close(aiSocketFD);
		isAIControlled = false;
	}
}

void exitGame(const int& status)
{
	SDL_Delay(3000);
	quitGraphics();
    close(aiSocketFD);
	std::exit(status);
}

Fps::Fps(const int & fps) : fps(fps)
{
	frameDuration = 1000 / fps;
	frameCounter = 0;
	lastSecondFPS = 0;
	lastRefresh = SDL_GetTicks();
	lastSecondTicks = lastRefresh;
}

void Fps::limit()
{
	++frameCounter;
	int currentTicks = SDL_GetTicks();
	int lastFrameTicks = currentTicks - lastRefresh;
	if (lastFrameTicks < frameDuration){
		SDL_Delay(frameDuration - lastFrameTicks);
		lastRefresh += lastFrameTicks;
	}
	lastRefresh = currentTicks;
	if (currentTicks - lastSecondTicks >= 1000) {
		lastSecondFPS = 1000.0f / frameCounter;
		frameCounter = 0;
		lastSecondTicks = currentTicks;
	}
}

float Fps::measure()
{
	return lastSecondFPS;
}
