import pygame

class Player_2():
    def __init__(self, x, y, player_size, sprite_sheet, animation_frames):
        self.size = player_size
        self.animation_list = self.load_images(sprite_sheet, animation_frames)
        self.action = 0  #0: Idle #1: Block #2: Punch #3: Jump #4: Death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.alive = True
        self.stamina = 100
        self.movex = 10
        self.jump = False
        self.gravity = 0
        self.block = False
        self.block_cd = 0
        self.attack_cd = 0
        self.attacking = False
        self.health = 100
        self.flip = False
        self.rect = pygame.Rect((x, y, 110, 220))
        
        self.punch_sound = pygame.mixer.Sound("Music/hit.mp3")
        self.punch_sound.set_volume(0.2)
        self.shield = pygame.mixer.Sound("Music/shield.mp3")
        self.shield.set_volume(0.1)

    def load_images(self, sprite_sheet, animation_frames):
    
        animation_list = [] 
        for y, animation in enumerate(animation_frames):  
            temp_img_list = [] 
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size) 
                temp_img_list.append(pygame.transform.scale(temp_img, (150, 220)))
            animation_list.append(temp_img_list) 
        return animation_list


    def move(self, surface, target):
        keys = pygame.key.get_pressed()

        #Movement and jumping
        if self.block == False and self.attacking == False and target.health > 0 and self.alive == True:
            if keys[pygame.K_l]:
                self.rect.x += self.movex
            if keys[pygame.K_j]:
                self.rect.x -= self.movex 
            if keys[pygame.K_i] and self.jump == False:
                self.gravity = -30
                self.jump = True
        
        #Apply gravity
        self.gravity += 2
        self.rect.y += self.gravity
        
        #Blocking
        if keys[pygame.K_o] and self.stamina >= 0 and self.block_cd == 0 and target.health > 0 and self.alive == True:
            self.stamina -= 2
            self.block = True
            self.rect.width = 140 
        else:
            self.player_stamina()
            self.stamina_cd()
            self.rect.width = 110
            self.block = False  
        
        #Attacking
        if keys[pygame.K_u] and self.block == False and self.alive == True and target.health > 0:
            self.attack(surface, target)
        
        #Attack cooldown
        if self.attack_cd > 0:
            self.attack_cd -= 0.7
        if self.attack_cd <= 0:
            self.attack_cd = 0 

        #keeps player on screen
        if self.rect.left <= 0: self.rect.x = 0
        if self.rect.right >= 1000: self.rect.right = 1000
        if self.rect.bottom >= 470:
            self.jump = False
            self.rect.bottom = 470
            if self.gravity >= 0:
                self.gravity = 0
        

        #Ensures players always face eachother
        if target.rect.centerx < self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        

    def attack(self, surface, target):
        if self.attack_cd == 0:
            self.attack_cd += 50
            self.attacking = True

            #Keeps attack hitboxes at the correct size and space when players are in standard or flipped orientation 
            if self.flip == False:
                attack_rect = pygame.Rect(self.rect.left - 30, self.rect.y - 2, self.rect.width / 3.5 , self.rect.height)   
            else:
                attack_rect = pygame.Rect(self.rect.right , self.rect.y - 2, self.rect.width / 2.7, self.rect.height) 
            if attack_rect.colliderect(target.rect) and target.block == False:
                target.health -= 10


            #Attack rectangle below that allows hitboxes to be seen when working on the game. Un-comment make use of it
            #pygame.draw.rect(surface, (0, 0, 255), attack_rect)


    def pass_through(self, target):
        #Prevents players from phasing through eachother when moving
        if self.flip == True and self.rect.colliderect(target.rect) and self.jump == False and target.jump == False:
            self.rect.x -= 5
            target.rect.x += 5
        elif self.rect.colliderect(target.rect) and self.jump == False and target.jump == False:
            self.rect.x += 5
            target.rect.x -= 5


    def player_stamina(self):
        self.stamina += 1
        if self.stamina > 100:
            self.stamina = 100
        if self.stamina == 0:
            self.block_cd += 1
   

    def stamina_cd(self):
        if self.block_cd >= 10:
            self.block_cd = 0
        elif self.block_cd > 0:
            self.block_cd += 0.09


    def update(self):  
        #Check what action is being performed
        if self.block == True:
            self.shield.play()
            self.update_action(1)
        elif self.attacking == True:
            self.punch_sound.play()
            self.update_action(2)
        elif self.jump == True:
            self.update_action(3)
        elif self.health <= 0:
            self.update_action(4)
            self.alive = False
        else:
            self.update_action(0)

        animation_cooldown = 300
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0
                if self.action == 2:
                    self.attacking = False
                
    
    def update_action(self, new_action):
        #Check if the new action is different than the previous one and reset the frame count to 0 to prevent skipped frames 
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        
        #Ensures players stay inside of their hitboxes at all times
        if self.flip == True and self.block == True:
            surface.blit(img, (self.rect.x - 10, self.rect.y + 8))
        elif self.flip == True:
            surface.blit(img, (self.rect.x - 10, self.rect.y + 8))
        elif self.flip == False and self.block == True:
            surface.blit(img, (self.rect.x , self.rect.y + 8))     
        else:
            surface.blit(img, (self.rect.x - 30, self.rect.y + 8))


        #Below is the players hitbox. Un-comment when working on game mechanics
        #pygame.draw.rect(surface, (0,255,0), self.rect)
