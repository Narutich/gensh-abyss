from glob import glob
import imp
from logging import getLoggerClass
from msilib.schema import Class
from tkinter import E
from django.shortcuts import render
from django.http import HttpResponse
import genshin
import genshinstats as gs
from array import *
from requests import request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import random


'''def second_parser():
    url_site = 'https://genshin.honeyhunterworld.com/d_1001/?lang=EN'
    browser = webdriver.Chrome('C:\Chromedriver\chromedriver.exe')
    browser.get(url_site)
    content = browser.page_source
    soup = BeautifulSoup(content,"html.parser")

    #Find the last floor variant 
    links = soup.select('section',attrs={})
    last_variant = ""
    variant_checker = set()
    for i in links:
        if('id' in i.attrs and 'Variant' in i['id']):
            last_variant = i['id']
        if('id' in i.attrs and 'Floor' in i['id']):
            variant_checker.add(last_variant)

    #Parse the last floor variant
    links = soup.select('img, td, a, section,label',attrs={})
    flag = False
    f = None
    cur_variant = ""
    for i in links:
        if(i.name == 'section' and 'id' in i.attrs and 'Variant' in i['id']):
            cur_variant = i['id'] 
        if(i.name == 'section' and 'id' in i.attrs and 'Floor' in i['id']):
            f = open(i['id'].replace(" ","").replace("#","").lower() +'.txt','w')
        if(cur_variant in variant_checker):
            if(i.name == 'label' and 'for' in i.attrs and 'a_chamber' in i['for']):
                f.write(i.text + '\n')    
            if(i.name == 'a' and '/m' in i['href']) and flag:
                if(len(i.text) != 0):
                    f.write("Mob_name: " + i.text + '\n')   
            if(i.name == 'td' and 'Monsters' in i.text):
                flag = True
                f.write(i.text + '\n')   
            if ('loading' in i.attrs and 'lazy' in i['loading'] and '/m' in i['src'] and flag):
                f.write('https://genshin.honeyhunterworld.com/' + i['src'] + '\n')

second_parser()'''

'''def tier_list_parser():
    browser = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
    browser.get("https://genshin.gg/tier-list")
    content = browser.page_source
    soup = BeautifulSoup(content,"html.parser")

    links = soup.select('div,h2,h3',attrs={})
    f = open('Tier_list.txt',"w")
    path = "D:\AbyssPy\genshin_prog\Tierlist"
    for a in links:
        if(a.name == "div" and a.has_key('class') and 'tier-title' in a['class']):
            f.write("--------------------------" + '\n')
            f.write("Tier: " + a.text + '\n')
            f.write("--------------------------" + '\n')
        if(a.has_key('class') and 'character-name' in a['class']):
            f.write("Name: " + a.text + '\n')   
        if(a.has_key('class') and 'character-role' in a['class']):
            f.write("Role: " + a.text + '\n')

    browser.quit()

tier_list_parser()'''


class Characters:
        def __init__(self, icon, name, rarity, element, role, tier):
            self.character_icon = icon
            self.character_name = name
            self.character_rarity = rarity
            self.character_element = element
            self.character_type = role
            self.character_tear = tier
            self.character_point = 0
            self.character_point_half_2 = 0

class Mobs:
    def __init__(self, name, icon, chamber, half):
        self.mob_name = name
        self.mob_icon = icon
        self.mob_chamber = chamber
        self.mob_half = half


class Team:
    def __init__(self, char_1, char_2, char_3, char_4):
        self.char_1 = char_1
        self.char_2 = char_2
        self.char_3 = char_3
        self.char_4 = char_4

    def __init__(self, char_1, char_2, char_3, char_4, char_5, char_6, char_7, char_8):
        self.char_1 = char_1
        self.char_2 = char_2
        self.char_3 = char_3
        self.char_4 = char_4
        self.char_5 = char_5
        self.char_6 = char_6
        self.char_7 = char_7
        self.char_8 = char_8


