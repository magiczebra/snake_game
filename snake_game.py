import pygame
import random, time

pygame.init()

class Snake_Game:

	def __init__(self):
		
		self.speedX = 10 # one grid space per game cycle
		self.speedY = 0
		self.snake_color = (0,0,255) # blue
		self.food_color = (255,0,0) # red
		self.block_size = 9 # actual grid is 10 pixels per square, 9 is used to distinguish blocks
		self.food = (0,0)
		self.size = self.width, self.height = 600, 600 # produces 600x600 pixel screen
		self.startX = self.width / 2 // 10 * 10
		self.startY = self.height / 2 // 10 * 10
		self.snake = [(self.startX - 20, self.startY), (self.startX - 10, self.startY), (self.startX, self.startY)] # intializes snake with 3 blocks at the center
		
		self.score = 0

	def eat(self): # duplicates last block in snake, canceling out removal in move() function, increases score
				   # also returns True to trigger spawn_food() function
		if self.snake[-1] == self.food:
			self.snake.insert(0, self.snake[0])
			self.score += 1
			return True

	def check_collision(self): # checks if snake head touches any wall of the screen or itself, returns True
		if self.snake[-1][0] >= (self.width + 1) or self.snake[-1][0] <= -1 or self.snake[-1][1] >= (self.height + 1) or self.snake[-1][1] <= -1:
			return True
		for block in self.snake[:-1]:
			if self.snake[-1] == block:
				return True

	def spawn_food(self): # generates random location for food in grid, checks if that space is 
						  # already taken by the snake and calls itself
		self.food = (random.randint(0,(self.width / 10 - 1)) * 10, random.randint(0,self.height / 10 - 1) * 10)
		for block in self.snake:
			if self.food == block:
				self.spawn_food()

	def update(self, screen): # updates output to screen of snake and food
		pygame.draw.rect(screen, (0,0,0), (0,0,600,600))
		for block in self.snake:
			_block = (block[0], block[1], self.block_size, self.block_size)
			pygame.draw.rect(screen, self.snake_color, _block)
		_food = (self.food[0], self.food[1], self.block_size, self.block_size)
		pygame.draw.rect(screen, self.food_color, _food)

	def change_direction(self, event): # checks for keyboard input of arrow keys, determines x and y velocity
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.speedX = 0
				self.speedY = -10
			elif event.key == pygame.K_DOWN:
				self.speedX = 0
				self.speedY = 10
			elif event.key == pygame.K_LEFT:
				self.speedX = -10
				self.speedY = 0
			elif event.key == pygame.K_RIGHT:
				self.speedX = 10
				self.speedY = 0

	def move(self): # appends the next block in the direction the snake is going, removes the last block
		self.snake.append((self.snake[-1][0] + self.speedX, self.snake[-1][1] + self.speedY))
		self.snake.remove(self.snake[0])


# main loop

if __name__ == '__main__':
	game = Snake_Game()
	game.spawn_food()

	screen = pygame.display.set_mode(game.size)

	running = True
	while running:
		for event in pygame.event.get():
			game.change_direction(event)
			print(event)
			if event.type == pygame.QUIT:
				running = False
		game.move()
		game.update(screen)
		if game.eat():
			game.spawn_food()
			for event in pygame.event.get():
				game.change_direction(event)
				game.move()
				print(event)
			game.update(screen)
		if game.check_collision():
			running = False
		pygame.display.update()

		time.sleep(0.07) # adjust for speed at different screen sizes ( 0 for 600x600, 0.03 for 400x400 )
	

print('game over\nscore: ', game.score)
wait_for_input = input('click any key to continue')
pygame.quit()