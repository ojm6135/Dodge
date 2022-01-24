import pygame as pg
import random
import time


class Player:
    SPEED = 2.5
    
    def __init__(self):
        self.img = pg.image.load(r'C:\MyProjects\dodge\dodge\images\Spaceship.PNG')
        self.img_size = (25, 25)
        self.img = pg.transform.scale(self.img, self.img_size)
        
        self.pos_x = (screen_size[0] - self.img_size[0]) // 2 
        self.pos_y = (screen_size[1] - self.img_size[1]) // 2
        
    def move_up(self):
        self.pos_y -= Player.SPEED
    
    def move_down(self):
        self.pos_y += Player.SPEED
    
    def move_left(self):
        self.pos_x -= Player.SPEED
    
    def move_right(self):
        self.pos_x += Player.SPEED
        
    def get_size(self):
        return self.img_size

    def get_pos(self):
        return self.pos_x, self.pos_y
    
    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
    
    def show(self):
        screen.blit(self.img, (self.pos_x, self.pos_y))
        
    
class Dust:    
    def __init__(self):
        self.img = pg.image.load(f'C:\\MyProjects\\dodge\\dodge\\images\\asteroids/{["a", "b"][random.randint(0, 1)]}{random.randint(10000, 10015)}.png')
        self.img_size = (15, 15)
        self.img = pg.transform.scale(self.img, self.img_size)
        
        self.spawn_point = [ ( 0, random.randint(0, screen_size[1]) ), ( screen_size[0], random.randint(0, screen_size[0]) ),
                ( random.randint(0, screen_size[0]), 0 ), ( random.randint(0, screen_size[0]), screen_size[1] ) ]
        self.pos_x, self.pos_y = self.spawn_point[random.randint(0, 3)]
        
        self.dx = None
        self.dy = None
        
        self.SPEED = 3
        
        self.created_time = time.time()
        
    def remove(self):
        del self
        
    def get_size(self):
        return self.img_size
        
    def get_pos(self):
        return self.pos_x, self.pos_y
    
    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
    
    def set_direction(self, direction_x, direction_y):
        self.dx = self.SPEED * direction_x * random.uniform(0.50, 0.90)
        self.dy = self.SPEED * direction_y * random.uniform(0.50, 0.90)
    
    def move(self):
        self.pos_x += self.dx
        self.pos_y += self.dy
    
    def get_speed(self):
        return self.SPEED
    
    def get_time(self):
        return self.created_time

    def show(self):
        screen.blit(self.img, (self.pos_x, self.pos_y))

   
# 오브젝트가 화면을 넘어갔을 때 반대편에서 나오게 위치 조정
def reposition_obj(obj):
    x, y = obj.get_pos()
    
    if x < 0:
        obj.set_pos(x + screen_size[0], y)

    elif x > screen_size[0]:
        obj.set_pos(x - screen_size[0], y)

    elif y < 0:
        obj.set_pos(x, y + screen_size[1])

    elif y > screen_size[1]:
        obj.set_pos(x, y - screen_size[1])
        
   
def create_dust(k):
    if k % 10 == 0:
        dust = Dust()
        
        idx = random.randint(0, 7)
        dust.set_direction(directions[idx][0], directions[idx][1])  
              
        dust_li.append(dust)
        
        
def manage_dust():
    DURATION = 10
    
    remove_li = []
 
    curr = time.time()
    
    for dust in dust_li:
        # 위치 변경
        dust.move()
        reposition_obj(dust)
        
        # Dust 지속 시간 체크
        end = curr - dust.get_time()
        if end >= DURATION:
            remove_li.append(dust)
            
    # 생성된 지 DURATION초가 지난 Dust 삭제
    for dust in reversed(remove_li):
        dust_li.remove(dust)
            
            
def show_dust():
    for dust in dust_li:
        dust.show()
        
        
def is_crush(player):
    player_x, player_y = player.get_pos()
    player_w, player_h = player.get_size()
    
    for dust in dust_li:
        dust_x, dust_y = dust.get_pos()
        dust_w, dust_h = dust.get_size()
        
        if player_x <= dust_x <= (player_x + player_w - VALUE):
            if player_y <= dust_y <= (player_y + player_h - VALUE):
                return 1
            elif player_y + VALUE <= (dust_y + dust_h) <= (player_y + player_h):
                return 1
                             
        elif player_x + VALUE <= (dust_x + dust_w) <= (player_x + player_w):
            if player_y <= dust_y <= (player_y + player_h - VALUE):
                return 1
            elif player_y + VALUE <= (dust_y + dust_h) <= (player_y + player_h):
                return 1


