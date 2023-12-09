import pygame, time, sys
from random import randint

# 初始化游戏
pygame.init()

# 设置屏幕尺寸和标题
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("KillWG")

# 加载图片
background = pygame.image.load(r"source/bg.png")
wg_image = pygame.image.load(r"source/squash.png")
wg_squeeze = pygame.transform.scale(wg_image, (50, 25))
playButton = pygame.transform.scale(pygame.image.load(r"source/playbutton.png"), (159, 54))
replayButton = pygame.transform.scale(pygame.image.load(r"source/replaybutton.png"), (147, 50))
quitButton = pygame.transform.scale(pygame.image.load(r"source/quitbutton.png"), (147, 50))

# 加载声音
wgBoom = pygame.mixer.Sound(r"source/boom.wav")
#bgm = pygame.mixer.Sound(r"source/bgmusic.ogg")
easteregg = pygame.mixer.Sound(r"source/easteregg.ogg")
pygame.mixer.music.load(r"source/bgmusic.ogg")

# 定义各种文字
defaultFont = pygame.font.Font(None ,50)
logoFont = pygame.font.Font(r"source/Silver.ttf", 100)

# 播放音频
def playSound(sound, volume = 1):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(volume)
    channel.play(sound)
                
# 窝瓜类
class Wogua(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = wg_image
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, screen_width - self.rect.width)
        self.rect.y = randint(0, screen_height - self.rect.height)
        self.lastTime = 0

    def update(self):
        self.rect.x = randint(0, screen_width - self.rect.width)
        self.rect.y = randint(0, screen_height - self.rect.height)

# 主循环
def main():
    #playSound(bgm, 1)
    global running, score, brokeRecord

    # 根据是否打破纪录判断是否需要重播BGM
    if brokeRecord == True:
        pygame.mixer.stop()
        pygame.mixer.music.play(-1)

    # 开玩倒计时
    screen.blit(background, (0, 0))
    timerFont = pygame.font.Font(None, 100)
    for i in range(1, 4):
        pygame.draw.circle(screen, (255, 255, 255), (400, 300), 100)
        timer_text = timerFont.render(str(4-i), True, (0, 0, 0))
        screen.blit(timer_text, (375, 275))
        pygame.display.flip()
        time.sleep(1)
    
    tick = 1
    startTime = time.time()
    lastTime = startTime
    consistency = 0

    while running:
            
        ticks = pygame.time.get_ticks()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if wg.rect.collidepoint(mouse_pos): # 如果命中
                    score = score + 10
                    #tick -= 0.015
                    if tick>0.7:
                        tick = tick*0.97
                    print("[Tick]", tick)
                    consistency += 1
                    # 绘制压扁图像、分数及剩余时间
                    screen.blit(background, (0, 0))
                    screen.blit(wg_squeeze, (wg.rect.x, wg.rect.y + 25))
                    score_text = defaultFont.render(f"Score: {score}", True, (250, 255, 255))
                    screen.blit(score_text, (10, 10))
                    remainTime_text = defaultFont.render("Time: {:.0f}".format(remainTime), True, (255, 255, 255))
                    screen.blit(remainTime_text, (10, 60))
                    playSound(wgBoom, 1)# 播放音效
                    all_wg.update()
                    pygame.display.flip()
                    time.sleep(0.5)
            
        # 计算剩余时间
        currentTime = time.time()
        remainTime = 60 - (currentTime - startTime)
        #print("[Remaintime]", remainTime)
        if remainTime <= 0:
            running = False
            break
        
        # 更新窝瓜位置
        if currentTime - lastTime > tick:
            lastTime = currentTime
            all_wg.update()

        # 绘制各种图像
        screen.blit(background, (0, 0))
        all_wg.draw(screen)
        score_text = defaultFont.render(f"Score: {score}", True, (250, 255, 255))
        screen.blit(score_text, (10, 10))
        remainTime_text = defaultFont.render("Time: {:.0f}".format(remainTime), True, (255, 255, 255))
        screen.blit(remainTime_text, (10, 60))

        # 刷新屏幕
        pygame.display.flip()

        #time.sleep(tick)
        
# 重新开始
def replay():
    global running
    while running == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 250 < mouseX < 400 and 350 < mouseY <400:
                    print("Replay clicked")
                    running = True
                elif 250 < mouseX < 400 and 400 < mouseY < 450:
                    print("Quit clicked")
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# 创建窝瓜组
all_wg = pygame.sprite.Group()

# 创建多个窝瓜实例并加入窝瓜组
for _ in range(1):
    wg = Wogua()
    all_wg.add(wg)

# 起始界面
pygame.mixer.music.play(-1)
screen.blit(background, (0, 0))
start = False
while start == False:
    fr = pygame.time.Clock()
    fr.tick(1)
    all_wg.draw(screen)
    all_wg.update()
    logo_text = logoFont.render("Whack a Squash", True, (255, 255, 255))
    screen.blit(logo_text, (200, 50))
    screen.blit(playButton, (800/2-318/4, 600/2-108/4+150))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if 800/2-318/4 < mouseX < 800/2-318/4+318/2 and 600/2-108/4+150 < mouseY < 600/2-108/4+150+108/2:
                start = True
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# 游戏主循环
running = True
score = 0
brokeRecord = False
keys = pygame.key.get_pressed()

while running == True:
    score = 0
    main()

    # 结束页面
    screen.blit(background, (0, 0))
    timeout_text = defaultFont.render("TIME OUT", True, (255, 255, 255))
    screen.blit(timeout_text, (325, 300))
    pygame.display.flip()
    time.sleep(2)
    screen.blit(background, (0, 0))

    # 读取最高记录
    recordFile = open(r"source/record.txt")
    record = int(recordFile.read())
    print('Best:', record)
    recordFile.close()

    # 显示分数及历史最高
    if score > record:
        record = score
        recordFile = open(r"source/record.txt", 'w')
        recordFile.write(str(record)) # 写入最高纪录
        recordFile.close()
        score_text = defaultFont.render(f"Final Score: {score}", True, (255, 255, 255))
        congratultion_text = defaultFont.render("NEW RECORD!", True, (255, 0, 0))
        screen.blit(congratultion_text, (250, 200))
        pygame.mixer.music.stop()
        playSound(easteregg, 1)
        brokeRecord = True
    else:
        score_text = defaultFont.render(f"Final Score: {score}", True, (255, 255, 255))
        brokeRecord = False
    screen.blit(score_text, (250, 250))
    record_text = defaultFont.render(f"Best: {record}", True, (255 ,255, 255))
    screen.blit(record_text, (250 ,300))

    # 重玩与退出按钮
    '''
    pygame.draw.rect(screen, (0, 0, 0), (250, 350, 150, 50))
    replayButton_text = defaultFont.render("Replay", True, (255, 255, 255))
    screen.blit(replayButton_text, (250, 350))

    pygame.draw.rect(screen, (0, 0, 0), (250, 400, 150, 50))
    quitButton_text = defaultFont.render("Quit", True, (255, 255, 255))
    screen. blit(quitButton_text, (250, 400))

    pygame.display.flip()
    '''

    screen.blit(replayButton, (250, 350))
    screen.blit(quitButton, (250, 400))
    pygame.display.flip()

    replay()

while running == False:
    pygame.quit()
    sys.exit()
