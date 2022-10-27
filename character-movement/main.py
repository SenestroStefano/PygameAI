"""Smooth Movement in pygame"""

#Imports
import pygame, sys, random, os, re
import global_var as GLOB
import giocatore

#pygame initialization
pygame.init()
clock = pygame.time.Clock()

def get_font(size):
    return pygame.font.Font("freesansbold.ttf", size)

#Debug Class
class Debug():
    def log(self, flag):

        if flag:
            
            pygame.draw.rect(GLOB.screen, (255,255,255), player.rect, int(1*GLOB.MULT))
            keys_pressed = pygame.key.get_pressed()

            key = ""

            if player.getUpPress():
                key = "up"
            elif player.getDownPress():
                key = "down"
            elif player.getLeftPress():
                key = "left"
            elif player.getRightPress():
                key = "right"
            
            FPS_TEXT = get_font(8*int(GLOB.MULT)).render("FPS: "+str(int(clock.get_fps())), True, "white")
            FPS_RECT = FPS_TEXT.get_rect(center=(GLOB.screen_width-40*GLOB.MULT, 20*GLOB.MULT))

            DROP_TEXT = get_font(5*int(GLOB.MULT)).render("DROP "+str(100-int(clock.get_fps()*100/GLOB.FPS))+"%", True, "red")
            DROP_RECT = DROP_TEXT.get_rect(center=(GLOB.screen_width-95*GLOB.MULT, 20*GLOB.MULT))

            KEY_TEXT = get_font(10*int(GLOB.MULT)).render(key, True, "blue")
            KEY_RECT = KEY_TEXT.get_rect(center=(GLOB.screen_width-140*GLOB.MULT, 20*GLOB.MULT))


            GLOB.screen.blit(KEY_TEXT, KEY_RECT)

            if int(clock.get_fps()) <= (GLOB.FPS-(GLOB.FPS/20)):
                #print("Gli fps sono scesi: "+str(clock.get_fps()))
                GLOB.screen.blit(DROP_TEXT, DROP_RECT)
                

            GLOB.screen.blit(FPS_TEXT, FPS_RECT)

            if keys_pressed[pygame.K_o]:
                GLOB.Moff -= 1

            if keys_pressed[pygame.K_p]:
                GLOB.Moff += 1

            RUN_TEXT = get_font(8*int(GLOB.MULT)).render("V-A: "+str(round(GLOB.Player_speed, 1)), True, "white")
            RUN_RECT = RUN_TEXT.get_rect(center=(40*GLOB.MULT, 20*GLOB.MULT))

            GLOB.screen.blit(RUN_TEXT, RUN_RECT)

            POS_TEXT = get_font(8*int(GLOB.MULT)).render("x/y: "+str(int(player.getPositionX()-cam.getPositionX()))+" | "+str(int(player.getPositionY()-cam.getPositionY())), True, "Blue")
            POS_RECT = POS_TEXT.get_rect(center=(200*GLOB.MULT, 20*GLOB.MULT))

            GLOB.screen.blit(POS_TEXT, POS_RECT)

            MOS_TEXT = get_font(8*int(GLOB.MULT)).render("x/y: "+str(int(mostro.x))+" | "+str(int(mostro.y)), True, "Red")
            MOS_RECT = MOS_TEXT.get_rect(center=(200*GLOB.MULT, 50*GLOB.MULT))

            GLOB.screen.blit(MOS_TEXT, MOS_RECT)


#Delay

class Delay():
    def __init__(self, sec, event):
        self.__min = 0
        self.__max = sec * GLOB.FPS
        self.__increment = 1
        self.__function = event
        self.__flag = True
        self.__times = 0

    # | Avvia il delay -> Poi si interromperà |
    def Start(self):
        if self.__flag:
            self.__min += self.__increment

            if int(self.__min) >= self.__max:
                self.__function()
                self.__flag = False

    # | Restarta il delay |
    def ReStart(self):
        if not self.__flag:
            self.__min = 0
            self.__flag = True

    # | Imposta il delay a infinito |
    def Infinite(self):
        self.ReStart()
        self.Start()

    def TotTimes(self, val):
        if self.__times <= val:
            self.ReStart()
            self.Start()
            self.__times += 1

    # | Stampa lo stato attuale del delay |
    def ActualState(self):
        print("| Current Second: %d | Max Seconds: %d | Function: %s |" %(self.__min/GLOB.FPS, self.__max/GLOB.FPS, self.__function))

