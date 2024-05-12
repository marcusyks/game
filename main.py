import pygame
import random

"""
Game Constants
"""
PLAYER_SIZE = 40
CAPTION = "I'm Bored Game"
DURATION = 30
SCREEN_SIZE = (1280, 720)
BOUNDARY = PLAYER_SIZE*3
PLAYABLE_X = (BOUNDARY,1280-BOUNDARY)
PLAYABLE_Y = (BOUNDARY,720-BOUNDARY)
MOVEMENT_SPEED = 300
BLOCK_SIZE = 10

"""
    Class that handles all the game logic: points, generation of point blocks, update player size and speed etc.
"""
class GameLogic():
    def __init__(self, playable_x, playable_y, block_size, player_size, main_instance):

        """
        Constructor for class GameLogic

        Args:
            playable_x (tuple): Playable x axis coordinates of the screen
            playable_y (tuple): Playable x axis coordinates of the screen
            block_size (int): Size of each point block
            player_size (float): Player's size
            main_instance (GameHandler class): Instance of GameHandler -> for child to parent data transfer
        """

        self.points = 0
        self.block_size = block_size
        self.playable_x = playable_x
        self.playable_y = playable_y
        self.player_size = player_size
        self.main_instance = main_instance
        self.blocks = self.generate_blocks()

    def update_size(self):

        """
        Function that updates size and speed and passes it back to GameHandler
        """

        self.player_size -= .2
        self.main_instance.update_player(.2,2)

    def collision_detect(self, player_pos):

        """
        Function that checks whether point blocks collides with player

        Args:
            player_pos (tuple): Player's current position (x,y)
        """

        for block_pos in self.blocks:
            if (player_pos[0] + self.player_size > block_pos[0] and
                player_pos[0] - self.player_size < block_pos[0] + self.block_size and
                player_pos[1] + self.player_size > block_pos[1] and
                player_pos[1] - self.player_size < block_pos[1] + self.block_size):
                self.blocks.remove(block_pos)
                self.points += 1
                self.update_size()

    def generate_blocks(self):

        """
        Function that generates all point blocks

        Returns:
            List[List[x,y]]: A list of lists with x and y coordinates of each block
        """

        block_positions = []
        for _ in range(10):
            x = random.randint(self.playable_x[0], self.playable_x[1] - self.block_size)
            y = random.randint(self.playable_y[0], self.playable_y[1] - self.block_size)
            block_positions.append([x, y])
        return block_positions

    def get_block_size(self):

        """
        Getter function for block_size

        Returns:
            int: Point block size
        """

        return self.block_size

    def get_blocks(self):

        """
        Getter function that gets blocks coordinates

        Returns:
            List[List[x,y]]: A list of lists with x and y coordinates of each block
        """

        if len(self.blocks) == 0:
            self.blocks = self.generate_blocks()
        return self.blocks

    def get_points(self):

        """
        Getter function that gets points accumulated

        Returns:
            int: Total amount of points accumulated
        """

        return self.points


"""
    Class that handles all UI and acts as the view of the game
"""
class ScreenHandler():
    def __init__(self, screen, player_size):

        """
        Constructor for ScreenHandler class

        Args:
            screen (tuple): Screen dimension
            player_size (float): Player's size
        """

        self.player_size = player_size
        self.screen = screen

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

    def draw_timer(self, text):

        """
        Function that draws time counter

        Args:
            text (str): Time counter text
        """

        font = pygame.font.SysFont('Consolas', 30)
        self.screen.blit(font.render(text, True, "black"), (self.player_size/4,self.player_size/2))

    def draw_game_arena(self):

        """
        Function that draws the playable game arena
        """

        bounding_box = pygame.Rect(2*self.player_size, 2*self.player_size, self.width-4*self.player_size, self.height-4*self.player_size)
        pygame.draw.rect(self.screen, "black", bounding_box, 10)

    def draw_player(self, player_pos, player_size):

        """
        Function that draws player

        Args:
            player_pos (tuple): Player's current coordinates
            player_size (float): Player's size
        """

        pygame.draw.circle(self.screen, "black", player_pos, player_size-10)

    def draw_points(self, text):

        """
        Function that draws points counter

        Args:
            text (str): Point counter text
        """

        font = pygame.font.SysFont('Consolas', 30)
        self.screen.blit(font.render(text, True, "black"), (self.player_size/4,self.height - self.player_size))

    def draw_blocks(self, blocks, block_size):

        """
        Function that draws point blocks

        Args:
            blocks (List[List[x,y]]): A list of lists with x and y coordinates of each block
            block_size (int): Size of point block
        """

        for block_pos in blocks:
            pygame.draw.rect(self.screen, "black", (block_pos[0], block_pos[1], block_size, block_size))

    def draw_text(self, string, type, center):

        """
        Function that draws texts on screen

        Args:
            string (str): Text to be displayed
            type (str): Type of text (Title, paragraph etc)
            center (tuple): Coordinates of the text
        """

        button_color = "black"

        if type == 'title':
            title_font = pygame.font.SysFont('Consolas', 60)
            title_text = title_font.render(string, True, button_color)
            title_rect = title_text.get_rect(center=center)
            self.screen.blit(title_text, title_rect)

        elif type == 'paragraph':
            font = pygame.font.SysFont('Consolas', 30)
            p_text = font.render(string, True, button_color)
            p_rect = p_text.get_rect(center=center)
            self.screen.blit(p_text, p_rect)




