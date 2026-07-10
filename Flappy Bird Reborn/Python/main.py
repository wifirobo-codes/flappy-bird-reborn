import os, random, sys
try:
	import pygame
except ImportError:
	raise SystemExit(1)

pygame.init()
try:
	pygame.mixer.init()
except pygame.error:
	pass

WIDTH=432
HEIGHT=768
GROUND_H=120
FPS=60
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_ROOT=os.path.join(ROOT,"Assets")
HIGH_FILE=os.path.join(ROOT,"Python","highscore.txt")

def asset(name): return os.path.join(ASSET_ROOT,name)

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird Reborn")
clock=pygame.time.Clock()
font_big=pygame.font.SysFont("arial",52,bold=True)
font_small=pygame.font.SysFont("arial",28,bold=True)

bg_img=pygame.image.load(asset("background-day.png")).convert()
bg_img=pygame.transform.scale(bg_img,(WIDTH,HEIGHT-GROUND_H))
base_img=pygame.image.load(asset("base.png")).convert_alpha()
pipe_img=pygame.image.load(asset("pipe-green.png")).convert_alpha()
pipe_top_img=pygame.transform.flip(pipe_img,False,True)
bird_img=pygame.image.load(asset("yellowbird-upflap.png")).convert_alpha()
bird_img=pygame.transform.scale(bird_img,(36,26))
orb_img=pygame.image.load(asset("speed orb.png")).convert_alpha()
orb_img=pygame.transform.scale(orb_img,(26,26))
die_snd=None
if pygame.mixer.get_init(): die_snd=pygame.mixer.Sound(asset("die.wav"))

white=(255,255,255)
black=(20,20,20)
gold=(255,220,70)

bird_x=80
bird_r=18
boost_time=0.0
bg_x=0.0


def load_high():
	try:
		return int(open(HIGH_FILE,"r",encoding="utf-8").read().strip() or "0")
	except:
		return 0


def save_high(value):
	try:
		open(HIGH_FILE,"w",encoding="utf-8").write(str(value))
	except:
		pass


high_score=load_high()


def make_pipe(x):
	gap_y=random.randint(180,HEIGHT-GROUND_H-160)
	return {"x":x,"gap_y":gap_y,"scored":False,"orb":random.randint(1,30)==1,"orb_taken":False}


def reset():
	global boost_time
	boost_time=0.0
	return {"bird_y":HEIGHT*0.45,"vel":0.0,"pipes":[make_pipe(WIDTH+120),make_pipe(WIDTH+320),make_pipe(WIDTH+520)],"score":0,"state":"ready"}


g = reset()

def draw_bird(x,y,angle):
	rot=pygame.transform.rotozoom(bird_img,angle,1)
	rect=rot.get_rect(center=(x,y))
	screen.blit(rot,rect)


def draw_pipe(pipe):
	top_h=pipe["gap_y"]-130
	bottom_y=pipe["gap_y"]+130
	bottom_h=HEIGHT-GROUND_H-bottom_y
	top=pygame.transform.scale(pipe_top_img,(52,max(1,top_h)))
	bottom=pygame.transform.scale(pipe_img,(52,max(1,bottom_h)))
	screen.blit(top,(pipe["x"],0))
	screen.blit(bottom,(pipe["x"],bottom_y))
	if pipe.get("orb") and not pipe.get("orb_taken"):
		orb_y=pipe["gap_y"]
		orb_x=pipe["x"]+12
		screen.blit(orb_img,(orb_x,orb_y-13))


def pipe_rects(pipe):
	top_h=pipe["gap_y"]-130
	bottom_y=pipe["gap_y"]+130
	bottom_h=HEIGHT-GROUND_H-bottom_y
	return [pygame.Rect(pipe["x"],0,52,top_h),pygame.Rect(pipe["x"],bottom_y,52,bottom_h)]


def orb_rect(pipe):
	return pygame.Rect(pipe["x"]+3,pipe["gap_y"]-10,26,26)


def start():
	if g["state"]=="ready": g["state"]="play"


