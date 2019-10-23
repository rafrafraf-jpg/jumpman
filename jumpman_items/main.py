# jumpman main game
import pygame as pg
from settings import *
import time

###### FIX: PARTIALLY JUMPING THROUGH BLOCKS WHEN JUMPING INTO CORNER
###### ADD: GLOBAL SCOREBOARD, BOSS CHARACTER

pg.init()
pg.mixer.music.load('sounds/music.mp3')
pg.mixer.music.play(-1)

class Block(object):
  def __init__(self, pos, texture):
    '''pos = (x,y)\texture = "grass"'''
    if texture in textures:
      self.texture = textures[texture]
    self.pos = list(pos)

  def args(self):
    return self.texture, self.pos
  
class Game(object):
  def __init__(self):
    '''init game window'''
    pg.init()
    self.screen = pg.display.set_mode((W, H))
    pg.display.set_caption(title)
    self.clock = pg.time.Clock()

    pg.mixer.pre_init(44100, -16, 1, 512)

    self.effect = pg.mixer.Sound('sounds/jump.wav')

    self.running = True

    self.runScreen = False

    self.gameSpeed = 16# must be a mupltiple of screen width(512)

    self.playing = True

    try:
      self.volMute
    except Exception:
      self.volMute = False

    # checks if level doesnt exist if true then defines level
    try:
      self.level
    except Exception:
      self.level = 0

    if self.level == -1:
      self.level = 0

    self.output = []
    self.outputSideCol = []

    # background var
    self.bgX = 0
    self.bgY = 0

    # initialise main/jumpman sprite var
    self.frame = 0
    self.rFrame = True
    
    self.mainX = HW - mainJR.get_width() / 2
    self.mainY = H * 0.71
    
    self.walkRight = False
    self.walkLeft = False
    
    self.mW = mainJR.get_width()
    self.mH = mainJR.get_height()
    
    self.vel = 0
    self.grav = 0
    
    self.falling = False
    self.jump = False

    # tmp var for show_start_screen func
    self.tmp = 0
    self.msgtmp = 19
    self.bool = True

    # tmp var for show_gameover_screen func
    self.gameovertmp = 0
    self.drawmaintmp = False

    # tmp var for show_next_level func
    self.lvltmp = 0

    # creates a list of blocks with image and coords and a list of all the block coords based on what level
    blockgrid = []
    xcoord,ycoord = 0,-1
    for i in blockgridtmp[self.level]:
      ycoord += 1
      tmp = len(i)
      for x in i:
        if xcoord == tmp:
          xcoord = 0
        xcoord += 1
        if x == 'g':
          blockgrid.append((((xcoord - 1) * 64,ycoord * 64), 'grass'))
        if x == 'r':
          blockgrid.append((((xcoord - 1) * 64,ycoord * 64), 'rGrass'))
        if x == 'b':
          blockgrid.append((((xcoord - 1) * 64,ycoord * 64), 'bricks'))
        if x == 's':
          blockgrid.append((((xcoord - 1) * 64,ycoord * 64), 'spikes'))
        if x == 'i':
          blockgrid.append((((xcoord - 1) * 64,ycoord * 64), 'barrier'))
        if x == 'c':
          blockgrid.append((((xcoord - 1) * 64,ycoord * 64), 'castlebricks'))
        if x == 'p':
          blockgrid.append((((xcoord - 1) * 64,ycoord * 64), 'blockpipe2'))
        if x == 'P':
          blockgrid.append((((xcoord - 1) * 64,ycoord * 64), 'blockpipe'))
    
    # create and reset block coordinates
    self.blocks = []
    self.spikegrid = []
    self.blockgridmap = []
    self.lastpipe = (0,0)
    for i in blockgrid:
      self.blockgridmap.append(i[0])
      if i[1] == 'spikes':
        self.spikegrid.append(i[0])
      if i[1] != 'barrier':# hides barrier blocks
        self.blocks.append(Block(i[0],i[1]))
      if i[1] == 'blockpipe' and i[0][0] > self.lastpipe[0]:
        self.lastpipe = i[0]

    # check if music was paused
    if self.volMute:
      pg.mixer.music.pause()
      self.effect.set_volume(0)
    else:
      pg.mixer.music.unpause()
      self.effect.set_volume(1.0)

    # stores level times scoreboard
    try:
      if self.end != 0:
        self.times.append(self.elapsed)
    except Exception:
      self.times = []

    self.elapsed = 0
    self.start = 0
    self.end = 0

    # once you loop back to level 1 after completing the final level, the scoreboard is wiped
    if len(self.times) + 1 > len(blockgridtmp):
      self.times = []
    
  def run(self):
    '''game loop'''
    while self.playing:
      if self.check_gameover():
        self.show_gameover_screen()
        
      elif 'next level' in self.output:
        self.show_next_level()
        self.level += 1
        self.__init__()
        
      else:
        # if not gameover show main game:
        self.clock.tick(FPS)
        self.events()
        pg.display.update()
        self.draw()
        
  def check_collision(self,a,aw,ah,b,bw,bh):
    '''check collision between rect obj a and b, returns
    which side of obj b is touching obj a'''
    ax,ay = a[0],a[1]
    bx,by = b[0],b[1]

    rect_obj_a = pg.Rect(ax, ay, aw, ah)
    rect_obj_b = pg.Rect(bx, by, bw, bh)

    if rect_obj_a.colliderect(rect_obj_b):
      if (bx,by) in self.spikegrid:
        # if obj a touches a spike
        return 'gameover'
      if (bx,by) == self.lastpipe:
        # if obj a touches the last pipe on the screen
        return 'next level'
      if by - 50 <= (ay + ah) <= by + 50:
        # if obj is above obj b
        self.mainY = by - ah
        return 'above'
      if by + bh - 32 < ay < by + bh + 32:
        # if obj a is under obj b
        return 'under'

  def check_side_collision(self,a,aw,ah,b,bw,bh):
    '''check collision between rect obj a and b, returns
    which side of obj b is touching obj a'''
    ax,ay = a[0],a[1]
    bx,by = b[0],b[1]

    rect_obj_a = pg.Rect(ax, ay, aw, ah)
    rect_obj_b = pg.Rect(bx, by, bw, bh)

    if rect_obj_a.colliderect(rect_obj_b):
      if (bx,by) in self.spikegrid:
        # if obj a touches a spike
        return 'gameover'
      if bx + bw + 32 >= ax >= bx + bw - 32:
        # if obj a is on the right side of obj b
        return 'right'
      if bx - 32 <= ax + aw <= bx + 32:
        # if obj a is on the left side of obj b
        return 'left'
    
  def events(self):
    '''game loop events'''
    for event in pg.event.get():
      if event.type == pg.QUIT:
        self.playing = False
        self.running = False

      keys = pg.key.get_pressed()

      # walk right
      if not self.walkLeft and (keys[pg.K_RIGHT] or keys[ord('d')]):
        self.walkRight = True
        self.rFrame = True
      else:
        self.walkRight = False

      # walk left
      if not self.walkRight and (keys[pg.K_LEFT] or keys[ord('a')]):
        self.walkLeft = True
        self.rFrame = False
      else:
        self.walkLeft = False
        
      # jump
      if not self.falling and not self.jump and (keys[pg.K_UP] or keys[ord(' ')] or keys[ord('w')]):
        # check if sprite is in a 1 block high area
        if 'under' not in self.output and 'above' in self.output:
          self.vel = 42
          self.jump = True
          self.effect.play()
        
  def check_gameover(self):
    '''checks if anything should cause
    the show_gameover_screen func'''
    # check if sprite touches spikes
    if 'gameover' in self.output or 'gameover' in self.outputSideCol:
      return True
    # check if sprite falls out of screen
    elif self.mainY > H:
      return True
    else:
      return False
  
  def draw(self):
    '''game loop draw'''
    # moves blocks and background to the right
    if self.walkRight and 'left' not in self.outputSideCol:
      self.bgX -= self.gameSpeed / 4
      
      for i in self.blocks:
        i.pos[0] -= self.gameSpeed
        
      for i in range(len(self.blockgridmap)):
        x = self.blockgridmap[i][0] - self.gameSpeed
        y = self.blockgridmap[i][1]
        self.blockgridmap[i] = x,y

      for i in range(len(self.spikegrid)):
        x = self.spikegrid[i][0] - self.gameSpeed
        y = self.spikegrid[i][1]
        self.spikegrid[i] = x,y

      self.lastpipe = (self.lastpipe[0] - self.gameSpeed, self.lastpipe[1])

    # moves blocks and background to the left
    if self.walkLeft and 'right' not in self.outputSideCol:
      self.bgX += self.gameSpeed / 4
      
      for i in self.blocks:
        i.pos[0] += self.gameSpeed
        
      for i in range(len(self.blockgridmap)):
        x = self.blockgridmap[i][0] + self.gameSpeed
        y = self.blockgridmap[i][1]
        self.blockgridmap[i] = (x,y)

      for i in range(len(self.spikegrid)):
        x = self.spikegrid[i][0] + self.gameSpeed
        y = self.spikegrid[i][1]
        self.spikegrid[i] = (x,y)

      self.lastpipe = (self.lastpipe[0] + self.gameSpeed, self.lastpipe[1])

    # blits the background on the left, middle and right of the screen to scroll
    self.screen.blit(bg, (self.bgX + W, self.bgY))
    self.screen.blit(bg, (self.bgX, self.bgY))
    self.screen.blit(bg, (self.bgX - W, self.bgY))
    # when bg is out of screen it centers it back into the screen
    if self.bgX == -W:
      self.bgX = 0
    if self.bgX == W:
      self.bgX = 0

    # draw all blocks onto display
    for i in self.blocks:
      self.screen.blit(*i.args())

    # walk right animation
    if not self.jump and not self.falling and self.walkRight:
      self.screen.blit(mainR[self.frame], (self.mainX, self.mainY))
      self.frame += 1
      if self.frame == len(mainRtmp):
        self.frame = 0   
    # walk left animation  
    if not self.jump and not self.falling and self.walkLeft:
      self.screen.blit(mainL[self.frame], (self.mainX, self.mainY))
      self.frame += 1
      if self.frame == len(mainRtmp):
        self.frame = 0
    # idle right frame
    if not self.jump and not self.falling and self.rFrame and not self.walkLeft and not self.walkRight:
      self.screen.blit(mainR[2], (self.mainX, self.mainY))
    # idle left frame
    if not self.jump and not self.falling and not self.rFrame and not self.walkLeft and not self.walkRight:
      self.screen.blit(mainL[2], (self.mainX, self.mainY))
    # falling right frame
    if not self.jump and self.falling and self.rFrame:
      self.screen.blit(mainJR, (self.mainX, self.mainY))
    # falling left frame
    if not self.jump and self.falling and not self.rFrame:
      self.screen.blit(mainJL, (self.mainX, self.mainY))
      
    # jump  
    if self.jump:
      # check if collides with bottom of block
      if 'under' not in self.output:
        self.mainY -= self.vel
        if self.vel <= 0:
          self.jump = False
          self.falling = True
        else:
          self.vel -= 6
      else:
        self.jump = False
        self.falling = True
        
      # jumping right frame
      if self.rFrame:
        self.screen.blit(mainJR, (self.mainX, self.mainY))
      # jumping left frame
      if not self.rFrame:
        self.screen.blit(mainJL, (self.mainX, self.mainY))
      if self.vel <= 0:
        self.jump = False
        self.falling = True
      
    # falling logic
    if self.falling and not self.jump:
      self.mainY += self.grav
      if self.grav != 48:
        self.grav += 6
    else:
      self.grav = 12

    # top platform main sprite collision check
    self.output = [self.check_collision((self.mainX + (self.mW / 4), self.mainY + (self.mH / 4) - 12),32,61+24, i,64,64) for i in self.blockgridmap]
    if not self.jump and 'above' in self.output:
      self.falling = False
    else:
      self.falling = True

    # sprite top and bottom hitbox
    mainHitBox = (self.mainX + (self.mW / 4), self.mainY + (self.mH / 4) - 24, 32, 61 + 48)
    #pg.draw.rect(self.screen, RED, mainHitBox)

    # side platform main sprite collision check
    self.outputSideCol =[self.check_side_collision((self.mainX + (self.mW / 4) - 7, self.mainY + (self.mH / 4) + 15),32 + 14,61 - 30, i,64,64) for i in self.blockgridmap]

    # sprite side hitbox
    mainHitBox2 = (self.mainX + (self.mW / 4) - 15, self.mainY + (self.mH / 4) + 10, 32 + 20, 61 - 30)
    #pg.draw.rect(self.screen, BLUE, mainHitBox2)

    self.vol_button()

    # get the start time of a level
    if self.start == 0:
      self.start = time.time()

    # displays the scores for every level up to the level the player is on
    textType = pg.font.SysFont('impact', 30)
    textRect = textType.render('%s\'S TIMES :' % self.user, 1, BLACK)    
    self.screen.blit(textRect, (0, 0))
    for i in range(len(blockgridtmp) - 1):
      try:
        self.display_times(i + 1, self.times[i], 28 + (i * 28))
      except Exception:
        pass
    
    pg.display.flip()

  def display_times(self, level, time, num):
    '''display level times'''
    textType = pg.font.SysFont('impact', 30)
    textRect = textType.render('LEVEL %s : %.2f SECONDS' % (level, time), 1, BLACK)    
    self.screen.blit(textRect, (0, 0 + num))
    
      
  def vol_button(self):
    '''volume mute and unmute'''
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    volx1 = W - 25
    voly1 = 1
    
    volx2 = W - 49
    voly2 = 1
    
    if self.volMute:
      obj1 = self.screen.blit(vol[1], (volx1,voly1))
      if volx1 + 24 > mouse[0] > volx1 and voly1 + 24 > mouse[1] > voly1:
        if click[0] == 1:
          self.volMute = False
          pg.mixer.music.unpause()
          self.effect.set_volume(1.0)
    else:
      obj2 = self.screen.blit(vol[0], (volx2,voly2))
      if volx2 + 24 > mouse[0] > volx2 and voly2 + 24 > mouse[1] > voly2:
        if click[0] == 1:
          self.volMute = True
          pg.mixer.music.pause()
          self.effect.set_volume(0)

  def draw_button(self, w, h, x, y, txt, c1, c2, rtrn=False):#### button text isnt centerd to rect FIX IT
    '''button function for the start and gameover screen'''
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    # checks if mouse is in area of button and if it clicks while in it
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
      # hover functionality using rtrn
      if rtrn:
        return 0
      button = pg.draw.rect(self.screen, c1, (x, y, w, h))
      if click[0] == 1:
        return True
    else:
      button = pg.draw.rect(self.screen, c2, (x, y, w, h))

    # default txt size is 20
    txtSize = 20
    
    textType = pg.font.SysFont('impact', txtSize)
    textRect = textType.render(txt, 1, BLACK)
    txtW, txtH = textRect.get_size()

    # if the default txt size is bigger than the button, decrease txt size
    while txtW > w:
      txtSize -= 1
      textType = pg.font.SysFont('impact', txtSize)
      textRect = textType.render(txt, 1, BLACK)
      txtW, txtH = textRect.get_size()
    # if the default txt size is smaller than the button, increase txt size
    while txtW < w:
      txtSize += 1
      textType = pg.font.SysFont('impact', txtSize)
      textRect = textType.render(txt, 1, BLACK)
      txtW, txtH = textRect.get_size()
    # make the txtsize 1 size smaller otherwise it doesnt fit perfectly
    textType = pg.font.SysFont('impact', txtSize - 1)
    textRect = textType.render(txt, 1, BLACK)
    txtW, txtH = textRect.get_size()
    
    self.screen.blit(textRect, (x + 1, y + (h / 2) - (txtH / 2)))
    
  def show_start_screen(self):
    '''play and exit start screen'''
    # update the display
    self.clock.tick(FPS)
    self.events()
    pg.display.update()
    
    self.screen.fill(BLACK)

    # random message
    tmpfont = pg.font.SysFont('helvetica', self.msgtmp, True, False)
    tmptext = pg.transform.rotate(tmpfont.render(message, True, WHITE),32)
    self.screen.blit(tmptext, (HW / 5, HH / 3))

    # increases then decreases random message txt size
    if self.bool:
      self.msgtmp += 1
      if self.msgtmp > 25:
        self.bool = False
    else:
      self.msgtmp -= 1
      if self.msgtmp < 19:
        self.bool = True
          
    # blits mainR animation onto start screen when hovering over the buttons
    self.screen.blit(mainR[self.tmp], (HW - 25, HH - 25 - (mainJR.get_height())))
      
    # draw 'LEVEL 1' and 'EXIT GAME' button with their functionality
    if self.draw_button(100,50,HW - 50,HH - 25,'LEVEL %s' % int(self.level + 1),GREEN,(0, 200, 0)):
      if len(self.letters) >= 3:
        # self.user is the string variable for the username of the player
        self.user = ''
        for i in self.letters:
          self.user += i
        self.runScreen = True
    elif self.draw_button(100,50,HW - 50,HH - 25,'LEVEL %s' % int(self.level + 1),GREEN,(0, 200, 0),True) == 0:
      if self.tmp == len(mainRtmp) - 1:
        self.tmp = 0
      else:
        self.tmp += 1
    
    if self.draw_button(100,50,HW - 50,HH + 25 + 1,'EXIT GAME',RED,(200, 0, 0)):
      self.running = False
      self.playing = False

    self.user_input()

    pg.display.flip()


  def user_input(self):
    '''creates the username input on start screen'''
    allow = 'abcdefghijklmnopqrstuvwxyz'
    
    try:
      self.letters
    except Exception:
      self.letters = []
    
    string = ''
    for i in self.letters:
      string += i + ' '

    while len(string) != 8:
      string += ' _'
    
    textType = pg.font.SysFont('impact', 45)
    textRect = textType.render('%s' % '_ _ _ _' if string == '' else string, 1, WHITE)
    txtWidth = textRect.get_width()
    self.screen.blit(textRect, (HW - (txtWidth / 2) + 5, 50))

    for event in pg.event.get():
      if event.type == pg.KEYDOWN:
        let = pg.key.name(event.key)
        
        if let in allow:
          if len(self.letters) < 4:
            self.letters.append(let.upper())
              
        elif let == 'backspace' and len(self.letters) > 0:
          del self.letters[-1]
                      
  def show_next_level(self):
    '''next level screen'''
    self.end = time.time()

    # get the time taken to finish the level
    self.elapsed = self.end - self.start
    
    while True:
      self.clock.tick(FPS)

      pg.draw.rect(self.screen,BLACK,(0, -H + self.lvltmp, W, H))

      if self.level == len(blockgridtmp) - 1:
        self.level = -1

      fnt = pg.font.SysFont('impact', 30)
      txtrct = fnt.render('LEVEL %s' % int(self.level + 2), 1, WHITE)
      wtmp = txtrct.get_width()
      self.screen.blit(txtrct, (HW - (wtmp / 2), -HH + self.lvltmp))

      if self.lvltmp == H + self.gameSpeed:
        break

      self.lvltmp += self.gameSpeed
    
      pg.display.update()
      pg.display.flip()

  def show_gameover_screen(self):
    '''game over/continue screen'''
    self.clock.tick(FPS)
    self.events()
    pg.display.update()

    # draw the bg onto display
    self.screen.blit(bg, (self.bgX + W, self.bgY))
    self.screen.blit(bg, (self.bgX, self.bgY))
    self.screen.blit(bg, (self.bgX - W, self.bgY))

    # draw all blocks onto display
    for i in self.blocks:
      self.screen.blit(*i.args())

    # draw the main/ jumpman sprite move into the middle of the screen
    if self.drawmaintmp:
      self.screen.blit(mainJR, (self.mainX, HH - self.mH / 2))

    # black screen slides in from left
    pg.draw.rect(self.screen, BLACK, (self.gameovertmp - W, 0, W, H))
    # black screen slides in from right
    pg.draw.rect(self.screen, BLACK, (- self.gameovertmp + W, 0, W, H))
    # black screen slides in from top
    pg.draw.rect(self.screen, BLACK, (0, (self.gameovertmp / 2) - H, W, H))
    # black screen slides in from bottom
    pg.draw.rect(self.screen, BLACK, (0, (- self.gameovertmp / 2) + H, W, H))

    # moves buttons up with the black screen
    if self.draw_button(100,50,HW - 50,- (self.gameovertmp / 2) + H + 10,'TRY AGAIN',GREEN,(0, 200, 0)):
        self.__init__()# resets all game variables to initial values to reset game
    if self.draw_button(100,50,HW - 50,- (self.gameovertmp / 2) + H + 61,'EXIT GAME',RED,(200, 0, 0)):
      self.running = False
      self.playing = False

    # increases variable that moves the black screen and buttons onto screen
    if self.gameovertmp != HW - 32:
      self.gameovertmp += 16
    else:
      self.drawmaintmp = True

    pg.display.flip()
  
g = Game()
while g.running:
  if not g.runScreen:
    g.show_start_screen()
  if g.runScreen:
    g.run()

pg.quit()