#Cam Class
class Cam():
    def __init__(self):

        #indico il giocatore impostato
        self.setPositionX(0) 
        self.setPositionY(0)

        self.image = pygame.image.load("assets/BackgroundCam.png").convert()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.image = pygame.transform.scale(self.image,((self.width*GLOB.MULT*2), (self.height*GLOB.MULT*2)))


    def setPositionX(self, x):
        self.x = x

    def setPositionY(self, y):
        self.y = y

    def getPositionX(self):
        return self.x

    def getPositionY(self):
        return self.y
    
    
    def screen_shake(self):
        intervallo = 5
        self.y = self.y + random.randint(-intervallo, intervallo)

        
    def update(self, visibility):
        GLOB.screen.blit(self.image, (self.x, self.y))

        offset = (4 * GLOB.Moff * GLOB.MULT, 2.25 * GLOB.Moff * GLOB.MULT)

        a =  player.getPositionX() >= GLOB.screen_width - offset[0] - player.width
        b =  player.getPositionX() <= offset[0]

        c =  player.getPositionY() >= GLOB.screen_height - offset[1] - player.height
        d =  player.getPositionY() <= offset[1]

        a1 = player.getRightPress()
        b1 = player.getLeftPress()

        c1 = player.getDownPress()
        d1 = player.getUpPress()

        ln = player.Last_keyPressed=="Null"

        if a and ln and not (player.getLeftPress() or player.getRightPress()):
            player.x -= GLOB.Player_default_speed

        if b and ln and not (player.getLeftPress() or player.getRightPress()):
            player.x += GLOB.Player_default_speed

        if c and ln and not (player.getUpPress() or player.getDownPress()):
            player.y -= GLOB.Player_default_speed

        if d and ln and not (player.getUpPress() or player.getDownPress()):
            player.y += GLOB.Player_default_speed

        if a and a1 or ln and a:
            player.setPositionX(player.getPositionX()-player.getVelocitaX())
            self.x -= player.getVelocitaX()
            # print("Cam-destra")
    

        if b and b1 or ln and b:
            player.setPositionX(player.getPositionX()-player.getVelocitaX())
            self.x += -player.getVelocitaX()
            # print("Cam-sinistra")


        if c and c1 or ln and c:
            player.setPositionY(player.getPositionY()-player.getVelocitaY())
            self.y -= player.getVelocitaY()
            # print("Cam-basso")
    

        if d and d1 or ln and d:
            player.setPositionY(player.getPositionY()-player.getVelocitaY())
            self.y += -player.getVelocitaY()
            # print("Cam-alto")
        
        if visibility:

            Player_hitbox = [ 0, 0, player.width * GLOB.MULT /GLOB.Player_proportion, player.height * GLOB.MULT /GLOB.Player_proportion]
            #Player_hitbox = player.rect

            Offset_rect = pygame.Rect(offset[0] + Player_hitbox[0], offset[1] + Player_hitbox[1], GLOB.screen_width - offset[0]*2 - Player_hitbox[0]*2, GLOB.screen_height - offset[1]*2 - Player_hitbox[1]*2)
            pygame.draw.rect(GLOB.screen, (255,255,255), Offset_rect, int(GLOB.MULT))
        
        #print("Posizione x: "+str(player.getPositionX())+" | Posizione y: "+str(player.getPositionY())+" | VelocitàX: "+str(player.getVelocitaX()))

