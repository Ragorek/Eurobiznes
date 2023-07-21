import pygame, random

pygame.init()
pygame.display.set_caption("Eurobiznes")
pygame.display.set_mode([13*54,13*54])
window_size,winx,winy = 0,pygame.display.get_window_size()[0],pygame.display.get_window_size()[1]
arew,areh = winx*1/13,winy*1/13

class eurobiznes():
    window = pygame.display.get_surface()
    FPS = 30
    window_count = 1
   
    class buttons():
        def __init__(self,px,py,sx,sy,msg):
            self.px = px
            self.py = py
            self.sx = sx
            self.sy = sy
            self.color = [225,225,225]
            self.chcolor =  [255,255,255]
            self.msg = msg
            self.font = pygame.font.SysFont('arial',20)
            self.text = self.font.render(self.msg,True,[0,0,0])

        def change_win(x):
            eurobiznes.window_count = x

        def quit():
            quit()

        def draw_button(self):
            mouse_px = pygame.mouse.get_pos()[0]
            mouse_py = pygame.mouse.get_pos()[1]
            mouse_lc = pygame.mouse.get_pressed()[0]

            pygame.draw.rect(eurobiznes.window,self.color,[self.px-self.sx/2,self.py-self.sy/2,self.sx,self.sy])

            if (self.px-self.sx/2 < mouse_px < self.px+self.sx/2 and self.py-self.sy/2 < mouse_py < self.py+self.sy/2):
                pygame.draw.rect(eurobiznes.window,self.chcolor,[self.px-self.sx/2,self.py-self.sy/2,self.sx,self.sy])

                if (mouse_lc == 1):
                    if(self.msg == "STARTUJ"):
                        for player in eurobiznes.players.players:
                            eurobiznes.players.position_player(player)
                        eurobiznes.buttons.change_win(2)

                    if(self.msg == "WYJDŹ"):
                        eurobiznes.buttons.quit()

                    if(self.msg == "POWRÓT"):
                        eurobiznes.buttons.change_win(1)

                    if(self.msg == "2 graczy"):
                        player1.active = 3
                        player2.active = 1
                        eurobiznes.players.players.remove(player3)
                        eurobiznes.players.players.remove(player4)
                        eurobiznes.buttons.change_win(3)

                    if(self.msg == "3 graczy"):
                        player1.active = 3
                        player2.active = 1
                        player3.active = 1
                        eurobiznes.players.players.remove(player4)
                        eurobiznes.buttons.change_win(3)

                    if(self.msg == "4 graczy"):
                        player1.active = 3
                        player2.active = 1
                        player3.active = 1
                        player4.active = 1
                        eurobiznes.buttons.change_win(3)

                    if(self.msg == "Kostki"):
                        for player in eurobiznes.players.players:
                            if(player.active > 1):
                                dice1 = random.randrange(1,7)
                                dice2 = random.randrange(1,7)
                                eurobiznes.info.roll[0] = dice1
                                eurobiznes.info.roll[1] = dice2
                                eurobiznes.info.draw_dice(eurobiznes.info.roll[0],0)
                                eurobiznes.info.draw_dice(eurobiznes.info.roll[1],1)
                                if(player.active == 3):
                                    if(player.prisoner == 0):
                                        eurobiznes.info.info_msg = player.name +" wrzucił " + str(dice1) + " i " + str(dice2) + " !"
                                        if(dice1 == dice2):
                                            player.repeats_count += 1
                                            if(player.repeats_count == 2):
                                                player.position = 11
                                                player.prisoner = 2
                                            else:
                                                player.move(dice1,dice2)
                                    
                                        else:
                                            player.move(dice1,dice2)
                                            player.active = 2
                                    else:
                                        
                                        if(dice1 == dice2 and dice1 == 6):
                                            player.prisoner = 0
                                            eurobiznes.info.info_msg = "Udało ci się uciec z więzienia !"
                                        else:
                                            player.active = 2
                                    player.position_player()
                    
                    if(self.msg == "Kup"):
                        for player in eurobiznes.players.players:
                            if(player.active > 1):
                                player.buy_field()

                    if(self.msg == "Ulepsz"):
                        for player in eurobiznes.players.players:
                            if(player.active > 1):
                                player.upgrade()
                    if(self.msg == "Zdegraduj"):
                        for player in eurobiznes.players.players:
                            if(player.active > 1):
                                player.degrade()
                           
                    if(self.msg == "Koniec tury"):
                        for player in eurobiznes.players.players:
                            if(player.active == 2):
                                if (player.upgrade_mode == True):
                                    player.upgrade()
                                player.active = 1
                                player.repeats_count = 0
                                if(player.prisoner > 0):
                                    player.prisoner -= 1
                                eurobiznes.info.info_msg = "Koniec tury dla " + player.name + " !"
                                try:                            
                                    eurobiznes.players.players[eurobiznes.players.players.index(player) + 1].active = 3
                                    break
                                except:
                                    eurobiznes.players.players[0].active = 3
                            
            
            textxy = self.text.get_rect()
            textxy.center = [self.px,self.py]
            eurobiznes.window.blit(self.text,textxy)

    class players():
        players = []

        def __init__(self,color):
            self.color = color
            self.money = 2000
            self.active = 0
            self.position = 1
            self.px = 0
            self.py = 0
            eurobiznes.players.players.append(self)
            self.number = eurobiznes.players.players.index(self) + 1
            self.name = "Gracz "+str(self.number)
            self.own = []
            self.stations_count = 0
            self.source_count = 0
            self.repeats_count = 0
            self.prisoner = 0
            self.upgrade_mode = False
            self.degrade_mode = False

        def buy_field(self):
            for field in eurobiznes.fields.fields:
                if(field.number == self.position):
                    if(field.cost != 0):
                        if(self.money >= field.cost):
                            can = True
                            for player in eurobiznes.players.players:
                                if(player != self):
                                    for owned_field in player.own:
                                        if(owned_field == field):
                                            eurobiznes.info.info_msg = "Już " + player.name + "posiada to pole !"
                                            can = False
                                else:
                                    for owned_field in player.own:
                                        if(owned_field == field):
                                            eurobiznes.info.info_msg = "Już posiadasz to pole !"
                                            can = False
                            if(can):
                                self.own.append(field)
                                self.money = self.money - field.cost
                                field.owner = self.name
                                if(field.number == 6 or field.number == 16 or field.number == 26 or field.number == 36):
                                    self.stations_count += 1
                                if(field.number == 13 or field.number == 29):
                                    self.source_count += 1
                                eurobiznes.info.info_msg = "Pole zostało zakupione !"
                        else:
                            eurobiznes.info.info_msg = "Brakuje ci " + str(field.cost - self.money) + " by kupić to pole !"
                    else:
                        eurobiznes.info.info_msg = "Nie możesz kupić pola " + field.msg + "!"
        
        def upgrade(self):
            if(self.upgrade_mode):
                upgrade.text = upgrade.font.render(upgrade.msg,True,[0,0,0])
                self.upgrade_mode = False
            else:
                upgrade.text = upgrade.font.render(upgrade.msg,True,[255,0,0])
                self.upgrade_mode = True
                degrade.text = degrade.font.render(degrade.msg,True,[0,0,0])
                self.degrade_mode = False
        
        def degrade(self):
            if(self.degrade_mode):
                degrade.text = degrade.font.render(degrade.msg,True,[0,0,0])
                self.degrade_mode = False
            else:
                degrade.text = degrade.font.render(degrade.msg,True,[255,0,0])
                self.degrade_mode = True
                upgrade.text = upgrade.font.render(upgrade.msg,True,[0,0,0])
                self.upgrade_mode = False
        def redcart():
            pass

        def move(self,dice1,dice2):
            self.position = self.position + dice1 + dice2
            if(self.position == 31):
                self.position = 11
                self.prisoner = 2
                eurobiznes.info.info_msg = "Trafiłeś do więzienia !"
            if(self.position > 40):
                self.position = self.position%40
                self.money = self.money + 400
            if(self.position == 8 or self.position == 23):
                self.redcart()
            for field in eurobiznes.fields.fields:
                if(self.position == field.number and field.owner != "Nikt" and field.owner != self.name):
                    if(field.number == 6 or field.number == 16 or field.number == 26 or field.number == 36):
                        for player in eurobiznes.players.players:
                            if(field in player.own):
                                player.money += 50 * player.stations_count
                                self.money -= 50 * player.stations_count
                    if(field.number == 13 or field.number == 29):
                        for player in eurobiznes.players.players:
                            if(field in player.own):
                                player.money += (dice1+dice2)*player.source_count*10
                                self.money -= (dice1+dice2)*player.source_count*10
                    elif(field.lvl == 0):
                        self.money = self.money - field.pay0
                        for player in eurobiznes.players.players:
                            if(field in player.own):
                                player.money = player.money + field.pay0
                    elif(field.lvl == 1):
                        self.money = self.money - field.pay1
                        for player in eurobiznes.players.players:
                            if(field in player.own):
                                player.money = player.money + field.pay1
                    elif(field.lvl == 2):
                        self.money = self.money - field.pay2
                        for player in eurobiznes.players.players:
                            if(field in player.own):
                                player.money = player.money + field.pay2
                    elif(field.lvl == 3):
                        self.money = self.money - field.pay3
                        for player in eurobiznes.players.players:
                            if(field in player.own):
                                player.money = player.money + field.pay3
                    elif(field.lvl == 4):
                        self.money = self.money - field.pay4
                        for player in eurobiznes.players.players:
                            if(field in player.own):
                                player.money = player.money + field.pay4
                    else:
                        self.money = self.money - field.pay5
                        for player in eurobiznes.players.players:
                            if(field in player.own):
                                player.money = player.money + field.pay5

            if(self.position == 5):
                self.money -= 400
            if(self.position == 39 and self.money > 1000):
                self.money -= 200

        def position_player(self):
            px = eurobiznes.fields.fields[self.position-1].px
            py = eurobiznes.fields.fields[self.position-1].py
            
            sx = eurobiznes.fields.fields[self.position-1].sx
            sy = eurobiznes.fields.fields[self.position-1].sy
            if (self.number == 1):
                self.px = px + sx*1.1/3 
                self.py = py + sy*1.1/3
            elif (self.number == 2):
                self.px = px + sx*1.9/3
                self.py = py + sy*1.1/3
            elif (self.number == 3):
                self.px = px + sx*1.1/3
                self.py = py + sy*1.9/3
            else :
                self.px = px + sx*1.9/3
                self.py = py + sy*1.9/3
            
        def draw_players():
            for player in eurobiznes.players.players:
                if (player.active > 0):
                    pygame.draw.circle(eurobiznes.window,player.color,[player.px,player.py],arew*1/8)

    class fields():
        fields = []
        def __init__(self,px,py,sx,sy,fc,msg,cost,pay0,pay1,pay2,pay3,pay4,pay5):
            self.px = px
            self.py = py
            self.sx = sx
            self.sy = sy
            self.fc = fc
            self.msg = msg
            self.cost = cost
            self.pay0 = pay0
            self.pay1 = pay1 
            self.pay2 = pay2
            self.pay3 = pay3
            self.pay4 = pay4
            self.pay5 = pay5
            self.lvl = 0
            self.owner = "Nikt"
            eurobiznes.fields.fields.append(self)
            self.number = eurobiznes.fields.fields.index(self) + 1
            if (self.number != 0 and self.number != 10 and self.number != 20 and self.number != 30):
                self.font = pygame.font.SysFont('arial',13)
            else:
                self.font = pygame.font.SysFont('arial',14)
            if(self.fc == [255,255,0]):
                self.country = "Grecja"
            elif(self.fc == [255,0,0]):
                self.country = "Wlochy"
            elif(self.fc == [0,0,255]):
                self.country = "Hiszpania"
            elif(self.fc == [254,127,0]):
                self.country = "Anglia"
            elif(self.fc == [0,255,0]):
                self.country = "Benelux"
            elif(self.fc == [255,0,255]):
                self.country = "Szwecja"
            elif(self.fc == [150,75,0]):
                self.country = "RFN"
            elif(self.fc == [0,0,0]):
                self.country = "Austria"
            else: self.country = ""
            
            if(self.cost != 0 and self.number != 6 and 1 < self.number < 11 ):
                self.house = 100
            elif(self.cost != 0 and self.number != 13 and self.number != 16 and 11 < self.number < 21):
                self.house = 200
            elif(self.cost != 0 and self.number != 26 and self.number != 29 and 21 < self.number < 31):
                self.house = 300
            elif(self.cost != 0 and self.number != 36):
                self.house = 400
            else:
                self.house = 0

            self.hotel = 5 * self.house

        def draw_fields():
            for field in eurobiznes.fields.fields:
                pygame.draw.rect(eurobiznes.window,[255,255,255],[field.px,field.py,field.sx,field.sy])
 
                field_number = pygame.font.SysFont('arial',12).render(str(field.number),True,[0,0,0])
                field_name = field.font.render(field.msg,True,[0,0,0])
                field_number_xy = field_number.get_rect()
                field_name_xy = field_name.get_rect()

                mouse_px = pygame.mouse.get_pos()[0]
                mouse_py = pygame.mouse.get_pos()[1]

                if(field.number == 1):
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px,field.py-1],[field.px+field.sx,field.py-1],2) #up
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px-1,field.py],[field.px-1,field.py+field.sy],2) #left
                    field_number_xy.center = [field.px+field.sx-10,field.py+field.sy-10]
                    field_name_xy.center = [field.px+field.sx/2,field.py+field.sy/2]
                if(1 < field.number < 11 ):
                    if(field.number != 3 and field.number !=5 and field.number != 6 and field.number !=8):
                        pygame.draw.rect(eurobiznes.window,field.fc,[field.px,field.py,field.sx,areh*1/2])
                        pygame.draw.line(eurobiznes.window,[0,0,0],[field.px,field.py+areh*1/2-1],[field.px+field.sx,field.py+areh*1/2-1],2) #between
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px,field.py-1],[field.px+field.sx,field.py-1],2)
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px-1,field.py],[field.px-1,field.py+field.sy],2) 
                    field_number_xy.center = [field.px+field.sx/2,field.py+field.sy-10]
                    field_name_xy.center = [field.px+field.sx/2,field.py+field.sy-25]
                if(field.number == 11):
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px,field.py-1],[field.px+field.sx,field.py-1],2)
                    field_number_xy.center = [field.px+10,field.py+field.sy-10]
                    field_name_xy.center = [field.px+field.sx/2,field.py+field.sy/2]
                if(11 < field.number < 21):
                    if(field.number != 13 and field.number != 16 and field.number != 18):
                        pygame.draw.rect(eurobiznes.window,field.fc,[field.px+field.sx*3/4,field.py,arew*1/2,field.sy])
                        pygame.draw.line(eurobiznes.window,[0,0,0],[field.px+arew*1.5-1,field.py],[field.px+arew*1.5-1,field.py+field.sy],2)
                    pygame.draw.line(eurobiznes.window,[0,0,0],[0,field.py-1],[field.sx,field.py-1],2)
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px+field.sx-1,field.py],[field.px+field.sx-1,field.sy],2)     
                    field_number_xy.center = [10,field.py+field.sy/2]
                    field_name_xy.center = [field.px+field.sx*2/5,field.py+field.sy-10]
                if(field.number == 21):
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px-1,0],[field.px-1,field.sy],2)
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px+field.sx-1,field.py],[field.px+field.sx-1,field.py+field.sy],2)
                    field_number_xy.center = [10,10]
                    field_name_xy.center = [field.px+field.sx/2,field.py+field.sy/2]
                if(21 < field.number < 31):
                    if(field.number != 23 and field.number !=26 and field.number != 29):
                        pygame.draw.rect(eurobiznes.window,field.fc,[field.px,field.py+field.sy*3/4,field.sx,areh*1/2])
                        pygame.draw.line(eurobiznes.window,[0,0,0],[field.px,field.py+areh*1.5],[field.px+field.sx,field.py+areh*1.5],2)
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px,field.py+field.sy-1],[field.px+field.sx,field.py+field.sy-1],2)
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px+field.sx-1,field.py],[field.px+field.sx-1,field.py+field.sy],2)
                    field_number_xy.center = [field.px+field.sx/2,10]  
                    field_name_xy.center = [field.px+field.sx/2,25]            
                if(field.number == 31):
                    field_number_xy.center = [field.px+field.sx-10,10]
                    field_name_xy.center = [field.px+field.sx/2,field.py+field.sy/2]
                if(31 < field.number < 41):
                    if(field.number != 34 and field.number != 36 and field.number != 37 and field.number != 39 ):
                        pygame.draw.rect(eurobiznes.window,field.fc,[field.px,field.py,arew*1/2,field.sy])
                        pygame.draw.line(eurobiznes.window,[0,0,0],[field.px+arew*1/2-1,field.py],[field.px+arew*1/2-1,field.py+field.sy],2)
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px,field.py-1],[field.px+field.sx,field.py-1],2)
                    pygame.draw.line(eurobiznes.window,[0,0,0],[field.px-1,field.py],[field.px-1,field.py+field.sy],2)
                    field_number_xy.center = [field.px+field.sx-10,field.py+field.sy/2]
                    field_name_xy.center = [field.px+field.sx*3/5,field.py+field.sy-10]

                eurobiznes.window.blit(field_number,field_number_xy)
                eurobiznes.window.blit(field_name,field_name_xy)

                if(field.px < mouse_px < field.px+field.sx and field.py < mouse_py < field.py+field.sy and field.number != 31 and field.number != 21 and field.number != 11 and field.number != 1):
                    eurobiznes.info.draw_info(field)
                    mouse_click = pygame.mouse.get_pressed()[0]
                    for player in eurobiznes.players.players:
                        if(field.cost != 0 and field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36 and player.upgrade_mode and mouse_click == 1):
                            if(field in player.own):
                                if(field.lvl < 4):
                                    if(player.money >= field.house):
                                        field.lvl = field.lvl + 1
                                        player.money = player.money - field.house
                                        eurobiznes.info.info_msg = "Zakupiono domek"
                                    else:
                                        eurobiznes.info.info_msg = "Nie masz wystarczająco pieniędzy na dodanie domku"
                                elif(field.lvl == 4):
                                    if(player.money >= field.hotel):
                                        field.lvl = field.lvl + 1
                                        player.money = player.money - field.hotel
                                        eurobiznes.info.info_msg = "Zakupiono hotel"
                                    else:
                                        eurobiznes.info.info_msg = "Nie masz wystarczająco pieniędzy na dodanie hotelu"
                                else:
                                        eurobiznes.info.info_msg = "Nie da się bardziej ulepszyć pola"
                            else:
                                 eurobiznes.info.info_msg = "Nie posiadasz tego pola"
                        if(field.cost != 0 and field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36 and player.degrade_mode and mouse_click == 1):
                            if(field in player.own):
                                if(field.lvl == 5):
                                    field.lvl = field.lvl - 1
                                    player.money = player.money + int(field.hotel/2)
                                    eurobiznes.info.info_msg = "Sprzedano hotel !"  
                                elif(field.lvl > 0):
                                    field.lvl = field.lvl - 1
                                    player.money = player.money + int(field.house/2)
                                    eurobiznes.info.info_msg = "Sprzedano domek"
                                else:
                                    eurobiznes.info.info_msg = "Pole nie posiada zabudowań do sprzedania !"
                            else:
                                 eurobiznes.info.info_msg = "Nie posiadasz tego pola"
    class info():
        roll = [0,0]
        info_msg = ""
        def __init__():
            pass

        def draw_info_msg():

            font = pygame.font.SysFont('arial',16)

            text1 = font.render(eurobiznes.info.info_msg,True,[0,0,0])
            text1xy = text1.get_rect()
            text1xy.center = [arew*5,areh*10]

            for player in eurobiznes.players.players:
                if(player.active > 1):    
                    text2 = font.render("Twoja gotówka: " + str(player.money),True,[0,0,0])
                    text2xy = text1.get_rect()
                    text2xy.bottomleft = [arew*2.5,areh*9]

            eurobiznes.window.blit(text1,text1xy)
            eurobiznes.window.blit(text2,text2xy)

        def draw_dice(dice,x):
            color = [0,0,0]
            if (x == 0):
                px = arew*9
            else: 
                px = arew*10
            py = areh*10
            pygame.draw.rect(eurobiznes.window,[255,255,255],[px,py,arew*0.5,areh*0.5])
            sx = pygame.draw.rect(eurobiznes.window,[255,255,255],[px,py,arew*0.5,areh*0.5]).size[0]
            sy = pygame.draw.rect(eurobiznes.window,[255,255,255],[px,py,arew*0.5,areh*0.5]).size[1]
            if (dice == 1):
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/2,py+sy*1/2],arew*1/16)
            elif(dice == 2):
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*1/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*3/4],arew*1/16)
            elif(dice == 3):
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*1/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*2/4,py+sx*2/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*3/4],arew*1/16)
            elif(dice == 4):
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*1/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*1/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*3/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*3/4],arew*1/16)
            elif(dice == 5):
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*1/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*1/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*2/4,py+sx*2/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*3/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*3/4],arew*1/16)
            else:
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*1/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*1/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*2/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*2/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*1/4,py+sx*3/4],arew*1/16)
                pygame.draw.circle(eurobiznes.window,color,[px+sx*3/4,py+sx*3/4],arew*1/16)

        def draw_info(field):
            
            font = pygame.font.SysFont('arial',14)
            if(field.number == 3 or field.number == 5 or field.number == 8 or field.number == 18 or field.number == 23 or field.number == 34 or field.number == 37 or field.number == 39):
                text1 = font.render("",True,[0,0,0])
            else: 
                text1 = font.render("Akt własności",True,[0,0,0])
            text1xy = text1.get_rect()
            text1xy.center = [arew*5,areh*3.20]

            if(field.number == 6):
                country_msg = "Kolej południowa"
            elif(field.number == 16):
                country_msg = "Kolej zachodnia"
            elif(field.number == 26):
                country_msg = "Kolej północna"
            elif(field.number == 36):
                country_msg = "Kolej zachodnia"
            elif(field.number == 3 or field.number == 18 or field.number == 34):
                country_msg = "Szansa niebieska"
            elif(field.number == 8 or field.number == 23 or field.number == 37):
                country_msg = "Szansa czerwona"
            elif(field.number == 5):
                country_msg = "Parking strzeżony"
            elif(field.number == 13):
                country_msg = "Elektrownia atomowa"
            elif(field.number == 29):
                country_msg = "Sieć wodociagów"
            elif(field.number == 39):
                country_msg = "Podatek od wzbogacenia"
            else:
                country_msg = "Kraj: " + field.country + ", Miasto: " + field.msg   
            text2 = font.render(country_msg,True,[0,0,0])
            text2xy = text2.get_rect()
            text2xy.center = [arew*5,areh*3.45]

            if(field.cost != 0):
                text3 = font.render("Koszt działki: " + str(field.cost),True,[0,0,0])
            else:
                text3 = font.render("",True,[0,0,0])
            text3xy = text3.get_rect()
            text3xy.bottomleft = [arew*2.5+5,areh*4]

            if(field.cost != 0):
                text4 = font.render("Opłata za postój:",True,[0,0,0])
            elif(field.number == 5):
                text4 = font.render("Opłata za postój: 400",True,[0,0,0])
            elif(field.number == 39):
                text4 = font.render("Jeżeli masz więcej niż 1000",True,[0,0,0])
            else:
                text4 = font.render("",True,[0,0,0])

            text4xy = text4.get_rect()
            text4xy.bottomleft = [arew*2.5+5,areh*4.50]

            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                text5 = font.render("-teren niezabudowany: " + str(field.pay0),True,[0,0,0])
            elif(field.cost != 0 and field.number != 13 and field.number != 29):
                text5 = font.render("-jeżeli gracz posiada 1 linię: 50",True,[0,0,0])
            elif(field.cost != 0):
                text5 = font.render("10*suma wyrzuconych wyrzuconych oczek.",True,[0,0,0])
            elif(field.number == 39):
                text5 = font.render("płacisz 200.",True,[0,0,0])
            else:
                text5 = font.render("",True,[0,0,0])

            text5xy = text5.get_rect()
            text5xy.bottomleft = [arew*2.5+5,areh*4.75]

            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                text6 = font.render("-teren z 1 domkiem:     " + str(field.pay1),True,[0,0,0])
            elif(field.cost != 0 and field.number != 13 and field.number != 29):
                text6 = font.render("-jeżeli gracz posiada 2 linie: 100",True,[0,0,0])
            elif(field.cost != 0):
                text6 = font.render("Jeżeli gracz posiada kartę wodociągi",True,[0,0,0])
            else:
                text6 = font.render("",True,[0,0,0])
            
            text6xy = text6.get_rect()
            text6xy.bottomleft = [arew*2.5+5,areh*5]

            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                text7 = font.render("-teren z 2 domkami:     " + str(field.pay2),True,[0,0,0])
            elif(field.cost != 0 and field.number != 13 and field.number != 29):
                text7 = font.render("-jeżeli gracz posiada 3 linie: 150",True,[0,0,0])
            elif(field.cost != 0):
                text7 = font.render("opłata jest podwojona.",True,[0,0,0])
            else:
                text7 = font.render("",True,[0,0,0])

            text7xy = text7.get_rect()
            text7xy.bottomleft = [arew*2.5+5,areh*5.25]

            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                text8 = font.render("-teren z 3 domkami:     " + str(field.pay3),True,[0,0,0])
            elif(field.cost != 0 and field.number != 13 and field.number != 29):
                text8 = font.render("-jeżeli gracz posiada 4 linie: 200",True,[0,0,0])
            else:
                text8 = font.render("",True,[0,0,0])

            text8xy = text8.get_rect()
            text8xy.bottomleft = [arew*2.5+5,areh*5.5]

            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                text9 = font.render("-teren z 4 domkami:     " + str(field.pay4),True,[0,0,0])
            else:
                text9 = font.render("",True,[0,0,0])

            text9xy = text9.get_rect()
            text9xy.bottomleft = [arew*2.5+5,areh*5.75]

            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                text10 = font.render("-teren z 1 hotelem:       " + str(field.pay5),True,[0,0,0])
            else:
                text10 = font.render("",True,[0,0,0])

            text10xy = text10.get_rect()
            text10xy.bottomleft = [arew*2.5+5,areh*6]
            
            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                text11 = font.render("Koszt domku wynosi:     " + str(field.house),True,[0,0,0])
            else:
                text11 = font.render("",True,[0,0,0])

            text11xy = text11.get_rect()
            text11xy.bottomleft = [arew*2.5+5,areh*6.5]

            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                text12 = font.render("Koszt hotelu wynosi:      " + str(field.hotel),True,[0,0,0])
            else:
                text12 = font.render("",True,[0,0,0])

            text12xy = text12.get_rect()
            text12xy.bottomleft = [arew*2.5+5,areh*6.75]

            if(field.cost != 0):
                text13 = font.render("Sprzedaż aktu własności:" + str(int(round(field.cost/2))),True,[0,0,0])
            else:
                text13 = font.render("",True,[0,0,0])

            text13xy = text13.get_rect()
            text13xy.bottomleft = [arew*2.5+5,areh*7.25]

            if(field.cost != 0 and  field.number != 6 and field.number != 13 and field.number != 16 and field.number != 26 and field.number != 29 and field.number != 36):
                if(field.lvl == 0):
                    text14 = font.render("Teren niezabudowany",True,[0,0,0])
                elif(field.lvl == 1):
                    text14 = font.render("Teren posiada 1 domek",True,[0,0,0])
                elif(1 < field.lvl < 5):
                    text14 = font.render("Teren posiada " + str(field.lvl) + " domki",True,[0,0,0])
                else:
                    text14 = font.render("Teren posiada hotel",True,[0,0,0])
            else:
                text14 = font.render("",True,[0,0,0])

            text14xy = text14.get_rect()
            text14xy.center = [arew*5+5,areh*7.75]
                
            
            if(field.cost != 0):
                text15 = font.render("Właściciel pola: " + field.owner ,True,[0,0,0])
            else:
                text15 = font.render("",True,[0,0,0])

            text15xy = text15.get_rect()
            text15xy.center = [arew*5+5,areh*8.25]


            pygame.draw.rect(eurobiznes.window,[0,0,0],[arew*2.5,areh*2.5,arew*5,areh*6])
            pygame.draw.rect(eurobiznes.window,[255,255,255],[arew*2.5+2,areh*2.5+2,arew*5-4,areh*6-4])
            pygame.draw.rect(eurobiznes.window,field.fc,[arew*2.5+2,areh*2.5+2,arew*5-4,areh*1/2])


            eurobiznes.window.blit(text1,text1xy)
            eurobiznes.window.blit(text2,text2xy)
            eurobiznes.window.blit(text3,text3xy)
            eurobiznes.window.blit(text4,text4xy)
            eurobiznes.window.blit(text5,text5xy)
            eurobiznes.window.blit(text6,text6xy)
            eurobiznes.window.blit(text7,text7xy)
            eurobiznes.window.blit(text8,text8xy)
            eurobiznes.window.blit(text9,text9xy)
            eurobiznes.window.blit(text10,text10xy)
            eurobiznes.window.blit(text11,text11xy)
            eurobiznes.window.blit(text12,text12xy)
            eurobiznes.window.blit(text13,text13xy)
            eurobiznes.window.blit(text14,text14xy)
            eurobiznes.window.blit(text15,text15xy)


    def game():
        run_it = True 

        while run_it:
            pygame.time.Clock().tick(eurobiznes.FPS)

            if (eurobiznes.window_count == 1):
                eurobiznes.window.fill([255,255,0])
                start_game.draw_button()
                quit_game.draw_button()

            elif (eurobiznes.window_count == 2):
                eurobiznes.window.fill([255,255,0])
                back.draw_button()
                player_choose_2.draw_button()
                player_choose_3.draw_button()
                player_choose_4.draw_button()
            else:
                eurobiznes.window.fill([255,255,0])
                eurobiznes.fields.draw_fields()
                eurobiznes.players.draw_players()
                roll.draw_button()
                buy.draw_button()
                sell.draw_button()
                upgrade.draw_button()
                degrade.draw_button()
                end_turn.draw_button()
                eurobiznes.info.draw_info_msg()
                if(eurobiznes.info.roll[0] != 0 and eurobiznes.info.roll[1] != 0):
                    eurobiznes.info.draw_dice(eurobiznes.info.roll[0],0)
                    eurobiznes.info.draw_dice(eurobiznes.info.roll[1],1)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_it = False

