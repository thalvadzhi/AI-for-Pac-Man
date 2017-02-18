#include "Python.h"
#include <iostream>
#include <assert.h>
#include <bits/unique_ptr.h>
#include <cstring>

typedef std::pair<int, int> pos;

const std::string MAP =
"oooooooooooooooooooooooooooooo"
"oWWWWWWWWWWWWWWWWWWWWWWWWWWWWo"
"oWPPPPPPPPPPPPwwPPPPPPPPPPPPWo"
"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo"
"oWHwoowPwooowPwwPwooowPwoowHWo"
"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo"
"oWPPPPPPPPPPPPPPPPPPPPPPPPPPWo"
"oWPwwwwPwwPwwwwwwwwPwwPwwwwPWo"
"oWPwwwwPwwPwwwwwwwwPwwPwwwwPWo"
"oWPPPPPPwwPPPPwwPPPPwwPPPPPPWo"
"oWWWWWWPwwwwwpwwpwwwwwPWWWWWWo"
"ooooooWPwwwwwpwwpwwwwwPWoooooo"
"ooooooWPwwppppbbppppwwPWoooooo"
"ooooooWPwwpcccddcccpwwPWoooooo"
"oWWWWWWPwwpcoooooocpwwPWWWWWWo"
"ottttttPpppciirrzzcpppPtttttto"
"oWWWWWWPwwpcoooooocpwwPWWWWWWo"
"ooooooWPwwpccccccccpwwPWoooooo"
"ooooooWPwwppppppppppwwPWoooooo"
"ooooooWPwwpwwwwwwwwpwwPWoooooo"
"oWWWWWWPwwpwwwwwwwwpwwPWWWWWWo"
"oWPPPPPPPPPPPPwwPPPPPPPPPPPPWo"
"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo"
"oWPwwwwPwwwwwPwwPwwwwwPwwwwPWo"
"oWHPPwwPPPPPPPssPPPPPPPwwPPHWo"
"oWwwPwwPwwPwwwwwwwwPwwPwwPwwWo"
"oWwwPwwPwwPwwwwwwwwPwwPwwPwwWo"
"oWPPPPPPwwPPPPwwPPPPwwPPPPPPWo"
"oWPwwwwwwwwwwPwwPwwwwwwwwwwPWo"
"oWPwwwwwwwwwwPwwPwwwwwwwwwwPWo"
"oWPPPPPPPPPPPPPPPPPPPPPPPPPPWo"
"oWWWWWWWWWWWWWWWWWWWWWWWWWWWWo"
"oooooooooooooooooooooooooooooo";

const int TileSize = 15;
const unsigned int PacmanMoveSpeed = 110;
const unsigned int GhostMoveSpeed = 100;

const unsigned int PinkyCagedTime = 0;
const unsigned int InkyCagedTime = 3000;
const unsigned int ClydeCagedTime = 6000;

const unsigned char Up =    'U';
const unsigned char Down =  'D';
const unsigned char Left =  'L';
const unsigned char Right = 'R';

const unsigned int FrightenTime = 6000;
const unsigned int ScatterTime = 7000;

const unsigned int DotPoints  = 10;
const unsigned int PillPoints = 50;
const unsigned int GhostPoints = 200;

const unsigned int RandomSeed = 42;

const char InkyChar = 'i';
const char BlinkyChar = 'b';
const char ClydeChar = 'z';
const char PinkyChar = 'r';
const char PlayerChar = 's';
const char Tunel = 't';
const char Cage = 'c';
const char Door = 'd';
const char Outside = 'o';
const char Path = 'p';
const char Dot = 'P';
const char Pill = 'H';
const char InnerWall = 'w';

struct Data;

inline const char& getTileAt(const int& col, const int& row, const Data& data);
inline void setTileAt(const int& y, const int& x, const char & tile, Data& data);
int collisionWall(const Data& data, const int & posX, const int & posY, const unsigned char& direction, bool(*isWalkable)(const char&));
const unsigned char pathFind(const Data& data, const int & x, const int & y, const pos & target, const unsigned char & direction, const int& movement, bool (*isWalkable)(const char&));

pos findTile(const int& posX, const int& posY);
char collectableCheck(Data& data, const int& posX, const int& posY);
void onPillCollected(Data& data);

bool isPlayerWalkable(const char& tile)
{
    return tile == Path || tile == Dot || tile == Pill || tile == Tunel;
}

bool isCagedWalkable(const char& tile)
{
    return tile == Outside || tile == Door || tile == Path || tile == Dot || tile == Pill;
}

bool isScatterWalkable(const char& tile)
{
    return tile == Path || tile == Dot || tile == Pill;
}

bool isEatenWalkable(const char & tile)
{
    return tile == Path || tile == Dot || tile == Pill || tile == Outside || tile == Door;
}

bool isGhostWalkable(const char& tile)
{
    return tile == Path || tile == Dot || tile == Pill;
}

struct MobileObject
{
    virtual ~MobileObject() {}
    virtual void move(Data& data) = 0;

    int posX, posY;
    unsigned char direction;

