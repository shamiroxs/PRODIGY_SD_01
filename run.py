import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Temperature Conversion Program')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
LIGHT_CYAN = (150, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (150, 255, 150)
DARK_GRAY = (50, 50, 50)
HOVER_COLOR = (100, 100, 100)

FONT = pygame.font.Font(None, 32)
LABEL_FONT = pygame.font.Font(None, 24)

TEMP_MIN, TEMP_MAX = -250, 250
slider_pos = WIDTH // 2 
temp_celsius = 0

input_active = False
text_input = "0"

circle_radius = 50
circle_positions = [(150, 300), (450, 300)] #faren & kelvin

slider_dragging = False

fade_alpha = 0



def draw_text_field():
    """Draw the text field with hover effect."""
    rect_color = HOVER_COLOR if input_active else DARK_GRAY
    text_surface = FONT.render(text_input, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
    input_rect = pygame.Rect(WIDTH // 2 - 100, 30, 200, 40)

    pygame.draw.rect(screen, rect_color, input_rect)
    pygame.draw.rect(screen, WHITE, input_rect, 2)
    screen.blit(text_surface, text_rect)

def draw_instructions(temp_celsius, mouse_pos):
    """Draw instructions with hover effect and fade in/out."""
    global fade_alpha

    normal_color = (150, 150, 150)
    hover_color = (200, 200, 200)

    # Determine whether to show instructions based on temperature value
    if temp_celsius == 0:
        # fade-in effect
        if fade_alpha < 255:
            fade_alpha += 10
    else:
        # fade-out effect
        if fade_alpha > 0:
            fade_alpha -= 10

    # Skip drawing when fully transparent
    if fade_alpha == 0:
        return

    instructions = "Enter/Drag the Celsius value"

    text_surface = LABEL_FONT.render(instructions, True, hover_color if is_hovering(mouse_pos) else normal_color)
    text_surface.set_alpha(fade_alpha)  # Set transparency
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 100))

    screen.blit(text_surface, text_rect)


def is_hovering(mouse_pos):
    """Check if the mouse is hovering over the instruction text area."""
    text_rect = pygame.Rect(WIDTH // 2 - 200, 85, 400, 30)  # Approximate bounds of the text
    return text_rect.collidepoint(mouse_pos)


def draw_slider():
    """Draw the horizontal slider."""
    global slider_pos
    bar_rect = pygame.Rect(50, 150, WIDTH - 100, 5)
    pygame.draw.rect(screen, WHITE, bar_rect)
    pygame.draw.circle(screen, CYAN if not input_active else HOVER_COLOR, (slider_pos, 150), 10)


def draw_circles(fahrenheit, kelvin):
    """Draw the Fahrenheit and Kelvin result circles."""
    labels = [f"{fahrenheit:.2f} °F", f"{kelvin:.2f} K"]

    for i, (x, y) in enumerate(circle_positions):
        color = LIGHT_CYAN if i == 0 else LIGHT_GREEN
        pygame.draw.circle(screen, color, (x, y), circle_radius)
        label_surface = LABEL_FONT.render(labels[i], True, BLACK)
        label_rect = label_surface.get_rect(center=(x, y))
        screen.blit(label_surface, label_rect)


def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit."""
    return c * 9 / 5 + 32


def celsius_to_kelvin(c):
    """Convert Celsius to Kelvin."""
    return c + 273.15

clock = pygame.time.Clock()

while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(WIDTH // 2 - 100, 30, 200, 40).collidepoint(event.pos):
                input_active = True
            elif 140 <= event.pos[1] <= 160 and abs(event.pos[0] - slider_pos) <= 10:
                slider_dragging = True
                input_active = False
            else:
                input_active = False

        if event.type == pygame.MOUSEBUTTONUP:
            slider_dragging = False

        if event.type == pygame.MOUSEMOTION and slider_dragging:
            slider_pos = max(50, min(WIDTH - 50, event.pos[0]))
            temp_celsius = TEMP_MIN + ((slider_pos - 50) / (WIDTH - 100)) * (TEMP_MAX - TEMP_MIN)
            text_input = str(round(temp_celsius, 2))
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 140 <= event.pos[1] <= 160:
                slider_pos = max(50, min(WIDTH - 50, event.pos[0]))
                temp_celsius = TEMP_MIN + ((slider_pos - 50) / (WIDTH - 100)) * (TEMP_MAX - TEMP_MIN)
                text_input = str(round(temp_celsius, 2))

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                text_input = text_input[:-1]
            elif event.unicode.isdigit() or (event.unicode == '-' and len(text_input) == 0) or event.unicode == '.':
                text_input += event.unicode

            try:
                temp_celsius = float(text_input)
                slider_pos = int(50 + ((temp_celsius - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)) * (WIDTH - 100))
            except ValueError:
                pass

    # Convert temperatures
    fahrenheit = celsius_to_fahrenheit(temp_celsius)
    kelvin = celsius_to_kelvin(temp_celsius)
    
    mouse_pos = pygame.mouse.get_pos()
    
    draw_text_field()
    draw_instructions(temp_celsius, mouse_pos)
    draw_slider()
    draw_circles(fahrenheit, kelvin)

    pygame.display.flip()
    clock.tick(60)

