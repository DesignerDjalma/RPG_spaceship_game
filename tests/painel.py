import pygame

def create_panel(image_path, width, height):
    # Load the image
    image = pygame.image.load(image_path).convert_alpha()
    
    # Define the sizes of the corners and the center
    maxx, maxy = 174, 65
    cenx, ceny = 74, 45
    corx, cory = 0, 0

    top_left = image.subsurface((corx, cory, cenx, ceny))
    bottom_right = image.subsurface((cenx, ceny, maxx-cenx, maxy-ceny))

    # bottom_left = image.subsurface((0, 45, 74, 45))
    # bottom_right = image.subsurface((74, 45, 174, 65))
    
    # # Calculate the areas for the center parts
    # top_center = image.subsurface((corner_width, 0, center_width, corner_height))
    # bottom_center = image.subsurface((corner_width, corner_height + center_height, center_width, corner_height))
    # left_center = image.subsurface((0, corner_height, corner_width, center_height))
    # right_center = image.subsurface((corner_width + center_width, corner_height, corner_width, center_height))
    
    # center = image.subsurface((corner_width, corner_height, center_width, center_height))

    # # Create the panel surface
    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    panel.set_alpha(120)
    # Blit the corners
    panel.blit(top_left, (0, 0))
    panel.blit(bottom_right, (74, 45))
    # panel.blit(top_right, (width - corner_width, 0))
    # panel.blit(bottom_left, (0, height - corner_height))
    # panel.blit(bottom_right, (width - corner_width, height - corner_height))

    # # Blit the center parts (tiled or stretched)
    # for x in range(corner_width, width - corner_width, center_width):
    #     panel.blit(top_center, (x, 0))
    #     panel.blit(bottom_center, (x, height - corner_height))
    
    # for y in range(corner_height, height - corner_height, center_height):
    #     panel.blit(left_center, (0, y))
    #     panel.blit(right_center, (width - corner_width, y))
    
    # for x in range(corner_width, width - corner_width, center_width):
    #     for y in range(corner_height, height - corner_height, center_height):
    #         panel.blit(center, (x, y))

    return panel

# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))

# Load and create a panel
panel_image_path = "v2/painel.png"  # Replace with your image path
panel_width = 400
panel_height = 400
panel = create_panel(panel_image_path, panel_width, panel_height)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the panel
    screen.blit(panel, (50, 50))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