    virtual void putOnTrack(const Data& data)
    {
        auto tile = findTile(posX, posY);
        switch (direction)
        {
            case Up:
            case Down:
                posX = tile.first * TileSize + TileSize / 2;
                break;
            case Left:
            case Right:
                posY = tile.second * TileSize + TileSize / 2;
                break;
        }
    }

    int frameDistance(const int& speed, const Data& data) const;

    virtual void reset(const Data& data);
};

struct Player : MobileObject {
    int score;
    int streak;
    int lives;
    char turn;

    void tryTurn(const Data& data);

    virtual void move(Data& data)
    {
        int movement = 0;
        if (!(movement = frameDistance(PacmanMoveSpeed, data)))
            return;

        for (int step = movement >= TileSize ? TileSize - 1 : movement; movement > 0;
             movement -= step, step = movement >= TileSize ? TileSize - 1 : movement) {
            switch (direction) {
                case Up:
                    posY -= step;
                    posY += collisionWall(data, posX, posY, Up, isPlayerWalkable);
                    break;
                case Down:
                    posY += step;
                    posY -= collisionWall(data, posX, posY, Down, isPlayerWalkable);
                    break;
                case Left:
                    posX -= step;
                    posX += collisionWall(data, posX, posY, Left, isPlayerWalkable);
                    break;
                case Right:
                    posX += step;
                    posX -= collisionWall(data, posX, posY, Right, isPlayerWalkable);
                    break;
            }

            switch (collectableCheck(data, posX, posY))
            {
                case Dot:
                    score += DotPoints;
                    break;
                case Pill:
                    score += PillPoints;
                    onPillCollected(data);
                    break;
            }
            tryTurn(data);
        }
        putOnTrack(data);
    }

    void reset(const Data& data);
};

enum Mode {
    Scatter,
    Chase,
    Frightened,
    Eaten,
    ModeCount,
};

struct Ghost : public MobileObject
{
    Mode mode;
    pos target;
    pos scatter;
    pos eatenTarget;
    int frightenedTimer;
    int cagedTimer;
    bool caged;

    pos lastTurnTile;

    virtual void move(Data& data);

    void frighten()
    {
        if (mode == Eaten)
            return;
        mode = Frightened;
        reverseDirection();
        frightenedTimer = FrightenTime;
    }

    void frightenedDirection(const int& movement, const Data& data);

    void exitDirection(const Data& data);

    void pathFind(const Data&, const int&, bool(*)(const char&));


    void collidePlayer(Data& data);

    bool reachedTarget() const
    {
        int x = target.first - posX;
        int y = target.second - posY;
        return x * x + y * y < (TileSize * TileSize);
    }

    virtual void chase(const Data& data) = 0;
    virtual int getSpeed() const = 0;
//
    void reverseDirection()
    {
        switch (direction)
        {
            case Up:
                direction = Down;
                break;
            case Down:
                direction = Up;
                break;
            case Left:
                direction = Right;
                break;
            case Right:
                direction = Left;
                break;
        }
        lastTurnTile = pos(0, 0);
    }

    void putOnTrack(const Data& data)
    {
        auto tile = findTile(posX, posY);
        char type = getTileAt(tile.second, tile.first, data);
        switch (type) {
            case Path:
            case Dot:
            case Tunel:
            case Pill:
                MobileObject::putOnTrack(data);
                break;
            case Door:
            case Outside:
                switch (direction)
                {
                    case Up:
                    case Down:
                        if((int(posX) - int(tile.first * TileSize)) - int(TileSize / 2) < 0)
                            posX = tile.first * TileSize;
                        else
                            posX = (tile.first + 1) * TileSize;
                        break;
                    case Left:
                    case Right:
                        posY = tile.second * TileSize + TileSize / 2;
                        break;
                }
                break;
        }
    }
};

void Ghost::pathFind(const Data & data, const int & movement, bool (*isWalkable)(const char&))
{
    unsigned char newDirection = ::pathFind(data, posX, posY, target, direction, movement, isWalkable);
    pos tile = findTile(posX, posY);
    if (newDirection != direction && tile != lastTurnTile) {
        lastTurnTile = tile;
        direction = newDirection;
    }
}

struct Pinky : public Ghost
{
    void chase(const Data& data);

    int getSpeed() const
    {
        return GhostMoveSpeed;
    }

    void reset(const Data& data);
};

struct Clyde : public Ghost
{
    void chase(const Data& data);

    int getSpeed() const
    {
        return GhostMoveSpeed;
    }

    void reset(const Data& data);
};

struct Inky : public Ghost
{

    void chase(const Data& data);

    int getSpeed() const
    {
        return GhostMoveSpeed;
    }

    void reset(const Data& data);
};

struct Blinky : public Ghost
{
    void chase(const Data& data);

    int getSpeed() const
    {
        return GhostMoveSpeed;
    }

    void reset(const Data& data);
};

struct Data {
    int mapWidth;
    int mapHeight;
    std::string map;

    Player player;
    Inky inky;
    Blinky blinky;
    Clyde clyde;
    Pinky pinky;