def character_power_point(chars, enemies):
    for i in chars:
        for j in enemies:
        #Pyro
            if(i.character_element == "Pyro" and j.mob_half == 'Monsters (First Half)' or i.character_element == "Pyro" and j.mob_half == ''):
                if("Pyro" in j.mob_name):
                    i.character_point -= 50
                if("Hydro" in j.mob_name):
                    i.character_point += 100
                if("Electro " in j.mob_name):
                    i.character_point += 10
                if("Cryo" in j.mob_name):
                    i.character_point += 200

            elif(i.character_element == "Pyro" and j.mob_half == 'Monsters (Second Half)'):
                if("Pyro" in j.mob_name):
                    i.character_point_half_2 -= 50
                if("Hydro" in j.mob_name):
                    i.character_point_half_2 += 100
                if("Electro " in j.mob_name):
                    i.character_point_half_2 += 10
                if("Cryo" in j.mob_name):
                    i.character_point_half_2 += 200

        #Hydro

            elif(i.character_element == "Hydro" and j.mob_half == 'Monsters (First Half)' or i.character_element == "Hydro" and j.mob_half == ''):
                if("Hydro" in j.mob_name):
                    i.character_point -= 50
                if("Pyro" in j.mob_name):
                    i.character_point += 200
                if("Electro " in j.mob_name):
                    i.character_point += 30
                if("Cryo" in j.mob_name):
                    i.character_point += 80 
        
            elif(i.character_element == "Hydro" and j.mob_half == 'Monsters (Second Half)'):
                if("Hydro" in j.mob_name):
                    i.character_point_half_2 -= 50
                if("Pyro" in j.mob_name):
                    i.character_point_half_2 += 200
                if("Electro " in j.mob_name):
                    i.character_point_half_2 += 30
                if("Cryo" in j.mob_name):
                    i.character_point_half_2 += 80 
        #Electro

            elif(i.character_element == "Electro" and j.mob_half == 'Monsters (First Half)' or i.character_element == "Electro" and j.mob_half == ''):
                if("Electro" in j.mob_name):
                    i.character_point -= 50
                if("Pyro" in j.mob_name):
                    i.character_point += 10
                if("Hydro" in j.mob_name):
                    i.character_point += 30
                if("Cryo" in j.mob_name):
                    i.character_point += 80 

            elif(i.character_element == "Electro" and j.mob_half == 'Monsters (Second Half)'):
                if("Electro" in j.mob_name):
                    i.character_point_half_2 -= 50
                if("Pyro" in j.mob_name):
                    i.character_point_half_2 += 10
                if("Hydro" in j.mob_name):
                    i.character_point_half_2 += 30
                if("Cryo" in j.mob_name):
                    i.character_point_half_2 += 80 
        #Cryo

            elif(i.character_element == "Cryo" and j.mob_half == 'Monsters (First Half)' or i.character_element == "Cryo" and j.mob_half == ''):
                if("Cryo" in j.mob_name):
                    i.character_point -= 50
                if("Pyro" in j.mob_name):
                    i.character_point += 100
                if("Hydro" in j.mob_name):
                    i.character_point += 80
                if("Electro" in j.mob_name):
                    i.character_point += 80

            elif(i.character_element == "Cryo" and j.mob_half == 'Monsters (First Half)'):
                if("Cryo" in j.mob_name):
                    i.character_point_half_2 -= 50
                if("Pyro" in j.mob_name):
                    i.character_point_half_2 += 100
                if("Hydro" in j.mob_name):
                    i.character_point_half_2 += 80
                if("Electro" in j.mob_name):
                    i.character_point_half_2 += 80

        #Anemo and Geo

            elif(i.character_element == "Anemo" and j.mob_half == 'Monsters (First Half)' or i.character_element == "Anemo" and j.mob_half == '' or
                i.character_element == "Geo" and j.mob_half == 'Monsters (First Half)' or i.character_element == "Geo" and j.mob_half == ''):
                i.character_point += 120
        
            elif(i.character_element == "Anemo" and j.mob_half == 'Monsters (Second Half)'or
                i.character_element == "Geo" and j.mob_half == 'Monsters (Second Half)'):
                i.character_point_half_2 += 120

        if(i.character_tear == "SS+"):
            i.character_point += 200
            i.character_point_half_2 += 200
        elif(i.character_tear == "S+"):
            i.character_point += 150
            i.character_point_half_2 += 150
        elif(i.character_tear == "S"):
            i.character_point += 100
            i.character_point_half_2 += 100
        elif(i.character_tear == "A"):
            i.character_point += 50
            i.character_point_half_2 += 50
        elif(i.character_tear == "B"):
            i.character_point += 30
            i.character_point_half_2 += 30
        elif(i.character_tear == "C"):
            i.character_point += 10
            i.character_point_half_2 += 10

    chars = chars.sort(key=lambda x: x.character_point, reverse=True)

