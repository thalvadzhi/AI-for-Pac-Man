#include "Graphics.h"
#include "Controls.h"
#include "Constants.h"

int main(int argc, char* argv[])
{
	srand(RandomSeed);
	if (!initGraphics()) {
		return 1;
	}

	Fps fps(FPS);

    useAIControls(); // TODO: Export to a menu
	board.initTimers();
	while (isRunning)
	{
		handleInput();
		board.update();
		updateAI(); // TODO: create a separate system for AI
		clearScreen();
		render(); // TODO: Render FPS
		fps.limit();
	}

	exitGame(0);
	return 0;
}