    int simulationStep;
    int scatterTimer;

    pos playerStart;
    pos inkyStart;
    pos pinkyStart;
    pos blinkyStart;
    pos clydeStart;

    void lostLive()
    {
        --player.lives;

        scatterTimer = ScatterTime;
        inky.reset(*this);
        pinky.reset(*this);
        clyde.reset(*this);
        blinky.reset(*this);
        player.reset(*this);
    }
};

void Clyde::chase(const Data& data)
{
    int x = data.player.posX - posX;
    int y = data.player.posY - posY;
    if (x * x + y * y > TileSize * 8 * TileSize * 8)
        target = pos(data.player.posX, data.player.posY);
    else
        target = scatter;
}

void Inky::chase(const Data& data)
{
    pos pivot;
    switch (data.player.direction)
    {
        case Up:
            pivot = pos(data.player.posX, data.player.posY - 2 * TileSize);
            break;
        case Down:
            pivot = pos(data.player.posX, data.player.posY + 2 * TileSize);
            break;
        case Left:
            pivot = pos(data.player.posX - 2 * TileSize, data.player.posY);
            break;
        case Right:
            pivot = pos(data.player.posX + 2 * TileSize, data.player.posY);
            break;
    }
    target.first = data.blinky.posX + (pivot.first - data.blinky.posX) * 2;
    target.second = data.blinky.posY + (pivot.second - data.blinky.posY) * 2;
}

void Pinky::chase(const Data& data)
{
    switch (data.player.direction)
    {
        case Up:
            target = pos(data.player.posX, data.player.posY - 4 * TileSize);
            break;
        case Down:
            target = pos(data.player.posX, data.player.posY + 4 * TileSize);
            break;
        case Left:
            target = pos(data.player.posX - 4 * TileSize, data.player.posY);
            break;
        case Right:
            target = pos(data.player.posX + 4 * TileSize, data.player.posY);
            break;
    }
}

inline const char& getTileAt(const int& col, const int& row, const Data& data)
{
    assert((row >= 0 || col >= 0 || row < data.mapHeight || col < data.mapWidth) && "Invalid map tile (out of bounds)!");
    return data.map[col * data.mapWidth + row];
}

inline void setTileAt(const int& y, const int& x, const char & tile, Data& data)
{
    assert((x >= 0 || y >= 0 || x < data.mapWidth || y < data.mapHeight) && "Invalid map tile (out of bounds)!");
    data.map[y * data.mapWidth + x] = tile;
}

pos findTile(const int& posX, const int& posY)
{
    pos result;
    result.first  = posX / TileSize;
    result.second = posY / TileSize;
    return result;
}

bool isPacmanWalkable(const Data& data, const int & col, const int & row, bool(*isWalkable)(const char&))
{
    const char& nextTile = getTileAt(col, row, data);
    return isWalkable(nextTile);
}


void availableTurns(const Data& data, const int & x, const int & y, unsigned char* directions, int& count, const unsigned char & direction, bool (*isWalkable)(const char&))
{
    pos tile = findTile(x, y);

    if (isPacmanWalkable(data, tile.second - 1, tile.first, isWalkable) && Up != direction && Down != direction)
        directions[count++] = Up;
    if (isPacmanWalkable(data, tile.second + 1, tile.first, isWalkable) && Up != direction && Down != direction)
        directions[count++] = Down;
    if (isPacmanWalkable(data, tile.second, tile.first - 1, isWalkable) && Left != direction && Right != direction)
        directions[count++] = Left;
    if (isPacmanWalkable(data, tile.second, tile.first + 1, isWalkable) && Left != direction && Right != direction)
        directions[count++] = Right;
}

const unsigned char randomTurn(const Data& data, const int& x, const int& y, const unsigned char & direction)
{
    int random = rand();
    int directionCount = 0;
    unsigned char directions[4];

    availableTurns(data, x, y, directions, directionCount, direction, isGhostWalkable);

    if (!directionCount)
        return direction;
    return directions[random % directionCount];
}

int collisionWall(const Data& data, const int & posX, const int & posY, const unsigned char& direction, bool(*isWalkable)(const char&))
{
    int edge;
    char tile;
    switch (direction)
    {
        case Up:
            edge = posY - (TileSize >> 1);
            tile = getTileAt(edge / TileSize, posX / TileSize, data);
            if (!isWalkable(tile))
                return (1 + (edge - 1) / TileSize) * TileSize - edge;
            break;
        case Down:
            edge = posY + (TileSize >> 1) + (TileSize & 0b1);
            tile = getTileAt(edge / TileSize, posX / TileSize, data);
            if (!isWalkable(tile))
                return edge - (edge / TileSize) * TileSize;
            break;
        case Left:
            edge = posX - (TileSize >> 1);
            tile = getTileAt(posY / TileSize, edge / TileSize, data);
            if (!isWalkable(tile))
                return (1 + (edge - 1) / TileSize) * TileSize - edge;
            break;
        case Right:
            edge = posX + (TileSize >> 1) + (TileSize & 0b1);
            tile = getTileAt(posY / TileSize, edge / TileSize, data);
            if (!isWalkable(tile))
                return edge - (edge / TileSize) * TileSize;
            break;
    }
    return 0;
}