class Mostro():
    def __init__(self, pos, vel, wh):
        self.x = pos[0]
        self.y = pos[1]
        self.width = wh[0]
        self.height = wh[1]
        self.default_height = self.height
        self.vel = vel * GLOB.MULT / GLOB.Delta_Time
        self.x, self.y = GLOB.screen.get_rect().center
        self.line_vector = pygame.math.Vector2(1, 0)
        self.angle = 90

        self.default_speed = self.vel

        self.monster_ai_vel = 0.5
        self.default_monster_ai_vel = self.monster_ai_vel
        self.monster_ai_brain = 0
        self.delay_monster = Delay(self.monster_ai_vel, self.__setBrain)
        self.Last_keyPressed = "Null"

        self.distanza = 90

        self.color_triangle = (255, 0, 0)

        self.altezza_rect = 20 * GLOB.MULT

        self.aggr = False

        self.direzione = ""

        self.flag_CanAttack = False
        self.flag_CanStartAttack = False

        self.valore_distanza = 220 * GLOB.MULT
        self.setHitbox()

        self.__left_pressed = False
        self.__right_pressed = False
        self.__up_pressed = False
        self.__down_pressed = False

        self.superfice = pygame.Surface((GLOB.screen_width, GLOB.screen_height))        
        
        self.current_spriteWO = 0
        self.current_spriteWVU = 0
        self.current_spriteWVD = 0
        self.current_spriteAngry = 0
        
        self.Name_animationWVD = Folder_walkVD
        self.Name_animationWVU = Folder_walkVU
        self.Name_animationWO = Folder_walkO
        self.Name_animationAngry = Folder_angry
        
        self.character_update(3)
        
        self.char_w, self.char_h = self.image.get_width() * GLOB.MULT / GLOB.Player_proportion, self.image.get_height() * GLOB.MULT / GLOB.Player_proportion

        self.luce_image = pygame.image.load("../assets/luce.png").convert_alpha()
        self.luce_image = pygame.transform.scale(self.luce_image, (self.char_w, self.char_h))
        
        self.transparenza = 40

        self.ICollide = False
        
        

    def setHitbox(self):
        self.hitbox = (self.x + 20 * GLOB.MULT + cam.getPositionX(),  self.y + 35 * GLOB.MULT + cam.getPositionY(), 16 * GLOB.MULT, 16 * GLOB.MULT)
        self.mesh = pygame.Rect(self.hitbox)

    def __setBrain(self):
        lista_valori = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
        self.monster_ai_brain = random.choice(lista_valori)
        
    def character_update(self, c):
        
        self.current_spriteWO += 0.2 / GLOB.Delta_Time
        self.current_spriteWVD += 0.2 / GLOB.Delta_Time
        self.current_spriteWVU += 0.2 / GLOB.Delta_Time

        if c == 1:
            if self.current_spriteWO >= len( GLOB.PlayerWalkingO):
                self.current_spriteWO = 0
            
            immagine = GLOB.PlayerWalkingO[int(self.current_spriteWO)]
            self.image = pygame.image.load(Folder_walkO + "/" + immagine).convert_alpha()
    
        if c == 2:
            if self.current_spriteWO >= len(GLOB.PlayerWalkingO):
                self.current_spriteWO = 0
            
            immagine = pygame.image.load(Folder_walkO + "/" + GLOB.PlayerWalkingO[int(self.current_spriteWO)]).convert_alpha()
            immagine_flip = pygame.transform.flip(immagine, True, False)
            self.image = immagine_flip
            
        if c == 3:
            if self.current_spriteWVD >= len( GLOB.PlayerWalkingVD):
                self.current_spriteWVD = 0
            
            immagine = GLOB.PlayerWalkingVD[int(self.current_spriteWVD)]
            self.image = pygame.image.load(Folder_walkVD + "/" + immagine).convert_alpha()
            
        if c == 4:
            if self.current_spriteWVU >= len( GLOB.PlayerWalkingVU):
                self.current_spriteWVU = 0
            
            immagine = GLOB.PlayerWalkingVU[int(self.current_spriteWVU)]
            self.image = pygame.image.load(Folder_walkVU + "/" + immagine).convert_alpha()
            
        if c == 5 and not self.flag_CanStartAttack:
            
            self.monster_ai_brain = -1
            
            self.current_spriteAngry += 0.2 / GLOB.Delta_Time
            
            if self.current_spriteAngry >= len(GLOB.MonsterAngry):
                self.flag_CanStartAttack = True
                self.current_spriteAngry = 0
                
            if self.current_spriteAngry >= 7:
                cam.screen_shake()
            
            immagine = GLOB.MonsterAngry[int(self.current_spriteAngry)]
            self.image = pygame.image.load(Folder_angry + "/" + immagine).convert_alpha()
            
            
    def finish(self):
        self.current_spriteAngry = 0
        self.current_spriteWO = 0
        self.current_spriteWVU = 0
        self.current_spriteWVD = 0
        self.character_update(3)

    def aggiorna(self):
        radius = 360

        self.setHitbox()
        
        if self.monster_ai_brain:
            if self.monster_ai_brain == int(self.monster_ai_brain):
                self.character_update(self.monster_ai_brain)
            
            elif self.monster_ai_brain == 1.5 or self.monster_ai_brain == 2.5:
                self.character_update(3)
                
            elif self.monster_ai_brain == 3.5 or self.monster_ai_brain == 4.5:
                self.character_update(4)
        else:
            self.finish()

        if not self.flag_CanAttack:
            self.aggr = False

        self.line_vector = pygame.math.Vector2(self.height, 0)
        
        rot_vector = self.line_vector.rotate(self.angle) * radius
        rot_vector1 = self.line_vector.rotate(self.angle + self.distanza) * radius

        distanza = (17 * GLOB.MULT, 22 * GLOB.MULT)

        start_line = round(self.x + self.width/2 + distanza[0] + cam.getPositionX()), round(self.y + cam.getPositionY() + distanza[1])
        end_line = round(self.x + self.width/2 + distanza[0] - rot_vector.x + cam.getPositionX()), round(self.y - rot_vector.y + cam.getPositionY() + distanza[1])


        end_line1 = round(self.x + self.width/2 + distanza[0] - rot_vector1.x + cam.getPositionX()), round(self.y - rot_vector1.y + cam.getPositionY() + distanza[1])


        self.superfice.fill(pygame.SRCALPHA)

        self.triangle = pygame.draw.polygon(surface=self.superfice, color=self.color_triangle, points=[end_line, end_line1, start_line], width=0)

        self.superfice.set_alpha(self.transparenza)


        # pygame.draw.line(GLOB.screen, (5,80,255), start_line, end_line, 8)
        # pygame.draw.line(GLOB.screen, (255,80,5), start_line, end_line1, 8)

        if (self.triangle.colliderect(player.hitbox) or self.aggr) and self.flag_CanAttack:
            
            self.character_update(5)
            
            if self.flag_CanStartAttack:
                self.raggio_ai_brain = 0
                self.monster_ai_brain = 0
                self.height = 0
                self.circle = pygame.draw.circle(self.superfice, "Red", (self.x + self.image.get_width()/2 + cam.getPositionX(), self.y + cam.getPositionY() + distanza[1]), self.valore_distanza, 0)
                self.color_rect = (255, 0, 255)
                self.color_triangle = (255, 0, 0)
                self.aggr = True
                player.color = "White"

        else:
            self.height = self.default_height
            self.delay_monster.Infinite()
            self.color_triangle = (255, 0, 0)
            self.color_rect = (255, 0, 0)
            player.color = "Blue"

        self.image = pygame.transform.scale(self.image, (self.char_w, self.char_h))
        GLOB.screen.blit(self.image, (self.x + cam.getPositionX(), self.y + cam.getPositionY()))

        if self.aggr:
            GLOB.screen.blit(self.luce_image, (self.x + cam.getPositionX(), self.y + cam.getPositionY()))

        GLOB.screen.blit(self.superfice, (0, 0))

            # pygame.draw.line(GLOB.screen, (5,80,255), start_line, end_line, 8)
            # pygame.draw.line(GLOB.screen, (255,80,5), start_line, end_line1, 8)

        if self.mesh.colliderect(player.hitbox) and self.flag_CanAttack:
            print("GAME OVER")
            inizializza()

        if not self.aggr:

            self.vel = self.default_speed

            if self.monster_ai_brain == 1.5:
                self.direzione = "destra-basso"
                self.angle = 180

            if self.monster_ai_brain == 2.5:
                self.direzione = "sinistra-basso"
                self.angle = 270

            if self.monster_ai_brain == 3.5:
                self.direzione = "sinistra-alto"
                self.angle = 0

            if self.monster_ai_brain == 4.5:
                self.direzione = "destra-alto"
                self.angle = 90

            
            if self.monster_ai_brain == 0:
                self.direzione = "fermo"
            
            if self.monster_ai_brain == 1:
                self.direzione = "destra"
                self.Last_keyPressed = "Right"
                self.angle = 135
            
            if self.monster_ai_brain == 2:
                self.direzione = "sinistra"
                self.Last_keyPressed = "Left"
                self.angle = 315
            
            if self.monster_ai_brain == 3:
                self.direzione = "basso"
                self.Last_keyPressed = "Down"
                self.angle = 225
            
            if self.monster_ai_brain == 4:
                self.direzione = "alto"
                self.Last_keyPressed = "Top"
                self.angle = 45

            # print(self.monster_ai_brain, self.direzione)

            # -- DESTRA --
            if ((self.monster_ai_brain == 1 or self.monster_ai_brain == 1.5 or self.monster_ai_brain == 4.5) and self.monster_ai_brain):
                self.x += self.vel
                self.setRightPress(True)
            else:
                self.setRightPress(False)

            # -- SINISTRA --
            if ((self.monster_ai_brain == 2 or self.monster_ai_brain == 2.5 or self.monster_ai_brain == 3.5)):
                self.x -= self.vel
                self.setLeftPress(True)
            else:
                self.setLeftPress(False)
            
            # -- BASSO --
            if ((self.monster_ai_brain == 3 or self.monster_ai_brain == 1.5 or self.monster_ai_brain == 2.5)):
                self.y += self.vel
                self.setDownPress(True)
            else:
                self.setDownPress(False)

            # -- ALTO --
            if ((self.monster_ai_brain == 4 or self.monster_ai_brain == 4.5 or self.monster_ai_brain == 3.5)):
                self.y -= self.vel
                self.setUpPress(True)
            else:
                self.setUpPress(False)

        
        if self.aggr and self.circle.colliderect(player.hitbox) and not self.ICollide:

            self.vel = self.default_speed * 1.4

            if (player.Last_keyPressed == "Left" and player.Last_keyPressed != "Right") or self.hitbox[0] > player.x:
                self.x -= self.vel
                self.direzione = "sinistra"
                self.monster_ai_brain = 2

            if (player.Last_keyPressed == "Right" and player.Last_keyPressed != "Left") or self.hitbox[0] + self.hitbox[2]/2 < player.x:
                self.x += self.vel
                self.direzione = "destra"
                self.monster_ai_brain = 1

            if (player.Last_keyPressed == "Up" and player.Last_keyPressed != "Down") or self.hitbox[1] > player.y:
                self.y -= self.vel
                self.direzione = "alto"
                self.monster_ai_brain = 4

            if (player.Last_keyPressed == "Down" and player.Last_keyPressed != "Up") or self.hitbox[1] + self.hitbox[3]/2 < player.y:
                self.y += self.vel
                self.direzione = "basso"
                self.monster_ai_brain = 3

        else:
            
            self.flag_CanStartAttack = False
            self.aggr = False


        # GLOB.screen.blit(self.image, (self.x + cam.getPositionX(), self.y + cam.getPositionY()))

        # pygame.draw.rect(GLOB.screen, "Purple", self.mesh, 2 * GLOB.MULT)



        if self.angle >= 360:
            self.angle = 0

        if self.angle <= -1:
            self.angle = 359

    def ruota_destra(self):
        self.angle += 1

    def ruota_sinistra(self):
        self.angle -= 0.25 * GLOB.MULT

    def aumenta_distanza(self):
        self.distanza += 0.25 * GLOB.MULT

    def diminuisci_distanza(self):
        self.distanza -= 0.25 * GLOB.MULT

    def aumenta_lunghezza(self):
        self.default_height += 0.025 * GLOB.MULT

    def diminuisci_lunghezza(self):
        self.default_height -= 0.025 * GLOB.MULT

    def attacca(self, v):
        self.flag_CanAttack = v

    def setRightPress(self, r):
        self.__right_pressed = r

    def setLeftPress(self, l):
        self.__left_pressed = l

    def setUpPress(self, u):
        self.__up_pressed = u

    def setDownPress(self, d):
        self.__down_pressed = d

    def getRightPress(self):
        return self.__right_pressed

    def getLeftPress(self):
        return self.__left_pressed

    def getUpPress(self):
        return self.__up_pressed

    def getDownPress(self):
        return self.__down_pressed

    def HasCollision(self, object):
        
        def Confronta(value):   # Creo una funziona dato che la utilizzo piu' volte e se gli passo "x" fa una cosa mentre se gli passo "y" ne fa un'altra
            
            #self.finish()    # ogni volta che collido stoppo l'animazione del player

            if value=="x":  # confronto il valore passato

                if self.mesh.right >= object.right:  # confronto se la posizione del player delle x è maggiore o uguale della posizione delle x dell'oggetto di cui ho collisione
                    self.x += self.vel   # ogni volta che collido vado a settare la posizione del player indietro grazie alla sua velocità
                    return True # ritorno un valore perchè dopo lo vado ad utilizzare
                elif self.mesh.left <= object.left:
                    self.x -= self.vel    # ogni volta che collido vado a settare la posizione del player indietro grazie alla sua velocità
                    return False # ritorno un valore perchè dopo lo vado ad utilizzare

            if value=="y":  # confronto il valore passato

                if self.mesh.bottom >= object.bottom:  # confronto se la posizione del player delle y è maggiore o uguale della posizione delle y dell'oggetto di cui ho collisione
                    self.y += self.vel    # ogni volta che collido vado a settare la posizione del player indietro grazie alla sua velocità
                    return True # ritorno un valore perchè dopo lo vado ad utilizzare
                elif self.mesh.top <= object.top:
                    self.y -= self.vel    # ogni volta che collido vado a settare la posizione del player indietro grazie alla sua velocità
                    return False # ritorno un valore perchè dopo lo vado ad utilizzare
            

        if self.mesh.colliderect(object):   # Metodo di pygame che confronta se due rettangoli collidono

            self.ICollide = True
            
            self.finish()

            self.monster_ai_vel = 0.25

            pygame.draw.rect(GLOB.screen, "Green", self.mesh, 1)

            # Setto diverse variabili per non ripeterli nei confronti
            w = (self.Last_keyPressed == "Up")
            a = (self.Last_keyPressed == "Left")
            
            s = (self.Last_keyPressed == "Down")
            d = (self.Last_keyPressed == "Right")

            
            a1 = (self.getRightPress() and w or self.getLeftPress() and w)
            b1 =  (self.getLeftPress() and s or self.getRightPress() and s)

            c1 =  (self.getUpPress() and a or self.getDownPress() and a)
            d1 =  (self.getUpPress() and d or self.getDownPress() and d)

            # print("\n\nSinistro o Destro and Sù: ",str(a1))
            # print("Sinistro o Destro and Giù: ",str(b1))
            # print("Alto o Basso and Sinistra: ",str(c1))
            # print("Alto o Basso and Destra: ",str(d1))

            # print("\nup: "+str(self.getUpPress())+" |down: "+str(self.getDownPress())+" |left: "+str(self.getLeftPress())+" |right: "+str(self.getRightPress())+"\n")
            
            if self.Last_keyPressed != "Null":  # Confronto se il giocatore è fermo o si sta muovendo

                if (a1 or b1) and (not c1 and not d1):  # se è stato premuto il pulsante destro/sinistro e NON quello alto o basso mentre si ha una collisione allora:

                    Confronta("x")  # richiamo la funzione

                    if Confronta("x"):  # se la funzione mi ritorna True allora:
                        self.setLeftPress(False)

                        if self.aggr:
                            self.setRightPress(True)
                            self.monster_ai_brain = 1
                    else:  # se la funzione mi ritorna False allora:
                        self.setRightPress(False)

                        if self.aggr:
                            self.setLeftPress(True)
                            self.monster_ai_brain = 2

                    self.Last_keyPressed = "Null"   # Variabile usata per non dare errori dato che l'ultimo pulsante cliccato sono l'insieme di due in contemporanea

                    
                if (c1 or d1) and (not a1 and not b1):  # se è stato premuto il pulsante alto/basso e NON con quello sinistro o destro mentre si ha una collisione allora:

                    Confronta("y")  # richiamo la funzione

                    if Confronta("y"):  # se la funzione mi ritorna True allora:
                        self.setUpPress(False)
             
                        if self.aggr:
                            self.setDownPress(True)
                            self.monster_ai_brain = 3
                    else:  # se la funzione mi ritorna False allora:
                        self.setDownPress(False)
             
                        if self.aggr:
                            self.setUpPress(True)
                            self.monster_ai_brain = 4
                    self.Last_keyPressed = "Null"   # Variabile usata per non dare errori dato che l'ultimo pulsante cliccato sono l'insieme di due in contemporanea
                    

                if (self.getRightPress() or self.getLeftPress() or a or d) and (not w and not s):   # Qua altri confronti con unicamente con un pulante a volta cliccato sinistra/destra
                    Confronta("x")
                
                if (self.getUpPress() or self.getDownPress() or w or s) and (not d and not a):   # Qua altri confronti con unicamente con un pulante a volta cliccato alto/basso
                    Confronta("y")
            else:
                Confronta("y")
                Confronta("x")
                #self.setAllkeys(None)
        else:
            self.ICollide = False
            self.monster_ai_vel = self.default_monster_ai_vel


