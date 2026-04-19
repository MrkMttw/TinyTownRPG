class Button():
	"""
	Button class

	Attributes:
		self.image: image of the button
		self.x_pos: x position of the button
		self.y_pos: y position of the button
		self.font: font of the button
		self.base_color: base color of the button
		self.hovering_color: hovering color of the button
		self.text_input: text input of the button
		self.text: text of the button
		self.rect: rectangle of the button
		self.text_rect: text rectangle of the button
	"""
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		"""
		Initialize the button
		
		Args:
			image: image of the button
			pos: position of the button
			text_input: text input of the button
			font: font of the button
			base_color: base color of the button
			hovering_color: hovering color of the button
			
		Returns:
			None
		"""
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			# If no image is provided, use the text as the button
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		"""
		Update the button
		
		Args:
			screen: Pygame screen object
			
		Returns:
			None
		"""
		if self.image is not None:
			# If an image is provided, draw it
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		"""
		Check if the button is clicked
		
		Args:
			position: position of the mouse
			
		Returns:
			True if the button is clicked, False otherwise
		"""
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			# If the mouse is over the button, return True
			return True
		return False

	def changeColor(self, position):
		"""
		Change the color of the button
		
		Args:
			position: position of the mouse
			
		Returns:
			None
		"""
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			# If the mouse is over the button, change the color
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			# If the mouse is not over the button, change the color back
			self.text = self.font.render(self.text_input, True, self.base_color)