char collectableCheck(Data& data, const int& posX, const int& posY)
{
    auto tile = findTile(posX, posY);
    switch (getTileAt(tile.second, tile.first, data))
    {
        case Dot:
            setTileAt(tile.second, tile.first, Path, data);
            return Dot;
        case Pill:
            setTileAt(tile.second, tile.first, Path, data);
            return Pill;
        default:
            return '\0';
    }
}

void Ghost::exitDirection(const Data& data)
{
    if (posX < data.blinkyStart.first)
        direction = Right;
    else if (posX > data.blinkyStart.first)
        direction = Left;
    else
        direction = Up;
}

void Ghost::collidePlayer(Data& data)
{
    int x = data.player.posX - posX;
    int y = data.player.posY - posY;
    bool collided = x * x + y * y < (TileSize * TileSize);

    if (collided) {
        switch (mode)
        {
            case Frightened:
                mode = Eaten;
                data.player.score += data.player.streak++ * GhostPoints;
                reverseDirection();
                break;
            case Scatter:
            case Chase:
                data.lostLive();
                break;
        }
    }
}

void Ghost::frightenedDirection(const int& movement, const Data& data)
{
    switch (direction)
    {
        case Up:
            if(collisionWall(data, posX, posY - movement, Up, isGhostWalkable))
                direction = randomTurn(data, posX, posY, Up);
            break;
        case Down:
            if(collisionWall(data, posX, posY + movement, Down, isGhostWalkable))
                direction = randomTurn(data, posX, posY, Down);
            break;
        case Left:
            if(collisionWall(data, posX - movement, posY, Left, isGhostWalkable))
                direction = randomTurn(data, posX, posY, Left);
            break;
        case Right:
            if (collisionWall(data, posX + movement, posY, Right, isGhostWalkable))
                direction = randomTurn(data, posX, posY, Right);
            break;
    }
}

void onPillCollected(Data& data)
{

    if (data.inky.mode != Frightened && data.pinky.mode != Frightened && data.blinky.mode != Frightened && data.clyde.mode != Frightened)
        data.player.streak = 1;
    data.inky.frighten();
    data.blinky.frighten();
    data.clyde.frighten();
    data.pinky.frighten();
}

void Player::reset(const Data& data)
{
    posX = data.playerStart.first;
    posY = data.playerStart.second;
    turn = 'U';
    MobileObject::reset(data);
}

void Blinky::reset(const Data& data)
{
    caged = false;
    posX = data.blinkyStart.first;
    posY = data.blinkyStart.second;
    frightenedTimer = 0;
    mode = Scatter;
    cagedTimer = 0;
    MobileObject::reset(data);
}

void Clyde::reset(const Data& data)
{
    caged = true;
    posX = data.clydeStart.first;
    posY = data.clydeStart.second;
    frightenedTimer = 0;
    mode = Scatter;
    cagedTimer = ClydeCagedTime;
    MobileObject::reset(data);
}

void Pinky::reset(const Data& data)
{
    caged = true;
    posX = data.pinkyStart.first;
    posY = data.pinkyStart.second;
    frightenedTimer = 0;
    mode = Scatter;
    cagedTimer = PinkyCagedTime;
    MobileObject::reset(data);
}

void Inky::reset(const Data& data)
{
    caged = true;
    posX = data.inkyStart.first;
    posY = data.inkyStart.second;
    frightenedTimer = 0;
    mode = Scatter;
    cagedTimer = InkyCagedTime;
    MobileObject::reset(data);
}

void MobileObject::reset(const Data& data)
{
    direction = char('U');
}

void Blinky::chase(const Data& data)
{
    target = pos(data.player.posX, data.player.posY);
}

