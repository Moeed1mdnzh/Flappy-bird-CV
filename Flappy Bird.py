import pygame,time,cv2
from menu import Menu
import random as r
from pen import Pen

class Game:
	def __init__(self):
		self.menu_object = Menu()
		self.board = self.menu_object.board
		self.birdUp = pygame.image.load("birdUp.png")
		self.birdMid = pygame.image.load("birdMid.png")
		self.birdDwn = pygame.image.load("birdDown.png") 
		self.my_pen = None
		self.bird = self.birdMid
		self.pipe = pygame.image.load("pipe_bottom.png")
		self.pipes = [[self.pipe,pygame.transform.flip(self.pipe,False,True)]]
		self.pipe_y = [[400+20,0-20]]
		self.pipe_speed = 20
		self.ground = pygame.image.load("ground.png")
		self.dead = False
		self.W,self.H = 288*3,512
		self.bird_x,self.bird_y = self.W//2,self.H//2
		self.pipe_x = [[self.W,self.W]]
		self.score = 0
		self.birds = [self.birdUp,self.birdMid,self.birdDwn]
		self.font = pygame.font.SysFont("agencyfb",100,bold=True)
		self.seconds = 2

	def get_time(self):
		time = pygame.time.get_ticks()
		return time/1000

	def display_bird(self,bird_case):
		self.board.blit(pygame.transform.rotate(bird_case,20),(self.bird_x,self.bird_y))

	def generate_pipes(self):
		self.pipes.append([self.pipe,pygame.transform.flip(self.pipe,False,True)])
		self.pipe_x.append([self.W,self.W])
		Y = r.randint(190,400)
		self.pipe_y.append([Y+20,Y-400-20])
		
	def Ground(self):
		self.board.blit(self.ground,(0,470))
		self.board.blit(self.ground,(self.W//3,470))
		self.board.blit(self.ground,((self.W//3)*2,470))

	def refresh(self):
		pygame.display.update()

	def quit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

	def remove_pipes(self):
		for index,_ in enumerate(self.pipes):
			if self.pipe_x[index][0] <= -200:
				self.pipes.remove(self.pipes[index])
				self.pipe_y.remove(self.pipe_y[index])
				self.pipe_x.remove(self.pipe_x[index])

	def display_pipes(self):
		for index,value in enumerate(self.pipes):
			for i in range(2):
				self.board.blit(value[i],(self.pipe_x[index][i],self.pipe_y[index][i]))
				self.pipe_x[index][i] -= self.pipe_speed
			if self.pipe_x[index][0] in range(self.W//3+200,self.W//3+220): self.generate_pipes()

	def Score(self):
		rendered = self.font.render(str(self.score),True,(50,50,50))
		self.board.blit(rendered,(390,20))
	
	def get_score(self):
		for index,x in enumerate(self.pipe_x):
			if self.bird_x in range(x[0],x[1]+82) and self.bird_y in range(self.pipe_y[index][1]+320,self.pipe_y[index][0]):
				self.score += 1

	def delay(self,time):
		pygame.time.delay(time)

	def display_background(self):
		self.board.blit(self.menu_object.background,(0,0))
		self.board.blit(self.menu_object.background,(self.W//3,0))
		self.board.blit(self.menu_object.background,((self.W//3)*2,0))	

	def hit_pipe(self):
		for index,x in enumerate(self.pipe_x):
			if self.bird_x in range(x[1]+12,x[1]+82) and self.bird_y in range(self.pipe_y[index][1],self.pipe_y[index][1]+330): self.dead = True
		for index,x in enumerate(self.pipe_x):
			if self.bird_x in range(x[0]+12,x[0]+82) and self.bird_y in range(self.pipe_y[index][0]-20,self.pipe_y[index][0]+320): self.dead = True
				
	def out_of_screen(self):
		if self.bird_y not in range(0,470): self.dead = True
                   
	def gameLoop(self):
		cap = cv2.VideoCapture(0)
		self.menu_object.main()
		self.my_pen = Pen(cap)
		while not self.dead:
			for bird in self.birds:
				self.bird_y = self.my_pen.main()
				self.delay(60)
				self.display_background()
				self.display_bird(bird)
				self.display_pipes()
				self.Score()
				if self.get_time() >= self.seconds:
					self.get_score()
					self.seconds += 0.490
				self.hit_pipe()
				self.Ground()
				self.out_of_screen()
				self.quit()
				self.refresh()
				self.remove_pipes()
		self.display_background()
		self.font_score = pygame.font.SysFont("agencyfb",30,bold=True)
		self.font_lose = pygame.font.SysFont("agencyfb",80,bold=True)
		rendered_score = self.font_score.render(f"Your final score : {str(self.score)}",True,(50,50,50))
		rendered_lose = self.font_lose.render("YOU LOST",True,(50,50,50))
		self.board.blit(rendered_score,(315,160))
		self.board.blit(rendered_lose,(280,70))
		self.quit()
		self.refresh()
		time.sleep(4)
		return True

def main():
	g = Game()
	g = g.gameLoop()
	if g:
		main()

if __name__ == "__main__":
	main()