"""
    Class that handles all movement related variables
"""
class MovementHandler():
    def __init__(self,speed,playable_x,playable_y):

        """
        Constructor of MovementHandler class

        Args:
            speed (int): Player's movement speed
            playable_x (tuple): Playable x-axis coordinates on the screen
            playable_y (tuple): Playable y_axis coordinates on the screen
        """

        self.speed = speed
        self.playable_x = playable_x
        self.playable_y = playable_y

    def is_out_of_bound(self,position,direction,player_size):

        """
        Function that checks if player is out of bounds

        Args:
            position (Vector2): Coordinates of player position
            direction (string): Direction at which the player is going

        Returns:
            bool : player is out of bounds
        """

        if direction == "left":
            return False if position.x > self.playable_x[0] else True
        elif direction == "right":
            return False if position.x < self.playable_x[1] else True
        if direction == "up":
            return False if position.y > self.playable_y[0] else True
        elif direction == "down":
            return False if position.y < self.playable_y[1] else True

    def perform_movement(self,keys,position,dt, player_size):

        """
        Function that performs movement on player

        Args:
            keys (ScancodeWrapper): Dictionary of all keys
            position (Vector2): Coordinates of player position
            dt (int): Time elapsed between current and previous frame
        """

        if keys[pygame.K_LEFT]:
            if not self.is_out_of_bound(position, "left", player_size):
                position.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            if not self.is_out_of_bound(position, "right", player_size):
                position.x += self.speed * dt
        if keys[pygame.K_UP]:
            if not self.is_out_of_bound(position, "up", player_size):
                position.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            if not self.is_out_of_bound(position, "down", player_size):
                position.y += self.speed * dt

    def update_movement(self, new_speed):
        self.speed = new_speed