'''def team_builder(chars):
    arr = set()
    team = []
    whole_teams = []
    sub_dps_counter = 1
    for i in chars:
        if(len(team) == 4):
            if(team not in whole_teams):
                whole_teams.append(team)
            #return team
        if(i.character_type == "Sub DPS" and i.character_type in arr and sub_dps_counter < 2):
            team.append(i)
            sub_dps_counter += 1
        elif(i.character_type not in arr):
            arr.add(i.character_type)
            team.append(i)

    return whole_teams'''


def define_role(character):
    f = open("Tier_list.txt",'r')
    flag = False
    tier = None
    for x in f:
        name = str(character.name)
        fname = x.replace("Name: ","").replace('\n',"")
        if("Tier" in x):
            tier = x.replace("Tier: ","").replace('\n',"")
        if("Name" in x):
            if(name == "Traveler"):
                name = name + ' (' + character.element + ')'
            if(name == 'Tartaglia'):
                name = 'Childe'
            if(fname in name):
                flag = True
            else :
                flag = False
        if(flag == True and "Role" in x):
            info = [x.replace("Role: ","").replace('\n',""),tier]
            return info

#constellations
def read_mobs(request):
    file_name = request.get_full_path().replace('/','') + '.txt'
    f = open(file_name,'r')
    mobs = []
    chamber = ''
    name = ''
    icon = ''
    half = ''
    for x in f:
        if('Chamber' in x):
            chamber = x.strip()
        if('https' in x):
            icon = x.strip()
        if('Mob_name:' in x):
            name = x.strip()
        if('Monsters' in x):
            half = x.strip()
        if(chamber != '' and icon != '' and name != ''):
            mobs.append(Mobs(name, icon, chamber, half))
            icon = ''
            name = ''
    return mobs

def read_characters():
    characters = []
    for i in data.characters:
        info = define_role(i)
        characters.append(Characters(i.icon, i.name, i.rarity, i.element, info[0], info[1]))
    return characters

async def views_floor(request, *args, **kwargs):
    global data
    global nickname
    cook = get_cookie()
    if(cook == {}):
        data = {}
        uid = None
        nickname = None
        return render(request, 'lack_of_cookie.html')

    await get_client_data(cook)

    mobs = read_mobs(request)

    if(nickname == None):
        nickname = data.info.nickname

    characters = read_characters()
    
    character_power_point(characters, mobs)

    """for character in data.characters:
        chars.append(Characters(character.icon, character.name, character.rarity, character.element))  """        
    return render(request, 'Floor.html', {'mobs': mobs,'chars': characters, 'nickname': nickname})

uid = None
data = {}
nickname = None


async def get_client_data(cook):
    global uid
    global data
     #Chech cookie
    client = genshin.Client(cook)
    if(uid == None):
        uid = gs.get_uid_from_hoyolab_uid(cook['ltuid'],False,cook)

    if(data == {}):
        data = await client.get_genshin_user(uid)
        print(data.info.nickname)

def get_cookie():
    global data
    global nickname
    global uid
    cook = gs.get_browser_cookies()
    if('account_id' in cook.keys()):
        if(cook["account_id"] != cook["ltuid"]):
            cook["ltuid"] = cook["account_id"]
            data = {} 
            nickname = None
            uid = None
    return cook


async def say_hello(request):
    global data
    global nickname
    global uid
     #Chech cookie
    cook = get_cookie()
    if(cook == {}):
        data = {}
        uid = None
        nickname = None
        return render(request, 'lack_of_cookie.html')
    
    await get_client_data(cook)

    nickname = data.info.nickname

    floors = []
    print(cook)
    for i in range (12):
        floors.append(i + 1)  
         
    return render(request, 'home.html', {'nickname': nickname,'floors' : floors})
    
def preolad(request):
    return render(request, 'preloader.html')