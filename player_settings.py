import pygame
import sys

# Color scheme
COLOR_BG = (40, 40, 40)
COLOR_ELEMENT = (60, 60, 60)
COLOR_ACCENT = (100, 100, 100)
COLOR_TEXT = (200, 200, 200)
COLOR_HOVER = (80, 80, 80)

# Player colors (darker matte shades)
PLAYER_COLORS = [
    (0, 32, 91),    # Navy Blue
    (109, 0, 26),   # Burgundy Red
    (181, 148, 16), # Mustard Yellow
    (0, 66, 37),    # Forest Green
    (76, 0, 92),    # Royal Purple
    (191, 87, 0),   # Burnt Orange
    (92, 64, 51),   # Chocolate Brown
    (240, 240, 240) # Off-White
]

class PlayerSettings:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.dragging = False
        self.faction_values = ["Red"] * 8  # Initial value, will be overwritten
        self.color_options = ["Red", "Green", "Blue", "Yellow", "White", "Black", "Orange"]
        self.aggression_levels = ["Defensive", "Neutral", "Offensive"]

        # Game settings state
        self.total_players = 4
        self.human_players = 1
        self.ai_players = self.total_players - self.human_players
        self.dropdown_open = False
        self.active_dropdown = None
        self.dragging_handicap = -1

        # UI positions
        self.slider_rect = pygame.Rect(20, 20, 200, 20)
        self.dropdown_rect = pygame.Rect(20, 60, 200, 30)
        self.table_rect = pygame.Rect(20, 150, 760, 400)
        self.handicap_values = [100] * 8
        self.aggression_values = ["Neutral"] * 8
        self.resource_values = ["100"] * 8  # Remove % from default values
        self.text_input_active = -1  # Add text input state

    def draw_slider(self):
        pygame.draw.rect(self.screen, COLOR_ELEMENT, self.slider_rect)
        handle_x = self.slider_rect.x + (self.total_players - 2) * (self.slider_rect.width / 6)
        pygame.draw.rect(self.screen, COLOR_ACCENT, (handle_x - 5, self.slider_rect.y - 3, 10, 26))
        label = self.font.render(f"Total Players: {self.total_players}", True, COLOR_TEXT)
        self.screen.blit(label, (self.slider_rect.x, self.slider_rect.y - 20))

    def draw_table(self):
        headers = ["Players", "Faction", "Handicap", "Aggressiveness", "Resource Bonus"]
        column_width = self.screen.get_width() // len(headers)
        color_options = ["Red", "Green", "Blue", "Yellow", "White", "Black", "Orange"]
        aggression_levels = self.aggression_levels  # Use the class property

        # Draw headers
        for i, header in enumerate(headers):
            label = self.font.render(header, True, COLOR_TEXT)
            self.screen.blit(label, (self.table_rect.x + i * column_width + 10, self.table_rect.y - 20))

        # Draw all player rows first
        for player in range(self.total_players):
            y = self.table_rect.y + 40 * player
            pygame.draw.circle(self.screen, PLAYER_COLORS[player], (self.table_rect.x + 15, y + 15), 10)
            player_type = "Human" if player < self.human_players else "AI"
            self.screen.blit(self.font.render(player_type, True, COLOR_TEXT), (self.table_rect.x + 35, y + 5))
            
            # Faction dropdown
            faction_rect = pygame.Rect(self.table_rect.x + column_width + 10, y + 5, 120, 25)
            pygame.draw.rect(self.screen, 
                COLOR_HOVER if self.active_dropdown == ("faction", player) else COLOR_ELEMENT, 
                faction_rect, border_radius=3)
            faction_text = self.font.render(self.faction_values[player], True, COLOR_TEXT)
            self.screen.blit(faction_text, (faction_rect.x + 5, faction_rect.y + 3))
            
            if self.active_dropdown == ("faction", player):
                for i, color in enumerate(self.color_options):
                    option_rect = pygame.Rect(faction_rect.x, faction_rect.y + 30 * (i + 1), faction_rect.width, 25)
                    pygame.draw.rect(self.screen, COLOR_ELEMENT, option_rect, border_radius=3)
                    option_text = self.font.render(color, True, COLOR_TEXT)
                    self.screen.blit(option_text, (option_rect.x + 5, option_rect.y + 3))

            # Handicap slider
            handicap_rect = pygame.Rect(self.table_rect.x + column_width * 2 + 10, y + 5, 100, 20)
            pygame.draw.rect(self.screen, COLOR_ELEMENT, handicap_rect)
            handle_x = handicap_rect.x + (self.handicap_values[player] - 50) * (handicap_rect.width / 100)
            pygame.draw.rect(self.screen, COLOR_ACCENT, (handle_x, handicap_rect.y, 8, 20))

            # Aggression dropdown
            aggression_rect = pygame.Rect(self.table_rect.x + column_width * 3 + 10, y + 5, 140, 25)
            pygame.draw.rect(self.screen, COLOR_ELEMENT, aggression_rect, border_radius=3)
            self.screen.blit(self.font.render(self.aggression_values[player], True, COLOR_TEXT), (aggression_rect.x + 5, aggression_rect.y + 3))
            
            if self.active_dropdown == ("aggression", player):
                for i, level in enumerate(self.aggression_levels):
                    option_rect = pygame.Rect(aggression_rect.x, aggression_rect.y + 30 * (i + 1), aggression_rect.width, 25)
                    pygame.draw.rect(self.screen, COLOR_ELEMENT, option_rect, border_radius=3)
                    option_text = self.font.render(level, True, COLOR_TEXT)
                    self.screen.blit(option_text, (option_rect.x + 5, option_rect.y + 3))

            # Resource input
            resource_rect = pygame.Rect(self.table_rect.x + column_width * 4 + 10, y + 5, 100, 25)
            pygame.draw.rect(self.screen, 
                COLOR_HOVER if self.text_input_active == player else COLOR_ELEMENT, 
                resource_rect, border_radius=3)
            # Handle empty input case
            display_text = self.resource_values[player] if self.resource_values[player] else ""
            resource_text = self.font.render(f"{display_text}%", True, COLOR_TEXT)
            self.screen.blit(resource_text, (resource_rect.x + 5, resource_rect.y + 3))

        # Draw dropdown options on top of everything
        for player in range(self.total_players):
            y = self.table_rect.y + 40 * player
            column_width = self.screen.get_width() // 5
            
            # Faction dropdown options
            if self.active_dropdown == ("faction", player):
                faction_rect = pygame.Rect(self.table_rect.x + column_width + 10, y + 5, 120, 25)
                # Draw background panel
                pygame.draw.rect(self.screen, COLOR_ELEMENT, 
                    pygame.Rect(faction_rect.x, faction_rect.y + 30, 120, len(self.color_options)*25 + 5),
                    border_radius=3)
                for i, color in enumerate(self.color_options):
                    option_rect = pygame.Rect(faction_rect.x, faction_rect.y + 30*(i+1), faction_rect.width, 25)
                    pygame.draw.rect(self.screen, COLOR_BG, option_rect, border_radius=3)
                    pygame.draw.rect(self.screen, COLOR_ACCENT, option_rect, 1, border_radius=3)  # Border
                    option_text = self.font.render(color, True, COLOR_TEXT)
                    self.screen.blit(option_text, (option_rect.x + 5, option_rect.y + 3))

            # Aggression dropdown options
            if self.active_dropdown == ("aggression", player):
                aggression_rect = pygame.Rect(self.table_rect.x + column_width * 3 + 10, y + 5, 140, 25)
                # Draw background panel
                pygame.draw.rect(self.screen, COLOR_ELEMENT,
                    pygame.Rect(aggression_rect.x, aggression_rect.y + 30, 140, len(self.aggression_levels)*25 + 5),
                    border_radius=3)
                for i, level in enumerate(self.aggression_levels):
                    option_rect = pygame.Rect(aggression_rect.x, aggression_rect.y + 30*(i+1), aggression_rect.width, 25)
                    pygame.draw.rect(self.screen, COLOR_BG, option_rect, border_radius=3)
                    pygame.draw.rect(self.screen, COLOR_ACCENT, option_rect, 1, border_radius=3)  # Border
                    option_text = self.font.render(level, True, COLOR_TEXT)
                    self.screen.blit(option_text, (option_rect.x + 5, option_rect.y + 3))

    def draw_dropdown(self):
        pygame.draw.rect(self.screen, COLOR_ELEMENT, self.dropdown_rect, border_radius=3)
        label = self.font.render(f"Humans: {self.human_players}", True, COLOR_TEXT)
        self.screen.blit(label, (self.dropdown_rect.x + 10, self.dropdown_rect.y + 5))

        if self.dropdown_open:
            for i in range(1, 9):
                option_rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + 35 * i, self.dropdown_rect.width, 30)
                pygame.draw.rect(self.screen, COLOR_ELEMENT, option_rect, border_radius=3)
                option_text = self.font.render(str(i), True, COLOR_TEXT)
                self.screen.blit(option_text, (option_rect.x + 10, option_rect.y + 5))

    def get_handicap_rect(self, player_index):
        column_width = self.screen.get_width() // 5
        return pygame.Rect(self.table_rect.x + column_width * 2 + 10, self.table_rect.y + 40 * player_index + 5, 100, 20)

    def get_faction_rect(self, player_index):
        column_width = self.screen.get_width() // 5
        return pygame.Rect(self.table_rect.x + column_width + 10, self.table_rect.y + 40 * player_index + 5, 120, 25)

    def get_aggression_rect(self, player_index):
        column_width = self.screen.get_width() // 5
        return pygame.Rect(self.table_rect.x + column_width * 3 + 10, self.table_rect.y + 40 * player_index + 5, 140, 25)

    def get_resource_rect(self, player_index):
        column_width = self.screen.get_width() // 5
        return pygame.Rect(
            self.table_rect.x + column_width * 4 + 10,
            self.table_rect.y + 40 * player_index + 5,
            100, 25
        )

    def run(self):
        running = True
        while running:
            # Check mouse state outside event loop
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if not mouse_pressed:
                self.dragging = False
                self.dragging_handicap = -1

            # Update slider positions
            if self.dragging and mouse_pressed:
                x = pygame.mouse.get_pos()[0] - self.slider_rect.x
                self.total_players = min(8, max(2, int((x / self.slider_rect.width) * 6) + 2))
            
            if self.dragging_handicap != -1 and mouse_pressed:
                player = self.dragging_handicap
                h_rect = self.get_handicap_rect(player)
                x = pygame.mouse.get_pos()[0] - h_rect.x
                self.handicap_values[player] = min(150, max(50, int((x / h_rect.width) * 100) + 50))

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle text input
                if event.type == pygame.KEYDOWN and self.text_input_active != -1:
                    current = self.resource_values[self.text_input_active]
                    if event.key == pygame.K_RETURN:
                        if not current:
                            self.resource_values[self.text_input_active] = "50"
                        else:
                            validated = min(9999, max(50, int(current)))
                            self.resource_values[self.text_input_active] = str(validated)
                        self.text_input_active = -1
                    elif event.key == pygame.K_BACKSPACE:
                        self.resource_values[self.text_input_active] = current[:-1] or ""
                    elif event.unicode.isdigit():
                        new_val = (current + event.unicode).lstrip('0') or '0'
                        self.resource_values[self.text_input_active] = new_val
                
                # Handle mouse clicks (SINGLE EVENT BLOCK)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Next button check - SINGLE DEFINITION
                    button_rect = pygame.Rect(self.screen.get_width() - 120, self.screen.get_height() - 60, 100, 40)
                    if button_rect.collidepoint(event.pos):
                        print("Next button clicked")

                    # Remove these duplicate blocks below
                    self.text_input_active = -1
                    
                    # First handle existing dropdown selections
                    handled = False
                    if self.active_dropdown:
                        p = self.active_dropdown[1]
                        if self.active_dropdown[0] == "faction":
                            faction_rect = self.get_faction_rect(p)
                            for i, color in enumerate(self.color_options):
                                option_rect = pygame.Rect(faction_rect.x, faction_rect.y + 30*(i+1), faction_rect.width, 25)
                                if option_rect.collidepoint(event.pos):
                                    self.faction_values[p] = color
                                    self.active_dropdown = None
                                    handled = True
                        elif self.active_dropdown[0] == "aggression":
                            aggression_rect = self.get_aggression_rect(p)
                            for i, level in enumerate(self.aggression_levels):
                                option_rect = pygame.Rect(aggression_rect.x, aggression_rect.y + 30*(i+1), aggression_rect.width, 25)
                                if option_rect.collidepoint(event.pos):
                                    self.aggression_values[p] = level
                                    self.active_dropdown = None
                                    handled = True
                    
                    # Only process new clicks if not handled
                    if not handled:
                        # Existing click handling code (slider, dropdown, etc)
                        if self.slider_rect.collidepoint(event.pos):
                            self.dragging = True
                        
                        # Human dropdown
                        if self.dropdown_rect.collidepoint(event.pos):
                            self.dropdown_open = not self.dropdown_open
                        elif self.dropdown_open:
                            for i in range(1, 9):
                                option_rect = pygame.Rect(
                                    self.dropdown_rect.x,
                                    self.dropdown_rect.y + 35 * i,
                                    self.dropdown_rect.width,
                                    30
                                )
                                if option_rect.collidepoint(event.pos):
                                    self.human_players = i
                                    self.dropdown_open = False
                        
                        # Table interactions
                        for p in range(self.total_players):
                            faction_rect = self.get_faction_rect(p)
                            if faction_rect.collidepoint(event.pos):
                                self.active_dropdown = ("faction", p)
                                self.text_input_active = -1
                            
                            aggression_rect = self.get_aggression_rect(p)
                            if aggression_rect.collidepoint(event.pos):
                                self.active_dropdown = ("aggression", p)
                                self.text_input_active = -1
                            
                            # Resource input
                            resource_rect = self.get_resource_rect(p)
                            if resource_rect.collidepoint(event.pos):
                                self.text_input_active = p
                                self.active_dropdown = None  # Clear other dropdowns
                                # Clear default value when first clicked
                                if self.resource_values[p] == "100":
                                    self.resource_values[p] = ""
                                handled = True

                            # Handicap slider click detection
                            handicap_rect = self.get_handicap_rect(p)
                            if handicap_rect.collidepoint(event.pos):
                                self.dragging_handicap = p
                                handled = True
                                break

            # Draw everything
            self.screen.fill(COLOR_BG)
            self.draw_slider()
            self.draw_table()
            self.draw_dropdown()
            
            # Draw Next button (complete implementation)
            button_rect = pygame.Rect(
                self.screen.get_width() - 120, 
                self.screen.get_height() - 60,
                100, 
                40
            )
            pygame.draw.rect(self.screen, 
                COLOR_HOVER if button_rect.collidepoint(pygame.mouse.get_pos()) else COLOR_ELEMENT, 
                button_rect, border_radius=5)
            button_text = self.font.render("Next", True, COLOR_TEXT)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
            
            # Critical screen updates
            pygame.display.flip()
            self.clock.tick(30)
