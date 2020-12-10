import pygame
import random as r

pygame.init()

class Menu:
	def __init__(self):
		self.W,self.H = 288*3,512
		self.board = pygame.display.set_mode((self.W,self.H))
		self.caption = "Flappy Bird"
		pygame.display.set_caption(self.caption)
		self.background = pygame.image.load("background.png")
		self.pipe = pygame.image.load("pipe_bottom.png")
		self.pipes =[[self.pipe,pygame.transform.flip(self.pipe,False,True)]]
		self.pipe_x = [[0,0]]
		self.pipe_y = [[400+20,0-20]]
		self.pipe_speed = 40
		self.color = [0,0,0]
		self.pos = None
		self.Quit = False
		self.text = "start"
		self.wanted_to_change_color = True
		self.font = pygame.font.SysFont("agencyfb",100,bold=True,italic=True)
	def mouse_pos(self):
		return pygame.mouse.get_pos()
	def start_button(self):
		self.color_changer()
		rendered = self.font.render(self.text,True,self.color)
		self.board.blit(rendered,(self.W//2-120,self.H//2-100))
	def refresh(self):
		pygame.display.update()
	def color_changer(self):
		if self.color[1] != 255 and self.color[0] == 0:
			self.color[1] += 15
		elif self.color[1] == 255 and self.color[0] != 255 and self.wanted_to_change_color:
			self.color[0] += 15
		elif self.color[1] == 255 and self.color[0] <= 255 and self.color[0] >= 15:
			self.color[0] -= 15
			self.wanted_to_change_color = False
		else:
			self.wanted_to_change_color = True
	def display_pipes(self):
		for index,value in enumerate(self.pipes):
			for i in range(2):
				self.board.blit(value[i],(self.pipe_x[index][i],self.pipe_y[index][i]))
				self.pipe_x[index][i] += self.pipe_speed
			if self.pipe_x[index][0] in range(self.W//3,self.W//3+40): self.new_pipe()
	def remove_pipe(self):
		for index,_ in enumerate(self.pipes):
			if self.pipe_x[index][0] >= self.W+200:
				self.pipes.remove(self.pipes[index])
				self.pipe_y.remove(self.pipe_y[index])
				self.pipe_x.remove(self.pipe_x[index])
	def new_pipe(self):
		self.pipes.append([self.pipe,pygame.transform.flip(self.pipe,False,True)])
		self.pipe_x.append([0,0])
		Y = r.randint(190,400)
		self.pipe_y.append([Y+20,Y-400-20])
	def quit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					if self.pos[0] in range(300,540) and self.pos[1] in range(170,280):
						self.Quit = True
	def mouse_click(self):
		self.pos = self.mouse_pos()
		if self.pos[0] in range(300,540) and self.pos[1] in range(150,280):
			pygame.draw.rect(self.board,self.color,(300,170,240,110),6)
	def delay(self,time):
		pygame.time.delay(time)
	def fill(self):
		self.board.blit(self.background,(0,0))
		self.board.blit(self.background,(self.W//3,0))
		self.board.blit(self.background,((self.W//3)*2,0))
	def main(self):
		while not self.Quit:
			self.delay(50)
			self.fill()
			self.display_pipes()
			self.start_button()
			self.mouse_click()
			self.quit()
			self.refresh()
			self.remove_pipe()
