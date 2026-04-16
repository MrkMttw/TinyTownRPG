import pygame
 
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


class TextBox():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, box_color=(255, 255, 255), border_color="BLACK", border_width=2, width=250, height=50):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color = base_color
		self.hovering_color = hovering_color
		self.text_input = text_input
		self.text = text_input
		self.box_color = box_color
		self.border_color = border_color
		self.border_width = border_width
		self.active = False
		if self.image is None:
			self.image = pygame.Surface((width, height), pygame.SRCALPHA)
			self.image.fill(self.box_color)
			if self.border_width > 0:
				pygame.draw.rect(self.image, self.border_color, self.image.get_rect(), self.border_width)
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.txt_surface = self.font.render(self.text, True, self.base_color)
		self.text_rect = self.txt_surface.get_rect(midleft=(self.rect.x + 8, self.rect.centery))

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.active = self.rect.collidepoint(event.pos)
			return None
		if event.type == pygame.KEYDOWN and self.active:
			if event.key == pygame.K_RETURN:
				return self.text
			elif event.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]
			else:
				self.text += event.unicode
			self.txt_surface = self.font.render(self.text, True, self.base_color)
			self.text_rect = self.txt_surface.get_rect(midleft=(self.rect.x + 8, self.rect.centery))
		return None

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		if self.text:
			screen.blit(self.txt_surface, self.text_rect)

	def get_text(self):
		return self.text