#Player Initialization
def inizializza():
    global Folder_walkO, Folder_walkVD, Folder_walkVU, Folder_angry
    global player, cam, console, mostro
        
    sceltaG = "Keeper"

    Folder_walkO = '../animation/'+sceltaG+'/WalkOrizontal'
    Folder_walkVD = '../animation/'+sceltaG+'/WalkVerticalD'
    Folder_walkVU = '../animation/'+sceltaG+'/WalkVerticalU'
    Folder_angry = '../animation/'+sceltaG+'/Angry'

    def riempi(percorso):
        FileNames = os.listdir(percorso)

        # Ordino i file e gli appendo ad una lista, in modo che le animazioni siano lineari e ordinate
        FileNames.sort(key=lambda f: int(re.sub('\D', '', f)))
        sorted(FileNames)

        for filename in FileNames:
            if percorso == Folder_walkO:
                #print("Trovato Percorso WO")
                GLOB.PlayerWalkingO.append(filename)
            if percorso == Folder_walkVD:
                #print("Trovato Percorso WVD")
                GLOB.PlayerWalkingVD.append(filename)
            if percorso == Folder_walkVU:
                #print("Trovato Percorso WVU")
                GLOB.PlayerWalkingVU.append(filename)
                
            if percorso == Folder_angry:
                GLOB.MonsterAngry.append(filename)

    riempi(Folder_walkO)
    riempi(Folder_walkVD)
    riempi(Folder_walkVU)
    riempi(Folder_angry)


    player = giocatore.Player(100 * GLOB.MULT, 90 * GLOB.MULT)
    cam = Cam()
    mostro = Mostro((0 * GLOB.MULT, 0 * GLOB.MULT), 1.2, (20 * GLOB.MULT, 0.6 * GLOB.MULT))
    console = Debug()


