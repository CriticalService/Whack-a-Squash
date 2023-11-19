import pygame
from random import randint
import time
import sys

# 初始化游戏
pygame.init()

# 设置屏幕尺寸和标题
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("KillWG")

# 加载图片
background = pygame.image.load(r"source/bg.png")
wg_image = pygame.image.load(r"source/wog2.png")

# 加载声音
wgBoom = pygame.mixer.Sound(r"source/boom.wav")
bgm = pygame.mixer.Sound(r"source/bgmusic.ogg")

# 窝瓜类
class Wogua(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = wg_image
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, screen_width - self.rect.width)
        self.rect.y = randint(0, screen_height - self.rect.height)

    def update(self):
        self.rect.x = randint(0, screen_width - self.rect.width)
        self.rect.y = randint(0, screen_height - self.rect.height)

# 播放音频
def playSound(sound, volume = 1):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(volume)
    channel.play(sound)

# 主循环
def main():
    tick = 1
    startTime = time.time()
    fr = pygame.time.Clock()
    playSound(bgm, 1)
    global running,score
    while running:
            
        #fr.tick(tick)
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if wg.rect.collidepoint(mouse_pos):
                    score = score + 10
                    tick += 0.015
                    playSound(wgBoom, 1)
                    all_wg.update()
                    
        # 计算剩余时间
        remainTime = 61 - (time.time() - startTime)
        print(remainTime)
        if remainTime < 0:
            running = False
            break
        
        # 更新地鼠位置
        all_wg.update(tick = 30)

        # 绘制背景
        screen.blit(background, (0, 0))

        # 绘制窝瓜
        all_wg.draw(screen)

        # 绘制分数
        score_text = defaultFont.render(f"Score: {score}", True, (250, 255, 255))
        screen.blit(score_text, (10, 10))

        # 绘制剩余时间
        remainTime_text = defaultFont.render("Time: {:.0f}".format(remainTime), True, (255, 255, 255))
        screen.blit(remainTime_text, (10, 60))

        # 刷新屏幕
        pygame.display.flip()
        
# 重新开始
def replay():
    global running
    while running==False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 250 < mouseX < 400 and 350 < mouseY <400:
                    score = 0
                    running = True
                    print(running)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# 定义各种文字
defaultFont = pygame.font.Font(None ,50)

# 创建窝瓜组
all_wg = pygame.sprite.Group()

# 创建多个窝瓜实例并加入窝瓜组
for _ in range(1):
    wg = Wogua()
    all_wg.add(wg)

# 游戏主循环
running = True
score = 0
while running == True:
    score = 0
    main()
    pygame.mixer.stop()

    # 读取最高记录
    recordFile = open(r"source/record.txt")
    record = int(recordFile.read())
    print('Best:',record)
    recordFile.close()

    # 结束页面
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # 显示分数及历史最高
    if score > record:
        record = score
        recordFile = open(r"source/record.txt", 'w')
        recordFile.write(str(record)) # 写入最高纪录
        recordFile.close()
        score_text = defaultFont.render(f"Final Score: {score}<NEW RECORD! >]", True, (255, 255, 255))
    else:
        score_text = defaultFont.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (250, 250))
    record_text = defaultFont.render(f"Best: {record}", True, (255 ,255, 255))
    screen.blit(record_text, (250 ,300))

    # 重玩与退出按钮
    pygame.draw.rect(screen, (0, 0, 0), (250, 350, 150, 50))
    replayButton_text = defaultFont.render("Replay", True, (255, 255, 255))
    screen.blit(replayButton_text, (250, 350))
    pygame.display.flip()
    time.sleep(2)
    
    replay()

while running == False:
    pygame.quit()
    sys.exit()
    break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        else:
            pass
