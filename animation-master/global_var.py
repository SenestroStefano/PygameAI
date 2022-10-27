import pygame
TITLE = "Animazioni"
# https://github.com/clear-code-projects/animation

# Valori di proporzione

Delta_Time = 2 # Delta_Time (Congliabile 1/2)
Player_proportion = 0.5 # Divisore della grandezza del giocatore

#FPS
FPS = 60 * Delta_Time

# rapporto di proporzione allo schermo NON INFERIORE AD 1
MULT = 3

# rapporto offset telecamera dello schermo MAX 40
Moff = 30

# rapporto audio del gioco
AU = 5

# rapporto musica del gioco
MU = 5

Scelta = 0

Debug = False

# Inizializzazione lista di animazione camminata
PlayerWalkingO = []
PlayerWalkingVD = []
PlayerWalkingVU = []

MonsterAngry = []

Background_Color = (12, 24, 36)

# Dimensione Schermo
DF_width = 480
DF_height = 270

screen_width = DF_width * MULT
screen_height = DF_height * MULT

# Configurazione Schermo
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption(TITLE)