def render(lista, color, var, hitbox):
        x = 0
        y = 0
        tiles_risoluzione = 32 * GLOB.MULT
        collisione = pygame.Rect(x + cam.getPositionX(), y + cam.getPositionY(), tiles_risoluzione, tiles_risoluzione)

        for valore_y in range(len(lista)):

            x = 0
            for valore_x in range(len(lista[valore_y])):
                condition = lista[valore_y][valore_x] == var

                if condition:
                    collisione = pygame.Rect(x + cam.getPositionX(), y + cam.getPositionY(), tiles_risoluzione, tiles_risoluzione)
                    pygame.draw.rect(GLOB.screen, color, collisione)
                    #print("\n- Render | Oggetto a schermo!", object)
                    
                    if hitbox != None:
                        #print("- Render | Collisione Oggetto Impostata!", collisione,"\n")
                        player.HasCollision(collisione)
                        mostro.HasCollision(collisione)

                if GLOB.Debug:
                    pygame.draw.rect(GLOB.screen, (255,0,0), collisione, 1)

                x += tiles_risoluzione

            y += tiles_risoluzione


lista_oggetti = [

    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1]

]

def disegna():
    #Draw
    GLOB.screen.fill((12, 24, 36))
    cam.update(GLOB.Cam_visible)
    #print(cam.getPositionX(), cam.getPositionY())

    mostro.aggiorna()
    player.draw(GLOB.screen)

    # render(lista = lista_oggetti, color = "Blue", var = 1, hitbox = None)
    render(lista = lista_oggetti, color = "Yellow", var = 0, hitbox = True)

    # obstacle = pygame.Rect((cam.getPositionX()+60*GLOB.MULT),(cam.getPositionY()+140*GLOB.MULT), 20*GLOB.MULT, 10*GLOB.MULT)

    # pygame.draw.rect(GLOB.screen, (0,100,255), obstacle)
    # player.HasCollision(obstacle)

    #update
    player.update()

