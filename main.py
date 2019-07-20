import copy
import random
import pygame


# TODO
#
# Move down too fast on KEYDOWN

# Block colors and patterns
blocks = [
    {
        'color': (170, 57, 57),
        'block': [
            [
                [1, 1, 1, 1]
            ],
            [
                [1],
                [1],
                [1],
                [1],
            ]
        ]
    },

    {
        'color': (170, 107, 57),
        'block': [
            [
                [1, 1, 0],
                [0, 1, 1],
            ],
            [
                [0, 1],
                [1, 1],
                [1, 0],
            ],
        ]
    },

    {
        'color': (170, 148, 57),
        'block': [
            [
                [0, 1, 1],
                [1, 1, 0],
            ],
            [
                [1, 0],
                [1, 1],
                [0, 1],
            ],
        ]
    },

    {
        'color': (131, 161, 54),
        'block': [
            [
                [1, 1],
                [1, 1],
            ]
        ]
    },

    {
        'color': (46, 65, 114),
        'block': [
            [
                [1, 0, 0],
                [1, 1, 1],
            ],
            [
                [1, 1],
                [1, 0],
                [1, 0],
            ],
            [
                [1, 1, 1],
                [0, 0, 1],
            ],
            [
                [0, 1],
                [0, 1],
                [1, 1],
            ],
        ]
    },

    {
        'color': (67, 47, 117),
        'block': [
            [
                [0, 0, 1],
                [1, 1, 1],
            ],
            [
                [1, 0],
                [1, 0],
                [1, 1],
            ],
            [
                [1, 1, 1],
                [1, 0, 0],
            ],
            [
                [1, 1],
                [0, 1],
                [0, 1],
            ],
        ]
    },

    {
        'color': (127, 42, 104),
        'block': [
            [
                [0, 1, 0],
                [1, 1, 1],
            ],
            [
                [1, 0],
                [1, 1],
                [1, 0],
            ],
            [
                [1, 1, 1],
                [0, 1, 0],
            ],
            [
                [0, 1],
                [1, 1],
                [0, 1],
            ],
        ]
    },
]

fps = 60

# Size of a tile in pixel
tilew = 30
tileh = 30

# 2 borders on each sides
border = 2

# Size of the board in tile
gameboardw = 10
gameboardh = 20

window = None


# When a block is selected 
# it's copied in a 4x4 array 
# for manipulation like rotation

class Block:
    def __init__(self):
        self._color = (0, 0, 0)
        self._rotation = 0
        self._rotation_max = 0

        self._offset = [4, 0]

        # Selected block 
        self._block = [[0 for y in range(4)] for x in range(4)]

        # Current block with every variants
        self._blocks = []


    def __del__(self):
        pass


    # Getters and setters

    def color(self, color = None):
        if color != None:
            self._color = color
        return self._color


    def rotation(self, rotation = None):
        if rotation != None:
            self._rotation = rotation
        return self._rotation


    def rotation_max(self, rotation_max = None):
        if rotation_max != None:
            self._rotation_max = rotation_max
        return self._rotation_max


    def offset(self, offset = None, x = None, y = None):
        if x != None:
            self._offset[0] = x
        if y != None:
            self._offset[1] = y
        if offset != None:
            self._offset = offset
        return copy.copy(self._offset)


    def map(self, map = None):
        if map != None:
            self._map = map
        return self._map


    def block(self, block = None):
        if block != None:
            self._block = block
        return self._block


    def blocks(self, blocks = None):
        if blocks != None:
            self._blocks = blocks
        return self._blocks


    # Add new block
    # Default rotation is 0
    # Default offset is (0, 4)
    def new(self, blocks):
        self.__init__()

        self._color = blocks['color']
        self._rotation = 0
        self._rotation_max = len(blocks['block'])

        self._offset = [4, 0]
        self._blocks = blocks['block']

        self._block = self.rotate(self._rotation)


    # Rotate current block
    # Ask for a rotation index
    # Check rotation_max()
    def rotate(self, rotation):
        b = self._blocks[rotation]
        wlen = len(b)
        hlen = len(b)

        block = [[0 for y in range(4)] for x in range(4)]

        for y, by in enumerate(b):
            for x, bx in enumerate(by):
                block[y][x] = bx

        return block