void Ghost::move(Data& data)
{
    bool(*isWalkable)(const char&) = nullptr;
    int movement = 0;
    if (!(movement = frameDistance( getSpeed(), data )))
        return;
    unsigned int frameDuration = data.simulationStep;

    int scatterTimer = data.scatterTimer;
    int steps = 1 + ((movement - 1) / (TileSize - 1));
    unsigned int duration = frameDuration / steps;

    for (int step = movement >= TileSize ? TileSize - 1 : movement; movement > 0;
         movement -= step, step = movement >= TileSize ? TileSize - 1 : movement)
    {
        duration += step < TileSize - 1 ? frameDuration % steps : 0;
        if (mode == Frightened) {
            if (frightenedTimer <= 0) {
                mode = scatterTimer > 0 ? Scatter : Chase;
                data.player.streak = 1;
            }
            else
                frightenedTimer -= duration;
        }
        if (scatterTimer <= 0) {
            if (mode == Scatter) {
                mode = Chase;
                reverseDirection();
            }
        }
        else
            scatterTimer -= duration;

        if (!caged) {
            switch (mode)
            {
                case Frightened:
                    frightenedDirection(step, data);
                    isWalkable = isGhostWalkable;
                    break;
                case Scatter:
                    target = scatter;
                    pathFind(data, step, isScatterWalkable);
                    isWalkable = isScatterWalkable;
                    break;
                case Chase:
                    chase(data);
                    pathFind(data, step, isGhostWalkable);
                    isWalkable = isGhostWalkable;
                    break;
                case Eaten:
                    target = eatenTarget;
                    pathFind(data, step, isEatenWalkable);
                    isWalkable = isEatenWalkable;
                    break;
            }
        }
        else {
            target = data.blinkyStart;
            cagedTimer -= duration;
            if (cagedTimer < 0)
                exitDirection(data);
            isWalkable = isCagedWalkable;
            if (reachedTarget()) {
                caged = false;
            }
        }

        int collision;
        switch (direction) {
            case Up:
                posY -= step;
                collision = collisionWall(data, posX, posY, Up, isWalkable);
                posY += collision;
                break;
            case Down:
                posY += step;
                collision = collisionWall(data, posX, posY, Down, isWalkable);
                posY -= collision;
                break;
            case Left:
                posX -= step;
                collision = collisionWall(data, posX, posY, Left, isWalkable);
                posX += collision;
                break;
            case Right:
                posX += step;
                collision = collisionWall(data, posX, posY, Right, isWalkable);
                posX -= collision;
                break;
        }
        if (caged && collision && cagedTimer > 0)
        {
            reverseDirection();
        }
        if (mode == Eaten && reachedTarget())
        {
            caged = true;
            mode = Chase;
        }
        putOnTrack(data);
        collidePlayer(data);
    }
}

int MobileObject::frameDistance(const int& speed, const Data& data) const
{
    int movement = int(speed * (data.simulationStep / 1000.0f));
    if (movement) {
        return movement;
    }
    else
        return 0;
}

pos startLoacation(const Data& data, const char& oldChar)
{
    int start = MAP.find(oldChar);
    pos result;
    result.first = (start % data.mapWidth) * TileSize + TileSize;
    result.second = (start / data.mapWidth) * TileSize + TileSize / 2;
    return result;
}

const unsigned char pathFind(const Data& data, const int & x, const int & y, const pos & target, const unsigned char & direction, const int& movement, bool (*isWalkable)(const char&))
{
    bool mustTurn = false;
    switch (direction) {
        case Up:
            if (!(mustTurn = collisionWall(data, x, y - movement, Up, isWalkable)) && y - movement > target.second)
                return direction;
            break;
        case Down:
            if (!(mustTurn = collisionWall(data, x, y + movement, Down, isWalkable)) && y + movement < target.second)
                return direction;
            break;
        case Left:
            if (!(mustTurn = collisionWall(data, x - movement, y, Left, isWalkable)) && x - movement > target.first)
                return direction;
            break;
        case Right:
            if (!(mustTurn = collisionWall(data, x + movement, y, Right, isWalkable)) && x + movement < target.first)
                return direction;
            break;
    }

    int directionCount = 0;
    unsigned char directions[4];

    availableTurns(data, x, y, directions, directionCount, direction, isWalkable);

    if (mustTurn && directionCount == 1)
        return directions[0];

    for (int i = 0; i < directionCount; ++i)
    {
        switch (directions[i]) {
            case Up:
                if (y >= target.second)
                    return directions[i];
                break;
            case Down:
                if (y <= target.second)
                    return directions[i];
                break;
            case Left:
                if (x >= target.first)
                    return directions[i];
                break;
            case Right:
                if (x <= target.first)
                    return directions[i];
                break;
        }
    }
    return direction;
}

void update(Data& data)
{
    data.player.move(data);
    data.blinky.move(data);
    data.pinky.move(data);
    data.inky.move(data);
    data.clyde.move(data);

    if (data.scatterTimer > 0)
        data.scatterTimer -= data.simulationStep;
}

void calculateKeyPositions(Data& data)
{
    data.pinky.eatenTarget = data.pinkyStart;
    data.pinky.scatter = pos(3 * TileSize + TileSize / 2, 3 * TileSize + TileSize / 2);

    data.inky.eatenTarget = data.inkyStart;
    data.inky.scatter = pos((data.mapWidth - 3) * TileSize - TileSize / 2, (data.mapHeight - 3) * TileSize - TileSize / 2);

    data.blinky.eatenTarget = data.pinkyStart;
    data.blinky.scatter = pos((data.mapWidth - 3) * TileSize - TileSize / 2, 3 * TileSize + TileSize / 2);

    data.clyde.eatenTarget = data.clydeStart;
    data.clyde.scatter = pos(3 * TileSize + TileSize / 2, (data.mapHeight - 3) * TileSize - TileSize / 2);
}

void Player::tryTurn(const Data& data)
{
    auto tile = findTile(posX, posY);
    switch (turn)
    {
        case Up:
            if (isPacmanWalkable(data, tile.second - 1, tile.first, isPlayerWalkable)) {
                direction = turn;
            }
            break;
        case Down:
            if (isPacmanWalkable(data, tile.second + 1, tile.first, isPlayerWalkable)) {
                direction = turn;
            }
            break;
        case Left:
            if (isPacmanWalkable(data, tile.second, tile.first - 1, isPlayerWalkable)) {
                direction = turn;
            }
            break;
        case Right:
            if (isPacmanWalkable(data, tile.second, tile.first + 1, isPlayerWalkable)) {
                direction = turn;
            }
            break;
    }
}