start_game = eurobiznes.buttons(arew*6.5,areh*6.5,arew*3,areh*1,"STARTUJ")
quit_game = eurobiznes.buttons(arew*6.5,areh*8,arew*3,areh*1,"WYJDŹ")

back = eurobiznes.buttons(arew*6.5,areh*8,arew*3,areh*1,"POWRÓT")
player_choose_2 = eurobiznes.buttons(arew*3,areh*6.5,arew*3,areh*1,"2 graczy")
player_choose_3 = eurobiznes.buttons(arew*6.5,areh*6.5,arew*3,areh*1,"3 graczy")
player_choose_4 = eurobiznes.buttons(arew*10,areh*6.5,arew*3,areh*1,"3 graczy")

start = eurobiznes.fields(arew*11,areh*11,arew*2,areh*2,[255,255,255],"START",0,0,0,0,0,0,0)
saloniki = eurobiznes.fields(arew*10,areh*11,arew*1,areh*2,[255,255,0],"Saloniki",120,5,40,60,180,320,500)
szansa_1b = eurobiznes.fields(arew*9,areh*11,arew*1,areh*2,[255,255,255],"Szansa !",0,0,0,0,0,0,0)
ateny = eurobiznes.fields(arew*8,areh*11,arew*1,areh*2,[255,255,0],"Ateny",120,10,40,120,360,640,900)
g_parking = eurobiznes.fields(arew*7,areh*11,arew*1,areh*2,[255,255,255],"$ Parking $",0,0,0,0,0,0,0)
s_railway = eurobiznes.fields(arew*6,areh*11,arew*1,areh*2,[255,255,255],"Kolej",400,0,0,0,0,0,0)
neapol = eurobiznes.fields(arew*5,areh*11,arew*1,areh*2,[255,0,0],"Neapol",200,15,60,180,540,800,1100)
szansa_1r = eurobiznes.fields(arew*4,areh*11,arew*1,areh*2,[255,255,255],"Szansa!",0,0,0,0,0,0,0)
mediolan = eurobiznes.fields(arew*3,areh*11,arew*1,areh*2,[255,0,0],"Mediolan",200,15,60,180,540,800,1100)
rzym = eurobiznes.fields(arew*2,areh*11,arew*1,areh*2,[255,0,0],"Rzym",240,20,80,200,600,900,1200)