"""
    Class that handles all scenes and acts as a controller
"""
class GameHandler():
    def __init__(self, player_size, caption, duration, boundary, playable_x, playable_y, block_size, movement_speed):

        """
        Constructor of GameHandler class

        Args:
            player_size (float): Player's size
            caption (str): Caption of the game
            duration (int): Duration of the game
            boundary (int): Boundary of the game arena
            playable_x (tuple): Playable x-axis coordinates on the screen
            playable_y (tuple): Playable y_axis coordinates on the screen
            block_size (int): Size of each point block
            movement_speed (int): Player's movement speed
        """

        self.default_speed = movement_speed
        self.default_size = player_size

        self.player_size = player_size
        self.caption = caption
        self.duration = duration
        self.boundary = boundary
        self.playable_x = playable_x
        self.playable_y = playable_y
        self.block_size = block_size
        self.movement_speed = movement_speed
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))

        self.screen_handler = ScreenHandler(self.screen, self.player_size)
        self.game_logic = None
        self.movement_handler = None

    def update_player(self, size, speed):

        """
        Function that updates player's size and speed as points increase

        Args:
            size (float): Player's size
            speed (int): Player's movement speed
        """

        self.movement_speed -= speed
        self.player_size -= size
        self.movement_handler.update_movement(self.movement_speed)

    def start_guide(self):

        """
        Guide scene for the game
        """
        pygame.display.set_caption(self.caption)
        self.screen.fill((255, 255, 255))

        title_text = "Guide"
        title_pos = (self.screen.get_width() / 2, 200)

        guide_text = "- Collect as many blocks as possible within 30 seconds."
        guide_pos = (self.screen.get_width() / 2, self.screen.get_height() - 400)

        guide_text2 = "- Use UP, DOWN, LEFT, RIGHT keys to move."
        guide_pos2 = (self.screen.get_width() / 2, self.screen.get_height() - 350)

        caution_text = "- CAUTION: You will get smaller and slower as time passes"
        caution_pos = (self.screen.get_width() / 2, self.screen.get_height() - 300)

        back_text = "[M] to go back to menu"
        back_pos = (self.screen.get_width() / 2, self.screen.get_height() - 100)

        # Check for events
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        self.start_game()
                    if keys[pygame.K_m]:
                        self.start_menu()

            # Redraw the button
            self.screen.fill((255, 255, 255))
            self.screen_handler.draw_text(title_text,"title",title_pos)
            self.screen_handler.draw_text(guide_text,"paragraph",guide_pos)
            self.screen_handler.draw_text(guide_text2,"paragraph",guide_pos2)
            self.screen_handler.draw_text(caution_text,"paragraph",caution_pos)
            self.screen_handler.draw_text(back_text,"paragraph",back_pos)

            # Update the display
            pygame.display.flip()

    def start_menu(self):

        """
        Starting scene for the game (menu)
        """

        pygame.init()

        pygame.display.set_caption(self.caption)
        self.screen.fill((255, 255, 255))

        title_text = "I'm Bored Game"
        title_pos = (self.screen.get_width() / 2, 200)

        start_text = "[Spacebar] to start game"
        start_pos = (self.screen.get_width() / 2, self.screen.get_height() - 300)

        guide_text = "[G] for guide"
        guide_pos = (self.screen.get_width() / 2, self.screen.get_height() - 200)

        # Check for events
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        self.start_game()
                    if keys[pygame.K_g]:
                        self.start_guide()

            # Redraw the button
            self.screen.fill((255, 255, 255))
            self.screen_handler.draw_text(title_text,"title",title_pos)
            self.screen_handler.draw_text(start_text,"paragraph",start_pos)
            self.screen_handler.draw_text(guide_text,"paragraph",guide_pos)

            # Update the display
            pygame.display.flip()


    def start_game(self):

        """
        Function that starts the game
        """

        self.player_size = self.default_size
        self.movement_speed = self.default_speed

        self.screen_handler = ScreenHandler(self.screen, self.player_size)
        self.game_logic = GameLogic(self.playable_x,self.playable_y,self.block_size, self.player_size, self)
        self.movement_handler = MovementHandler(self.movement_speed, self.playable_x,self.playable_y)

        width, height = self.screen.get_width(), self.screen.get_height()
        clock = pygame.time.Clock()
        dt = 0

        pygame.display.set_caption(self.caption)
        player_pos = pygame.Vector2(width / 2, height - self.boundary)

        time_counter, time_text = self.duration, f'Time Left: {str(self.duration)}'
        points_text = f'Points: {str(0)}'
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.USEREVENT:
                    time_counter -= 1
                    time_text = f'Time Left: {str(time_counter)}'
                    if time_counter == 0:
                        self.game_over(self.game_logic.get_points())

            # fill the screen with a color to wipe away anything from last frame
            points_text = f'Points: {self.game_logic.get_points()}'
            self.screen.fill("white")
            self.screen_handler.draw_player(player_pos, self.player_size)
            self.screen_handler.draw_game_arena()
            self.screen_handler.draw_points(points_text)
            self.screen_handler.draw_timer(time_text)
            self.screen_handler.draw_blocks(self.game_logic.get_blocks(),self.game_logic.get_block_size())

            keys = pygame.key.get_pressed()
            self.movement_handler.perform_movement(keys,player_pos,dt,self.player_size)
            self.game_logic.collision_detect(player_pos)

            # RENDER YOUR GAME HERE

            # flip() the display to put your work on screen
            pygame.display.flip()

            dt = clock.tick(60) / 500

    def game_over(self, points):

        """
        Displayed scene when game is over

        Args:
            points (int): Amount of points accumulated over the game
        """

        pygame.init()

        pygame.display.set_caption(self.caption)
        self.screen.fill((255, 255, 255))

        title_text = "Game Over!"
        title_pos = (self.screen.get_width() / 2, 200)

        points_text = f"Points: {self.game_logic.get_points()}"
        points_pos = (self.screen.get_width() / 2, self.screen.get_height() - 400)

        restart_text = "[R] to restart"
        restart_pos = (self.screen.get_width() / 2, self.screen.get_height() - 250)

        menu_text = "[M] to go back to menu"
        menu_pos = (self.screen.get_width() / 2, self.screen.get_height() - 200)

        # Check for events
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_r]:
                        self.start_game()
                    if keys[pygame.K_m]:
                        self.start_menu()

            # Redraw the button
            self.screen_handler.draw_text(title_text,"title",title_pos)
            self.screen_handler.draw_text(points_text,"paragraph",points_pos)
            self.screen_handler.draw_text(restart_text,"paragraph",restart_pos)
            self.screen_handler.draw_text(menu_text,"paragraph",menu_pos)

            # Update the display
            pygame.display.flip()

    def leaderboard(self):
        # Read txt file
        # See if score is higher than current highscore -> display text and update txt
        # Else display current highscore
        pass

if __name__ == "__main__":
    game_handler = GameHandler(PLAYER_SIZE,CAPTION,DURATION,BOUNDARY,PLAYABLE_X,PLAYABLE_Y,BLOCK_SIZE,MOVEMENT_SPEED)
    game_handler.start_menu()