class Tiles:
    def __init__(self):
        self._tiles = [[{'fill': False, 'color': (0, 0, 0)} for x in range(gameboardw)] for y in range(gameboardh)]


    def tile(self, x, y, fill = None, color = None):
        if fill != None or color != None:
            print ('x => ', x, ' y => ', y, 'fill => ', fill, 'color => ', color)

            self._tiles[y][x]['fill'] = fill
            self._tiles[y][x]['color'] = color

        return self._tiles[y][x]


    def tiles(self):
        return self._tiles


    def swap_row(self, irow):
        for y in range((irow - 1), -1, -1):
            self._tiles[y + 1] = copy.copy(self._tiles[y])


    def delete_row(self, irow):
        self.swap_row(irow)

        self._tiles[0] = [{'fill': False, 'color': (0, 0, 0)} for x in range(gameboardw)]


    def is_complete(self, irow):
        complete = True
        for x in range(len(self._tiles[irow])):
            tx = self._tiles[irow][x]

            if not tx['fill']:
                complete = False
                break
        return complete


class Gameboard:
    def __init__(self, window):
        self._window = window

        self._tick = 0
        self._state = 0
        self._move_tick = 0
        self._rotate_tick = 0

        self._block = Block()
        self._tiles = Tiles()

        # 0 - up
        # 1 - down
        # 2 - left
        # 3 - right
        self._direction = -1
        self._eventRotate = False

        self.test()


    def test(self):
        # self._tiles[4][19] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][18] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][4] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][5] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][6] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][0] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][2] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][2] = {'fill': True, 'color': (170, 57, 57)}
        # self._tiles[4][4] = {'fill': True, 'color': (170, 57, 57)}

        # for i in range(5, 20):
        #     self._tiles[i][4] = {'fill': True, 'color': (170, 57, 57)}
        #     self._tiles[i][5] = {'fill': True, 'color': (170, 57, 57)}
        pass


    def event(self, keys):
        self._direction = -1
        self._eventRotate = False

        for key in keys:
            if key == pygame.K_LEFT:
                self._direction = 2

            elif key == pygame.K_RIGHT:
                self._direction = 3

            elif key == pygame.K_DOWN:
                self._direction = 1

            elif key == pygame.K_SPACE:
                self._eventRotate = True


    # Render offset starts at (1, 1) to avoid the border
    def render(self):
        for y, ty in enumerate(self._tiles.tiles()):
            for x, tx in enumerate(ty):

                fx = (x + 1) * tilew
                fy = (y + 1) * tileh

                if tx['fill']:
                    pygame.draw.rect(self._window, tx['color'], pygame.Rect(fx, fy, tilew, tileh))
                    
                else:
                    pygame.draw.rect(self._window, (0, 0, 0), pygame.Rect(fx, fy, tilew, tileh))


        for y, by in enumerate(self._block.block()):
            for x, bx in enumerate(by):
                if bx != 1:
                    continue

                block_offset = self._block.offset()

                fx = (block_offset[0] + x + 1) * tilew
                fy = (block_offset[1] + y + 1) * tileh
                pygame.draw.rect(self._window, self._block.color(), pygame.Rect(fx, fy, tilew, tileh))


    def state(self):
        # State : Create a new block - Check collision on start
        if self._state == 0:
            if not self.state_new():
                self._state = 10

            else:
                self._state = 20


        # State : Game done - Quit
        elif self._state == 10:
            print ('Sorry you lost')
            return False


        # State : Play - Move
        elif self._state == 20:
            if not self.state_move():
                self._state = 30


        # Block is at end of his course
        elif self._state == 30:
            # Copy current block to the board
            self.write_block_to_board()
            self._state = 0

            # Check complete rows
            #   Check rows
            #   Swap rows if one is complete
            self.checkCompleteRow()
            
        return True


    def state_new(self):
        self.create_new_block()

        # Check collision
        # collision means no more block can in the board
        if not self.collisionDirection():
            return False

        return True


    def state_move(self):
        # Tick user event to prevent blocks to be too fast
        if self._move_tick >= 5:
            if self._direction == 1:
                if not self.moveMacro(1):
                    return False

            elif self._direction == 2:
                self.moveMacro(2)

            elif self._direction == 3:
                self.moveMacro(3)

            self._move_tick = 0


        # Tick user event to prevent blocks to be too fast
        if self._rotate_tick >= 10:
            if self._eventRotate:
                r = self._block.rotation()
                r_max = self._block.rotation_max()

                if self.collisionRotation((r + 1) % r_max):
                    self._block.rotation((r + 1) % r_max)
                    self._block.block(block = self._block.rotate((r + 1) % r_max))

            self._rotate_tick = 0


        # Every 30 ticks move down
        # 
        if self._tick == 30:
            if not self.moveMacro(1):
                return False

            self._tick = 0

        self._tick += 1
        self._move_tick += 1
        self._rotate_tick += 1

        return True


    # Create a new block base on a random number
    def create_new_block(self):
        # pick random block
        i = random.randint(0, 70) % 7

        # Re-init vars
        self._tick = 0
        self._move_tick = 0

        self._block.new(blocks[i])
    

    # Check collision for a given direction
    #
    #  
    # Return False on collision
    def collisionDirection(self, direction = -1):
        block = self._block.block()
        offset = self._block.offset()

        if direction == 0:
            pass

        # Down
        elif direction == 1:
            offset[1] += 1


        # Left
        elif direction == 2:
            offset[0] -= 1


        # Right
        elif direction == 3:
            offset[0] += 1

        return self.collision(block, offset)


    # Check collision for a rotation
    # 
    # rotate() method for Block class return a block with desired rotation
    # Offset stays unchanged
    # Return False on collision
    def collisionRotation(self, rotation):
        block = self._block.rotate(rotation)
        offset = self._block.offset()

        return self.collision(block, offset)


    # Collision calculation based on the next block offset
    # Return False on collision
    def collision(self, block, offset):
        for y, by in enumerate(block):
            for x, bx in enumerate(by):
                # If right side has a sub-block
                if bx == 1:

                    cx = offset[0] + x
                    cy = offset[1] + y

                    if cx < 0:
                        return False

                    if cy < 0:
                        return False

                    if cx > (gameboardw - 1):
                        return False

                    if cy > (gameboardh - 1):
                        return False

                    if self._tiles.tile(x = cx, y = cy)['fill']:
                        return False

        return True


    # Macro to check collision and move
    def moveMacro(self, direction):
        if self.collisionDirection(direction):
            self.move(direction)
            return True
        return False


    # Modify offset for a given direction
    # direction -> int
    # 0 - up
    # 1 - down
    # 2 - left
    # 3 - right
    def move(self, direction):
        offset = self._block.offset()

        if direction == 0:
            pass

        elif direction == 1:
            offset[1] += 1
            self._block.offset(offset = offset)

        elif direction == 2:
            offset[0] += -1
            self._block.offset(offset = offset)

        elif direction == 3:
            offset[0] += 1
            self._block.offset(offset = offset)


    def write_block_to_board(self):
        for y, by in enumerate(self._block.block()):
            for x, bx in enumerate(by):
                # If right side has a sub-block
                if bx == 1:

                    # Calcul offset of each piece of a block 
                    offset = self._block.offset()
                    cx = offset[0] + x
                    cy = offset[1] + y

                    self._tiles.tile(x = cx, y = cy, fill = True, color = self._block.color())


    def checkCompleteRow(self):
        print ('checkCompleteRow()')

        ys = []
        tiles = self._tiles.tiles()
        for y in range(gameboardh):

            if self._tiles.is_complete(y):
                print ('row ', y, ' complete')
                ys.append(y)

        if ys:
            self.swapRows(ys)


    def swapRows(self, rows):
        print ('swapRows()')

        tiles = self._tiles.tiles()
        for irow in rows: 
            self._tiles.delete_row(irow)
   