running=True
while running:
	clock.tick(FPS)
	if boost_time>0:
		boost_time-=1/60
		if boost_time<0:
			boost_time=0
	for event in pygame.event.get():
		if event.type==pygame.QUIT: running=False
		if event.type==pygame.KEYDOWN:
			if event.key in (pygame.K_SPACE,pygame.K_UP,pygame.K_w):
				if g["state"]=="dead": g=reset()
				g["vel"]=-8.8
				start()
			if event.key==pygame.K_r and g["state"]=="dead": g=reset()

	if g["state"]=="play":
		g["vel"]+=0.45
		if g["vel"]>10: g["vel"]=10
		g["bird_y"]+=g["vel"]
		speed=3.2+(1.1 if boost_time>0 else 0)
		for pipe in g["pipes"]:
			pipe["x"]-=speed
			if pipe["x"]<-70: pipe.update(make_pipe(WIDTH+120))
			if not pipe["scored"] and pipe["x"]+52<bird_x:
				pipe["scored"]=True
				g["score"]+=2 if boost_time>0 else 1
		bird_rect=pygame.Rect(bird_x-bird_r,int(g["bird_y"])-bird_r,bird_r*2,bird_r*2)
		if bird_rect.top<=0 or bird_rect.bottom>=HEIGHT-GROUND_H:
			if die_snd: die_snd.play()
			if g["score"]>high_score:
				high_score=g["score"]
				save_high(high_score)
			g["state"]="dead"
		for pipe in g["pipes"]:
			if pipe.get("orb") and not pipe.get("orb_taken") and bird_rect.colliderect(orb_rect(pipe)):
				pipe["orb_taken"]=True
				boost_time=2.0
				g["vel"]-=2.0
			for rect in pipe_rects(pipe):
				if bird_rect.colliderect(rect):
					if die_snd: die_snd.play()
					if g["score"]>high_score:
						high_score=g["score"]
						save_high(high_score)
					g["state"]="dead"

	bg_x-=0.6
	if bg_x<=-WIDTH:
		bg_x=0
	screen.blit(bg_img,(int(bg_x),0))
	screen.blit(bg_img,(int(bg_x)+WIDTH,0))
	for pipe in g["pipes"]: draw_pipe(pipe)
	base_x=0
	while base_x<WIDTH:
		screen.blit(base_img,(base_x,HEIGHT-GROUND_H))
		base_x+=base_img.get_width()
	angle=max(-35,min(90,-g["vel"]*4))
	draw_bird(bird_x,g["bird_y"],angle)
	score_surface=font_big.render(str(g["score"]),True,white)
	score_shadow=font_big.render(str(g["score"]),True,black)
	score_rect=score_surface.get_rect(center=(WIDTH//2,90))
	screen.blit(score_shadow,score_rect.move(3,3))
	screen.blit(score_surface,score_rect)
	high_surface=font_small.render("best "+str(high_score),True,white)
	high_shadow=font_small.render("best "+str(high_score),True,black)
	high_rect=high_surface.get_rect(center=(WIDTH//2,130))
	screen.blit(high_shadow,high_rect.move(2,2))
	screen.blit(high_surface,high_rect)
	if boost_time>0:
		x2a=font_big.render("x2",True,gold)
		x2b=font_big.render("x2",True,black)
		x2r=x2a.get_rect(center=(bird_x+48,int(g["bird_y"])-32))
		screen.blit(x2b,x2r.move(3,3))
		screen.blit(x2a,x2r)
	if g["state"]=="ready":
		text=font_small.render("press space",True,white)
		shadow=font_small.render("press space",True,black)
		rect=text.get_rect(center=(WIDTH//2,HEIGHT//2-40))
		screen.blit(shadow,rect.move(2,2))
		screen.blit(text,rect)
	elif g["state"]=="dead":
		panel=pygame.Surface((330,170),pygame.SRCALPHA)
		panel.fill((0,0,0,110))
		screen.blit(panel,(51,250))
		t1=font_small.render("game over",True,white)
		t2=font_small.render("space or r to restart",True,white)
		screen.blit(t1,t1.get_rect(center=(WIDTH//2,305)))
		screen.blit(t2,t2.get_rect(center=(WIDTH//2,350)))
	pygame.display.flip()

	if g["state"]=="dead" and g["score"]>high_score:
		high_score=g["score"]
		save_high(high_score)

pygame.quit()
sys.exit()