prison = eurobiznes.fields(0,areh*11,arew*2,areh*2,[255,255,255],"WiEZIENIE",0,0,0,0,0,0,0)
barcelona = eurobiznes.fields(0,areh*10,arew*2,areh*1,[0,0,255],"Barcelona",280,20,100,300,900,1250,1500)
electric = eurobiznes.fields(0,areh*9,arew*2,arew*1,[255,255,255],"Elektryk",300,0,0,0,0,0,0)
sewilla = eurobiznes.fields(0,areh*8,arew*2,arew*1,[0,0,255],"Sewilla",280,20,100,300,900,1250,1500)
madryt = eurobiznes.fields(0,areh*7,arew*2,arew*1,[0,0,255],"Madryt",320,25,120,360,1000,1400,1800)
w_railway = eurobiznes.fields(0,areh*6,arew*2,arew*1,[255,255,255],"Kolej",400,0,0,0,0,0,0)
liverpool = eurobiznes.fields(0,areh*5,arew*2,arew*1,[254,127,0],"Liverpool",380,30,150,450,1200,1550,1850)
szansa_2b = eurobiznes.fields(0,areh*4,arew*2,arew*1,[255,255,255],"Szansa !",0,0,0,0,0,0,0)
glasgow = eurobiznes.fields(0,areh*3,arew*2,arew*1,[254,127,0],"Glasgow",380,30,150,450,1200,1550,1850)
londyn = eurobiznes.fields(0,areh*2,arew*2,arew*1,[254,127,0],"Londyn",400,35,180,500,1400,1750,2100)