def show_menu():
    global done
    
    background = pg.image.load(r'C:\MyProjects\dodge\dodge\images\MenuBackground.jpg')
    background = pg.transform.scale(background, (700, 700))
    
    start_font = pg.font.Font(r'C:\MyProjects\dodge\dodge\OpenSans-Regular.ttf', 30)
    quit_font = pg.font.Font(r'C:\MyProjects\dodge\dodge\OpenSans-Regular.ttf', 28)
    start_txt = 'Start:    SPACE'
    quit_txt = 'Quit:        ESC'
    width = pg.font.Font.size(start_font, start_txt)[0]
    height = pg.font.Font.get_height(start_font)
    start_text = start_font.render(start_txt, True, (255, 255, 255))
    quit_text = quit_font.render(quit_txt, True, (255, 255, 255))
    
    screen.blit(background, (0, 0))
    screen.blit(start_text, ( (screen_size[0] - width) / 2, (screen_size[1] / 2 - height / 2)) )
    screen.blit(quit_text, ( (screen_size[0] - width) / 2 + 10, (screen_size[1] / 2 + height*3/2)) )
    pg.display.flip()
    
    flag = False
    while not flag:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                flag = True
                done = True
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    flag = True
                    run_game()
                    
                elif event.key == pg.K_ESCAPE:
                    flag = True
                    done = True


def show_timer(start_t):
    global done
    
    font = pg.font.Font(r'C:\MyProjects\dodge\dodge\OpenSans-Regular.ttf', 25)
    end_t = time.time()
    txt = f'{end_t - start_t:.2f}'
    width = pg.font.Font.size(font, txt)[0]
    text = font.render(txt, True, (255, 255, 255))
    screen.blit(text, ( (screen_size[0] - width) / 2, screen_size[1] - 38) )


def show_gameover():
    global done
    
    # font_1 = pg.font.Font('OpenSans-Regular.ttf', 35)
    # txt_1 = 'Game Over'
    # width_1 = pg.font.Font.size(font_1, txt_1)[0]
    # height_1 = pg.font.Font.get_height(font_1)
    # text_1 = font_1.render(txt_1, True, (255, 255, 255))
    # screen.blit(text_1, ( (screen_size[0] - width_1) / 2, screen_size[1] / 2 - 180) )
    
    font_2 = pg.font.Font(r'C:\MyProjects\dodge\dodge\OpenSans-Regular.ttf', 27)
    txt_2 = 'Retry:   SPACE                       Menu:   ESC'
    width_2 = pg.font.Font.size(font_2, txt_2)[0]
    height_2 = pg.font.Font.get_height(font_2)
    text_2 = font_2.render(txt_2, True, (255, 255, 255))
    screen.blit(text_2, ( (screen_size[0] - width_2) / 2, screen_size[1] / 2 - height_2) )
    pg.display.flip()
    
    flag = True
    while flag:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                flag = False
                done = True
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    flag = False
                    run_game()
                    
                elif event.key == pg.K_ESCAPE:
                    flag = False
                    show_menu()
                                

def run_game():
    global done
    
    start_t = time.time()
    
    k = 0
    
    player = Player()
    move_direction = {pg.K_UP: False, pg.K_DOWN: False, pg.K_LEFT: False, pg.K_RIGHT: False}
    
    dust_li.clear()
    
    while not done:
        clock.tick(60)
        k += 1
              
        for event in pg.event.get():
            # 게임 종료
            if event.type == pg.QUIT:
                done = True
            
            # 방향키 입력
            if event.type == pg.KEYDOWN:
                move_direction[event.key] = True
                 
            elif event.type == pg.KEYUP:
                move_direction[event.key] = False
                
                
        # 플레이어 이동        
        if move_direction[pg.K_UP]:
            player.move_up()
                    
        if move_direction[pg.K_DOWN]:
            player.move_down()
            
        if move_direction[pg.K_LEFT]:
            player.move_left()
            
        if move_direction[pg.K_RIGHT]:
            player.move_right()
            

        # 플레이어가 화면을 넘어갔을 때
        reposition_obj(player)
        
        # Dust 생성, 관리
        create_dust(k)
        manage_dust()
        
        # 화면 업데이트   
        screen.blit(background_img, (0, 0))
        player.show()
        show_dust()
        show_timer(start_t)
        if is_crush(player):
               show_gameover()
        pg.display.flip()
        
        
# 초기화
pg.init()

# 환경 설정
pg.display.set_caption('Dodge')
screen_size = (640, 480)
screen = pg.display.set_mode(screen_size)
done = False
clock = pg.time.Clock()

VALUE = 10  # 충돌 계산 보정값
dust_li = []  # 생성된 Dust를 담는 리스트

# Dust의 이동 방향 - 동, 서, 남, 북, 동남, 동북, 서남, 서북
directions = [ (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1) ]

# 배경 설정
background_img = pg.image.load(r'C:\MyProjects\dodge\dodge\images\MainBackground.jpg')
background_img = pg.transform.scale(background_img, (screen_size[0], screen_size[1]))

        
if __name__ == '__main__':
    show_menu()
    pg.quit()