def main():
    #Main Loop
    inizializza()
    while True:

        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.setLeftPress(True)
                    player.Last_keyPressed = "Left"
                if event.key == pygame.K_d:
                    player.setRightPress(True)
                    player.Last_keyPressed = "Right"
                if event.key == pygame.K_w:
                    player.setUpPress(True)
                    player.Last_keyPressed = "Up"
                if event.key == pygame.K_s:
                    player.setDownPress(True)
                    player.Last_keyPressed = "Down"
                    
            if event.type == pygame.KEYUP:
                player.Last_keyPressed = "Null"
                if event.key == pygame.K_a:
                    player.setLeftPress(False)
                if event.key == pygame.K_d:
                    player.setRightPress(False)
                if event.key == pygame.K_w:
                    player.setUpPress(False)
                if event.key == pygame.K_s:
                    player.setDownPress(False)


        if pygame.mouse.get_pressed()[0] or keys_pressed[pygame.K_e]:
            mostro.ruota_destra()

        if pygame.mouse.get_pressed()[2] or keys_pressed[pygame.K_q]:
            mostro.ruota_sinistra()

        if keys_pressed[pygame.K_l]:
            mostro.attacca(False)

        if keys_pressed[pygame.K_k]:
            mostro.attacca(True)

        if keys_pressed[pygame.K_UP]:
            mostro.aumenta_lunghezza()

        if keys_pressed[pygame.K_DOWN]:
            mostro.diminuisci_lunghezza()

        if keys_pressed[pygame.K_RIGHT]:
            mostro.aumenta_distanza()

        if keys_pressed[pygame.K_LEFT]:
            mostro.diminuisci_distanza()
            
        disegna()

        console.log(GLOB.Debug)
        pygame.display.flip()
        clock.tick(GLOB.FPS)


if __name__ == "__main__":
    main()