#define DEBUG

static PyObject *PacmanError;

#define CHECK(test, error) if (!test) { PyErr_SetString(PacmanError, error); return nullptr; }

PyObject* CreatePythonListFromPos(const int& posX, const int& posY)
{
    PyObject* pPos = PyList_New(2);
    PyList_SetItem(pPos, 0, PyLong_FromLong(posX));
    PyList_SetItem(pPos, 1, PyLong_FromLong(posY));

    return pPos;
}

static PyObject* simulate(PyObject *self, PyObject *args, PyObject *keywds) {
    Data data;

    char *main_kwlist[] = {
            "Map",
            "Inky",
            "Blinky",
            "Clyde",
            "Pinky",
            "Player",
            "Board",
            nullptr
    };

    PyObject *dictMap;
    PyObject *dictInky;
    PyObject *dictBlinky;
    PyObject *dictClyde;
    PyObject *dictPinky;
    PyObject *dictPlayer;
    PyObject *dictBoard;

    int res = PyArg_ParseTupleAndKeywords(
            args,
            keywds,
            "OOOOOOO",
            main_kwlist,
            &dictMap,
            &dictInky,
            &dictBlinky,
            &dictClyde,
            &dictPinky,
            &dictPlayer,
            &dictBoard
    );

    CHECK(res, "Invalid input")

    PyObject *key = nullptr, *value = nullptr;
    Py_ssize_t pos = 0;
    int available = 0;
    PyObject* pyStr;

    while (PyDict_Next(dictMap, &pos, &key, &value)) {
        pyStr = PyUnicode_AsEncodedString(key, "utf-8", "Error ~");
        const char *key_name = PyBytes_AsString(pyStr);
        if (!strcmp(key_name, "map")) {
            data.map = PyBytes_AsString(value);
            ++available;
        }
        if (!strcmp(key_name, "width")) {
            data.mapWidth = PyLong_AsLong(value);
            ++available;
        }
        if (!strcmp(key_name, "height")) {
            data.mapHeight = PyLong_AsLong(value);
            ++available;
        }
    }

#if defined(DEBUG)
    printf("Map: %s\n", data.map.c_str());
    printf("W: %d\n", data.mapWidth);
    printf("H: %d\n", data.mapHeight);
#endif

    CHECK((available == 3), "Missing map data")

    key = nullptr, value = nullptr;
    pos = 0;
    available = 0;

    while (PyDict_Next(dictPlayer, &pos, &key, &value)) {
        pyStr = PyUnicode_AsEncodedString(key, "utf-8", "Error ~");
        const char *key_name = PyBytes_AsString(pyStr);
        if (!strcmp(key_name, "score")) {
            data.player.score = PyLong_AsLong(value);
            ++available;
        }
        if (!strcmp(key_name, "lives")) {
            data.player.lives = PyLong_AsLong(value);
            ++available;
        }
        if (!strcmp(key_name, "streak")) {
            data.player.streak = PyLong_AsLong(value);
            ++available;
        }
        if (!strcmp(key_name, "position")) {
            CHECK((PyList_Size(value) == Py_ssize_t(2)), "Invalid player pos")
            PyObject *pPosX = PyList_GetItem(value, Py_ssize_t(0));
            PyObject *pPosY = PyList_GetItem(value, Py_ssize_t(1));
            data.player.posX = PyLong_AsLong(pPosX);
            data.player.posY = PyLong_AsLong(pPosY);
            ++available;
        }
        if (!strcmp(key_name, "direction")) {
            data.player.direction = *PyBytes_AsString(value);
            ++available;
        }
        if (!strcmp(key_name, "turn")) {
            data.player.turn = *PyBytes_AsString(value);
            ++available;
        }
    }

#if defined(DEBUG)
    printf("PLAYER\n");
    printf("lives: %d\n", data.player.lives);
    printf("score: %d\n", data.player.score);
    printf("streak: %d\n", data.player.streak);
    printf("pos: [%d, %d]\n", data.player.posX, data.player.posY);
    printf("direction: %c\n", data.player.direction);
#endif

    CHECK((available == 6), "Missing player data")

    const char* ModeNames[ModeCount];
    ModeNames[Scatter]    = "Scatter";
    ModeNames[Chase]      = "Chase";
    ModeNames[Frightened] = "Frightened";
    ModeNames[Eaten]      = "Eaten";

    Ghost *ghosts[] = { &data.inky, &data.pinky, &data.blinky, &data.clyde };
    PyObject *ghostsDict[] = { dictInky, dictPinky, dictBlinky, dictClyde };
    const char* names[] = { "Inky", "Pinky", "Blinky", "Clyde" };

    for (int i = 0; i < 4; ++i)
    {
        key = nullptr, value = nullptr;
        pos = 0;
        available = 0;

        while (PyDict_Next(ghostsDict[i], &pos, &key, &value)) {
            pyStr = PyUnicode_AsEncodedString(key, "utf-8", "Error ~");
            const char *key_name = PyBytes_AsString(pyStr);
            if (!strcmp(key_name, "mode")) {
                const char* mode = PyBytes_AsString(value);
                for ( int j = 0; j < ModeCount; ++j ) {
                    if (!strcmp(mode, ModeNames[j]))
                        ghosts[i]->mode = Mode(j);
                }
                ++available;
            }
            if (!strcmp(key_name, "position")) {
                CHECK((PyList_Size(value) == Py_ssize_t(2)), "Invalid ghost pos")
                PyObject *pPosX = PyList_GetItem(value, Py_ssize_t(0));
                PyObject *pPosY = PyList_GetItem(value, Py_ssize_t(1));
                ghosts[i]->posX = PyLong_AsLong(pPosX);
                ghosts[i]->posY = PyLong_AsLong(pPosY);
                ++available;
            }
            if (!strcmp(key_name, "direction")) {
                ghosts[i]->direction = *PyBytes_AsString(value);
                ++available;
            }
            if (!strcmp(key_name, "frightened_timer")) {
                ghosts[i]->frightenedTimer = PyLong_AsLong(value);
                ++available;
            }
            if (!strcmp(key_name, "caged_timer")) {
                ghosts[i]->cagedTimer = PyLong_AsLong(value);
                ++available;
            }
            if (!strcmp(key_name, "caged")) {
                ghosts[i]->caged = PyObject_IsTrue(value);
                ++available;
            }
            if (!strcmp(key_name, "last_turn_tile")) {
                CHECK((PyList_Size(value) == Py_ssize_t(2)), "Invalid lastTurnTile pos")
                PyObject *pPosX = PyList_GetItem(value, Py_ssize_t(0));
                PyObject *pPosY = PyList_GetItem(value, Py_ssize_t(1));
                ghosts[i]->lastTurnTile.first = PyLong_AsLong(pPosX);
                ghosts[i]->lastTurnTile.second = PyLong_AsLong(pPosY);
                ++available;
            }
            if (!strcmp(key_name, "target")) {
                CHECK((PyList_Size(value) == Py_ssize_t(2)), "Invalid target pos")
                PyObject *pPosX = PyList_GetItem(value, Py_ssize_t(0));
                PyObject *pPosY = PyList_GetItem(value, Py_ssize_t(1));
                ghosts[i]->target.first = PyLong_AsLong(pPosX);
                ghosts[i]->target.second = PyLong_AsLong(pPosY);
                ++available;
            }
        }

#if defined(DEBUG)
        printf("Ghost: %s\n", names[i]);
        printf("pos: [%d, %d]/direction: %c\n", ghosts[i]->posX, ghosts[i]->posY, ghosts[i]->direction);
        printf("target: [%d, %d]\n", ghosts[i]->target.first, ghosts[i]->target.second);
        printf("frightened_timer: %d/caged_timer: %d\n", ghosts[i]->frightenedTimer, ghosts[i]->cagedTimer);
        printf("mode: %s/caged: %s\n", ModeNames[ghosts[i]->mode], ghosts[i]->caged ? "True" : "False");
#endif

        CHECK((available == 8), "Missing ghost data")
    }

    key = nullptr, value = nullptr;
    pos = 0;
    available = 0;

    while (PyDict_Next(dictBoard, &pos, &key, &value)) {
        pyStr = PyUnicode_AsEncodedString(key, "utf-8", "Error ~");
        const char *key_name = PyBytes_AsString(pyStr);
        if (!strcmp(key_name, "scatter_timer")) {
            data.scatterTimer = PyLong_AsLong(value);
            ++available;
        }
        if (!strcmp(key_name, "simulation_step")) {
            data.simulationStep = PyLong_AsLong(value);
            ++available;
        }
    }

#if defined(DEBUG)
    printf("scatterTimer: %d\n", data.scatterTimer);
    printf("simulationStep: %d\n", data.simulationStep);
#endif

    CHECK((available == 2), "Missing board data")

    data.playerStart = startLoacation(data, PlayerChar);
    data.inkyStart = startLoacation(data, InkyChar);
    data.blinkyStart = startLoacation(data, BlinkyChar);
    data.clydeStart = startLoacation(data, ClydeChar);
    data.pinkyStart = startLoacation(data, PinkyChar);
    calculateKeyPositions(data);

    srand(RandomSeed);
    update(data);

    PyObject* pResult = PyDict_New();
    CHECK(PyDict_Check(pResult), "Failed to create output dict");

    {
        PyObject *obj;
        PyObject *pMap = PyDict_New();
        CHECK(PyDict_Check(pResult), "Failed to create map dict");

        res = PyDict_SetItemString(pMap, "map", obj = PyBytes_FromString(data.map.c_str())); Py_DECREF(obj);
        res += PyDict_SetItemString(pMap, "width", obj = PyLong_FromLong(data.mapWidth)); Py_DECREF(obj);
        res += PyDict_SetItemString(pMap, "height", obj = PyLong_FromLong(data.mapHeight)); Py_DECREF(obj);

        res += PyDict_SetItemString(pResult, "Map", pMap); Py_DECREF(pMap);

        CHECK((res == 0), "Failed to set map data");
    }

    {
        PyObject *obj;
        PyObject *pPlayer = PyDict_New();
        CHECK(PyDict_Check(pPlayer), "Failed to create player dict");

        char dir[] = { char(data.player.direction), '\0' };
        res = PyDict_SetItemString(pPlayer, "direction", obj = PyBytes_FromString(dir)); Py_DECREF(obj);
        dir[0] = char(data.player.turn);
        res = PyDict_SetItemString(pPlayer, "turn", obj = PyBytes_FromString(dir)); Py_DECREF(obj);
        res += PyDict_SetItemString(pPlayer, "score", obj = PyLong_FromLong(data.player.score)); Py_DECREF(obj);
        res += PyDict_SetItemString(pPlayer, "lives", obj = PyLong_FromLong(data.player.lives)); Py_DECREF(obj);
        res += PyDict_SetItemString(pPlayer, "streak", obj = PyLong_FromLong(data.player.streak)); Py_DECREF(obj);
        res += PyDict_SetItemString(pPlayer, "position", obj = CreatePythonListFromPos(data.player.posX, data.player.posY)); Py_DECREF(obj);

        res += PyDict_SetItemString(pResult, "Player", pPlayer); Py_DECREF(pPlayer);

        CHECK((res == 0), "Failed to set player data");
    }

    for ( int i = 0; i < 4; ++i )
    {
        PyObject *obj;
        PyObject *pGhost = PyDict_New();
        CHECK(PyDict_Check(pGhost), "Failed to create ghost dict");

        const char dir[] = { char(ghosts[i]->direction), '\0' };
        res = PyDict_SetItemString(pGhost, "direction", obj = PyBytes_FromString(dir)); Py_DECREF(obj);
        res += PyDict_SetItemString(pGhost, "mode", obj = PyBytes_FromString(ModeNames[ghosts[i]->mode])); Py_DECREF(obj);
        res += PyDict_SetItemString(pGhost, "position", obj = CreatePythonListFromPos(ghosts[i]->posX, ghosts[i]->posY)); Py_DECREF(obj);
        res += PyDict_SetItemString(pGhost, "target", obj = CreatePythonListFromPos(ghosts[i]->target.first, ghosts[i]->target.second)); Py_DECREF(obj);
        res += PyDict_SetItemString(pGhost, "last_turn_tile", obj = CreatePythonListFromPos(ghosts[i]->lastTurnTile.first, ghosts[i]->lastTurnTile.second)); Py_DECREF(obj);
        res += PyDict_SetItemString(pGhost, "target", obj = CreatePythonListFromPos(ghosts[i]->target.first, ghosts[i]->target.second)); Py_DECREF(obj);
        res += PyDict_SetItemString(pGhost, "frightened_timer", obj = PyLong_FromLong(ghosts[i]->frightenedTimer)); Py_DECREF(obj);
        res += PyDict_SetItemString(pGhost, "caged_timer", obj = PyLong_FromLong(ghosts[i]->cagedTimer)); Py_DECREF(obj);
        res += PyDict_SetItemString(pGhost, "caged", ghosts[i]->caged ? Py_True : Py_False);

        res += PyDict_SetItemString(pResult, names[i], pGhost); Py_DECREF(pGhost);

        CHECK((res == 0), "Failed to set ghost data");
    }

    {
        PyObject *obj;
        PyObject *pBoard = PyDict_New();
        CHECK(PyDict_Check(pResult), "Failed to create board dict");

        res = PyDict_SetItemString(pBoard, "simulation_step", obj = PyLong_FromLong(data.simulationStep)); Py_DECREF(obj);
        res += PyDict_SetItemString(pBoard, "scatter_timer", obj = PyLong_FromLong(data.scatterTimer)); Py_DECREF(obj);

        res += PyDict_SetItemString(pResult, "Board", pBoard); Py_DECREF(pBoard);

        CHECK((res == 0), "Failed to set board data");
    }

    return pResult;
}

static PyMethodDef PythonMethods[] = {
    { "simulate", (PyCFunction)simulate, METH_VARARGS | METH_KEYWORDS, "Determine pacman board state after quantum of time." },
    { nullptr, nullptr, 0, nullptr }
};

static struct PyModuleDef pacmanmodule = {
    PyModuleDef_HEAD_INIT,
    "pacman",
    nullptr,
    -1,
    PythonMethods
};

PyMODINIT_FUNC PyInit_pacman(void)
{
    PyObject *pmodule = PyModule_Create(&pacmanmodule);

    if (pmodule == nullptr)
        return nullptr;

    PacmanError = PyErr_NewException("pacman.error", NULL, NULL);
    Py_INCREF(PacmanError);
    PyModule_AddObject(pmodule, "error", PacmanError);

    return pmodule;
}