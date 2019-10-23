# jumpman settings
import pygame as pg
import json, random, os, base64

# display settings
title = 'jumpman 1.5'
W, H = 896, 512
HW, HH = W / 2, H /2
AREA = W * H
FPS = 20

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (169,169,169)

pg.init()
screen = pg.display.set_mode((W, H))
pg.display.set_caption(title)
clock = pg.time.Clock()

totalLoads = 14
LDMax = 249
LDInc = LDMax / totalLoads
inc = 0

def load_screen(txt,x=1,check=False):
  global inc
  
  clock.tick(FPS)

  if not check:
    inc += 1

  # check total loads
  #print(inc)

  screen.fill(BLACK)
    
  loadTextType = pg.font.SysFont('impact', 15)
  loadTextRect = loadTextType.render(txt, 1, WHITE)
  w = loadTextRect.get_width()
  #screen.blit(loadTextRect, (HW - (60 + w), HH))
  screen.blit(loadTextRect, (HW - (LDMax / 2), HH + 20))
  
  pg.draw.rect(screen,WHITE,(HW - (LDMax / 2), HH, (LDInc * inc) + x, 20))

  pg.draw.rect(screen,WHITE,(HW - (LDMax / 2), HH, LDMax, 20),True)

  pg.display.update()
  pg.display.flip()

load_screen('loading and scaling BG image')

# bakcground image load an scaling
bgtmp = pg.image.load('sprites/backgroundV3.png')

bg = pg.transform.scale(bgtmp, (W, H))

load_screen('loading and scaling volume button images')

# volume button loads

vol = [pg.transform.scale(pg.image.load('sprites/vol1.png'),(24,24)),
       pg.transform.scale(pg.image.load('sprites/vol2.png'),(24,24))]

load_screen('loading R sprite images[0]')

# main/jumpman sprite setup
mainRtmp = [pg.image.load('sprites/jumpmanR1.png'),
            pg.image.load('sprites/jumpmanR1.png'),
            pg.image.load('sprites/jumpmanR2.png'),
            pg.image.load('sprites/jumpmanR2.png'),
            pg.image.load('sprites/jumpmanR3.png'),
            pg.image.load('sprites/jumpmanR3.png'),
            pg.image.load('sprites/jumpmanR4.png'),
            pg.image.load('sprites/jumpmanR4.png')]

load_screen('loading R sprite images[4]')

mainR = []
for i in mainRtmp:
  mainR.append(pg.transform.scale(i, (64, 96)))

load_screen('loading L sprite images[0]')

mainLtmp = [pg.image.load('sprites/jumpmanL1.png'),
            pg.image.load('sprites/jumpmanL1.png'),        
            pg.image.load('sprites/jumpmanL2.png'),
            pg.image.load('sprites/jumpmanL2.png'),
            pg.image.load('sprites/jumpmanL3.png'),
            pg.image.load('sprites/jumpmanL3.png'),
            pg.image.load('sprites/jumpmanL4.png'),
            pg.image.load('sprites/jumpmanL4.png')]

load_screen('loading L sprite images[4]')


mainL = []
for i in mainLtmp:
  mainL.append(pg.transform.scale(i, (64, 96)))
  
mainJR = mainR[0]
mainJL = mainL[0]

load_screen('loading block textures [0]')

# block settings
textures = {
  'grass' : pg.transform.scale(pg.image.load('sprites/blockV2.png'),(64,64)),
  'rGrass' : pg.transform.scale(pg.image.load('sprites/block2V2.png'),(64,64)),
  'bricks' : pg.transform.scale(pg.image.load('sprites/block3.png'),(64,64)),
  'spikes' : pg.transform.scale(pg.image.load('sprites/blockspike.png'),(64,64)),
  'barrier' : pg.transform.scale(pg.image.load('sprites/blockbarrier.png'),(64,64)),
  'castlebricks' : pg.transform.scale(pg.image.load('sprites/block4.png'),(64,64)),
  'blockpipe' : pg.transform.scale(pg.image.load('sprites/blockpipe.png'),(64,64)),
  'blockpipe2' : pg.transform.scale(pg.image.load('sprites/blockpipe2.png'),(64,64))
  }

load_screen('loading block textures [5]')

load_screen('defining block grid')

