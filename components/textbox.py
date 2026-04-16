import pygame


class TextBox:
    """
    Text box class

    Attributes:
            self.image: image of the text box
            self.x_pos: x position of the text box
            self.y_pos: y position of the text box
            self.font: font of the text box
            self.base_color: base color of the text box
            self.hovering_color: hovering color of the text box
            self.text_input: text input of the text box
            self.text: text of the text box
            self.box_color: box color of the text box
            self.border_color: border color of the text box
            self.border_width: border width of the text box
            self.active: active state of the text box
            self.txt_surface: text surface of the text box
            self.text_rect: text rectangle of the text box
    """

    def __init__(
        self,
        image,
        pos,
        text_input,
        font,
        base_color,
        hovering_color,
        box_color=(255, 255, 255),
        border_color="BLACK",
        border_width=2,
        width=250,
        height=50,
    ):
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
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        if self.image is None:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill(self.box_color)
            if self.border_width > 0:
                pygame.draw.rect(
                    self.image,
                    self.border_color,
                    self.image.get_rect(),
                    self.border_width,
                )
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.txt_surface = self.font.render(self.text, True, self.base_color)
        self.text_rect = self.txt_surface.get_rect(
            midleft=(self.rect.x + 8, self.rect.centery)
        )

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
            self.text_rect = self.txt_surface.get_rect(
                midleft=(self.rect.x + 8, self.rect.centery)
            )
        return None

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

        display_text = self.text
        if self.active:
            if pygame.time.get_ticks() - self.cursor_timer > 500:
                self.cursor_timer = pygame.time.get_ticks()
                self.cursor_visible = not self.cursor_visible
            if self.cursor_visible:
                display_text += "|"

        if display_text:
            txt_surface = self.font.render(display_text, True, self.base_color)
            text_rect = txt_surface.get_rect(
                midleft=(self.rect.x + 8, self.rect.centery)
            )
            screen.blit(txt_surface, text_rect)

    def get_text(self):
        return self.text
