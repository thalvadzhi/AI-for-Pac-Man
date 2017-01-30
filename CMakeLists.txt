cmake_minimum_required(VERSION 2.8)
project(PacMan)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -lSDL2 -lSDL2_ttf -lSDL2_image")
set(CMAKE_CXX_COMPILER "/usr/bin/clang++")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/)

set(SRC
	./src/Board.cpp
	./src/Constants.cpp  
	./src/Controls.cpp 
	./src/Ghost.cpp  
	./src/Graphics.cpp  
	./src/Map.cpp  
	./src/MobileObject.cpp  
)

set(HEADERS
	./src/Board.h  
	./src/Constants.h  
	./src/Controls.h 
	./src/Ghost.h  
	./src/Graphics.h  
	./src/Main.cpp  
	./src/Map.h  
	./src/MobileObject.h  
	./src/Utils.h
)

add_executable(${PROJECT_NAME}.elf ${SRC} ${HEADERS})