# block grid map level 1
blockgridtmp = [[
  ['o','o','o','b','b','o','o','o','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','b','o','o','o','b','o','b','b','b','b','b','b','b','b','b','b','b','b','b','o','o','o','o'],
  ['o','o','o','b','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','b','o','b','o','b','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','o','o','o','o','o','b','b','b','o','o','o','o','o','o','o','o','o','o','o','o','o','o','g','g','o','o','o','o','o','o','o','o','g','g','o','b','o','b','o','b','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','b','b','s','b','b','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','g','o','o','g','o','g','g','g','s','g','g','o','o','o','b','o','o','o','b','o','o','o','o','o','o','o','o','o','P'],
  ['o','o','o','o','o','o','o','o','o','o','g','o','g','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','i','o','o','o','o','o','o','o','o','b','o','b','o','o','i','o','o','o','o','o','c','p'],
  ['o','o','o','b','o','o','o','o','o','g','b','o','b','g','o','o','o','o','o','o','o','o','o','o','g','o','o','o','o','o','o','o','i','o','o','o','o','o','o','o','o','b','o','o','o','o','o','o','o','o','o','c','c','p'],
  ['o','o','o','b','b','o','o','o','g','b','b','o','b','b','g','o','o','o','o','g','o','g','o','g','o','g','o','g','g','o','o','o','i','o','o','o','o','o','o','o','b','b','b','b','b','o','o','o','o','c','c','c','c','p'],
  ['o','o','o','b','b','s','b','g','b','b','b','s','b','b','b','g','g','g','g','o','s','o','s','o','o','o','o','o','o','o','g','g','g','g','g','g','g','o','g','s','b','b','b','b','o','s','s','s','s','o','o','o','o','p']
],[
  ['o','o','o','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','c','c','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','c','c','o','o','o','c','c','o','o','o','o','o','o','o','o','o','o','o','P'],
  ['o','o','o','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','c','s','s','c','o','o','o','o','o','o','r','p'],
  ['o','o','o','c','o','o','o','o','o','o','o','c','o','o','o','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','c','c','c','o','o','o','o','i','o','o','o','o','o','c','o','o','o','r','b','p'],
  ['o','o','o','c','o','o','o','o','c','o','o','o','o','o','o','o','o','o','o','c','c','s','c','s','c','s','s','c','o','o','c','c','s','s','o','o','o','c','o','o','o','i','o','o','o','o','c','o','o','o','r','b','b','p'],
  ['o','o','o','c','c','c','P','c','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','c','c','s','c','c','c','c','c','o','o','o','o','o','o','o','p']
],[
  ['o','o','o','o','o','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','o','o','o','o','o','o','o','o','o','o','o','o','o','s','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','i','o','o','o','o','o','o','r','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','b','o','s','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','o','o','o','o','r','r','r','o','o','o','o','o','o','o','o','o','o','o','r','o','o','o','o','o','o','o','o','o','r','b','o','s','o','o','o','o','r','o','o','o','r','r','o','o','o','o','o','o','o','o'],
  ['o','o','o','i','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','b','o','s','o','o','b','o','o','o','r','o','o','o','s','s','o','r','o','o','o','P'],
  ['o','o','o','o','o','o','o','o','o','o','o','o','r','r','o','o','o','o','o','o','o','r','o','o','o','o','o','r','o','o','o','r','o','b','o','s','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','r','p'],
  ['o','o','o','o','i','o','o','o','r','o','r','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','r','o','o','o','o','o','o','b','o','r','o','o','o','b','o','o','o','o','o','o','o','o','o','o','o','g','b','p'],
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','r','o','r','o','o','r','o','o','o','o','o','o','o','o','o','r','o','o','s','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','r','b','c','p'],
  ['o','o','o','r','r','r','P','r','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','o','o','b','b','b','b','s','b','o','o','o','o','o','o','o','o','o','o','o','o','o','o','p']
],[
  ['o','o','o','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','c','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','c','o','o','o','o','o','o','o','r','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','c','o','o','o','o','o','o','o','b','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','c','o','o','o','o','o','o','o','c','o','o','c','g','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','P'],
  ['o','o','o','c','o','o','o','o','o','r','o','g','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','r','o','o','o','r','o','o','g','o','o','o','o','o','o','o','o','s','s','c','o','o','o','o','o','o','g','p'],
  ['o','o','o','c','o','o','o','o','o','o','o','c','c','c','o','o','o','g','o','o','o','o','o','o','o','o','o','b','o','o','o','r','o','o','c','o','o','o','o','o','o','i','o','o','o','o','o','c','o','o','o','r','c','p'],
  ['o','o','o','c','o','o','o','o','c','o','o','o','o','o','o','o','o','o','o','g','g','s','c','s','r','s','s','r','o','o','r','r','s','s','o','o','o','o','o','o','o','i','o','o','o','o','b','o','o','o','g','c','b','p'],
  ['o','o','o','c','g','g','P','r','r','o','o','g','b','b','c','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','g','g','s','b','g','g','g','g','o','o','o','o','o','o','o','p']
],[
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','P'],
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','g','p'],
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','g','b','p'],
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','g','b','b','p'],
  ['g','g','g','g','g','g','P','g','g','g','g','b','b','b','b','b','b','b','b','b','b','c','c','c','c','c','c','c','c','c','c','r','r','r','r','r','r','r','r','r','r','i','i','i','i','i','i','i','i','i','o','o','o','p']
]]

load_screen('loading txt.json')

# stores words and randomly picks a word based on their probabilities for the start screen
class Message(object):
  def __init__(self, file="txt.json"):
    self.file = file
    try:
      x = self._read()
      load_screen('loaded txt.json')
    except:
      self._write({})
      
  def _read(self):
    txt = open(self.file,"r").read()
    j = json.loads(txt)
    load_screen('calculating word probabilities[ ]')
    LDTmp = 0
    #print(j)# = all words and probabilities
    check = 0
    for i in j:
      load_screen('calculating word probabilities[%s]' % LDTmp, LDTmp, True)
      LDTmp += 1
      check += j.get(i)
    #print(check)# = denominator for probability
    return j
    
  def _write(self, j):
    with open(self.file, "w+") as f:
      f.write(json.dumps(j))
  
  def add(self, msg, prob=5):
    old = self._read()
    old[msg] = prob
    self._write(old)
      
  def remove(self, msg):
    old = self._read()
    del old[msg]
    self._write(old)
  
  def _build(self):
    msgs = self._read()
    res = []
    for m in msgs:
      for i in range(msgs[m]):
        res.append(m)
    return res
  
  def get(self):
    return random.choice(self._build())
    load_screen('loaded word')

m = Message()
#m.add('jumpman V2',200)# add a word and probability
message = m.get()

load_screen('done')

pg.quit()