parking = eurobiznes.fields(0,0,arew*2,arew*2,[255,255,255],"PARKING",0,0,0,0,0,0,0)
rotterdam = eurobiznes.fields(arew*2,0,arew*1,areh*2,[0,255,0],"Rotterdam",440,35,180,500,1400,1750,2100)
szansa_2r = eurobiznes.fields(arew*3,0,arew*1,areh*2,[255,255,255],"Szansa !",0,0,0,0,0,0,0)
bruksela = eurobiznes.fields(arew*4,0,arew*1,areh*2,[0,255,0],"Bruksela",440,35,180,500,1400,1750,2100)
amsterdam = eurobiznes.fields(arew*5,0,arew*1,areh*2,[0,255,0],"Amsterdam",480,40,200,600,1500,1850,2200)
n_railway = eurobiznes.fields(arew*6,0,arew*1,areh*2,[255,255,255],"Kolej",400,0,0,00,0,0,0)
malmo = eurobiznes.fields(arew*7,0,arew*1,areh*2,[255,0,255],"Malmo",520,45,220,660,1600,1950,2300)
goteborg = eurobiznes.fields(arew*8,0,arew*1,areh*2,[255,0,255],"Goteborg",520,45,220,660,1600,1950,2300)
netpool = eurobiznes.fields(arew*9,0,arew*1,areh*2,[255,255,255],"Wodociąg",300,0,0,0,0,0,0)
sztokholm = eurobiznes.fields(arew*10,0,arew*1,areh*2,[255,0,255],"Sztokholm",560,50,240,720,1700,2050,2400)