class Game:
    def __init__(self):
        self._state = 0
        self._keys_pressed = []

        self._quit = False
        self._pause = False


    def __del__(self):
        pass
        

    def init(self):
        pygame.init()

        self.window = pygame.display.set_mode((
                                            tilew * (gameboardw + border), 
                                            tileh * (gameboardh + border)))
        pygame.display.set_caption('Tetris')
        self.window.fill((162, 160, 160))

        self._gm = Gameboard(self.window)

        self._clock = pygame.time.Clock()


    def quit(self):
        pygame.quit()


    def run(self):
        self.init()
        self._state = 20

        while not self._quit:
            # Gather events
            self.event()

            # 
            # Render handle in state()
            self.state()

            # Control frame rate
            self._clock.tick(fps)

        self.quit()


    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True

            # 
            if event.type == pygame.KEYDOWN:
                self._keys_pressed.append(event.key)

            if event.type == pygame.KEYUP:
                self._keys_pressed.remove(event.key)



    def state(self):
        # State : Play game
        if self._state == 20:

            if self._quit:
                self._state = 10
            elif self._pause:
                self._state = 30

            self.state_play()

        # State : Pause game
        elif self._state == 30:

            if self._quit:
                self._state = 10
            elif not self._pause:
                self._state = 20
                pass

            self.state_pause()


    def render(self, callback):
        self.window.fill((162, 160, 160))

        callback()

        pygame.display.update()


    def state_play(self):
        for key in self._keys_pressed:
            if key == pygame.K_ESCAPE:
                self._quit = True
                return False

            if key == pygame.K_RETURN:
                self._pause = True
                return False

        self._gm.event(self._keys_pressed)
        
        if not self._gm.state():
            self._quit = True

        # self.render ask for a callback
        self.render(self._gm.render)
                    
        
    def state_pause(self):
        for key in self._keys_pressed:
            if key == pygame.K_ESCAPE:
                self._quit = True
                return False

            if key == pygame.K_RETURN:
                self._pause = False
                return False



if __name__  == '__main__':
    game = Game()
    game.run()