gt_prison = eurobiznes.fields(arew*11,0,arew*2,areh*2,[255,255,255],"IDZ DO WIEZIENIA",0,0,0,0,0,0,0)
frankfurt = eurobiznes.fields(arew*11,areh*2,arew*2,areh*1,[150,75,0],"Frankfurt",600,55,260,780,1900,2200,2550)
kolonia = eurobiznes.fields(arew*11,areh*3,arew*2,areh*1,[150,75,0],"Kolonia",600,55,260,780,1900,2200,2550)
szansa_3b = eurobiznes.fields(arew*11,areh*4,arew*2,areh*1,[255,255,255],"Szansa !",0,0,0,0,0,0,0)
bonn = eurobiznes.fields(arew*11,areh*5,arew*2,areh*1,[150,75,0],"Bonn",640,60,300,900,2000,2400,2800)
e_railway = eurobiznes.fields(arew*11,areh*6,arew*2,areh*1,[255,255,255],"Kolej",400,0,0,0,0,0,0)
szansa_3r = eurobiznes.fields(arew*11,areh*7,arew*2,areh*1,[255,255,255],"Szansa !",0,0,0,0,0,0,0)
innsbruck = eurobiznes.fields(arew*11,areh*8,arew*2,areh*1,[0,0,0],"Innsbruck",700,70,350,1000,2200,2600,3000)
payday = eurobiznes.fields(arew*11,areh*9,arew*2,areh*1,[255,255,255],"Podatek",0,0,0,0,0,0,0)
wieden = eurobiznes.fields(arew*11,areh*10,arew*2,areh*1,[0,0,0],"Wieden",800,100,400,1200,2600,3400,4000)

roll = eurobiznes.buttons(arew*9.5,areh*2.75,arew*2,areh*0.75,"Kostki")
buy = eurobiznes.buttons(arew*9.5,areh*3.75,arew*2,areh*0.75,"Kup")
sell = eurobiznes.buttons(arew*9.5,areh*4.75,arew*2,areh*0.75,"Sprzedaj")
upgrade = eurobiznes.buttons(arew*9.5,areh*5.75,arew*2,areh*0.75,"Ulepsz")
degrade = eurobiznes.buttons(arew*9.5,areh*6.75,arew*2,areh*0.75,"Zdegraduj")
end_turn = eurobiznes.buttons(arew*9.5,areh*7.75,arew*2,areh*0.75,"Koniec tury")


player1 = eurobiznes.players([255,0,0])
player2 = eurobiznes.players([0,255,0])
player3 = eurobiznes.players([0,0,255])
player4 = eurobiznes.players([255,255,0])

eurobiznes.game()
pygame.quit()