#!/usr/bin/python3
from colorama import init
from colorama import Fore, Back, Style
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib.request, datetime
import os
import ast


def simple_get(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        with closing(get(url, stream=True, headers=headers)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return(resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def new_stats(hero_html, hero):
    html = simple_get(hero_html)
    soup = BeautifulSoup(html, 'html.parser')
    popularity = []
    for tr in soup.findAll('table')[2].findAll('tr'):
        data = tr.findAll('td')
        try:
            name = data[0].text
            picked = data[1].text
            passed = data[2].text
            pick_per = data[3].text
            popularity.append([name, picked, passed, pick_per])
        except Exception:
            pass
    with open(hero+'/'+hero+'.txt', 'w') as f:
        for item in popularity:
            f.write(str(item) + '\n')
    with open(hero+'/'+hero+'_last_check.txt', 'w') as f:
        f.write(str(datetime.datetime.now()))
    return popularity


def convert(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')


def compare_cards(player_cards, hero_cards):
    result = []
    get_weight = []
    for i in range(len(player_cards)):
        for sub in hero_cards:
            for s in sub:
                if player_cards[i].lower() in s.lower():
                    get_weight.append(sub)
    
    result = sorted(get_weight, key = lambda x: float(x[3][:-1]), reverse=True)
    return result


def work(hero, color):
    player_cards = []
    with open(hero+'/'+hero+'.txt', 'r') as f:
        hero_cards = [ast.literal_eval(line.strip()) for line in f]
    while True:
        try:
            num_cards = int(input('How many cards are we comparing?: '))
        except ValueError:
            print("Sorry that wasn't a number, try again.")
        else:
            break
    for i in range(num_cards):
        player_cards.append(input("Please Enter Card ["+str(i+1)+"]: "))
    result = compare_cards(player_cards, hero_cards)
    print('\nWeighted Results:')
    for i in range(len(result)):
        print(color + result[i][0] + ':' + Style.RESET_ALL + ' ' + Fore.RED + result[i][3] + Style.RESET_ALL + ', Picked: ' +  result[i][1] + ', Passed: ' + result[i][2])
    print('\n')
    

def main():
    try:
        init()
        print('Compare the' + Fore.RED + ' Spire 1.0' + Style.RESET_ALL)
        print('Press Ctrl+C at anytime to exit.\n')
        while True:
            hero = input('Which hero: ' + Fore.RED + '(I)ronclad ' + Style.RESET_ALL + '| ' + Fore.GREEN + '(S)ilent ' + Style.RESET_ALL + '| ' + Fore.BLUE + '(D)efect' + Style.RESET_ALL + ': ')

            if hero.lower() == 'ironclad' or hero.lower() == 'i':
                hero = 'ironclad'
                color = Fore.RED
                if not(os.path.isdir('ironclad/')):
                    os.mkdir('ironclad')
                break
            elif hero.lower() == 'silent' or hero.lower() == 's':
                hero = 'silent'
                color = Fore.GREEN
                if not(os.path.isdir('silent/')):
                    os.mkdir('silent')
                break
            elif hero.lower() == 'defect' or hero.lower() == 'd':
                hero = 'defect'
                color = Fore.BLUE
                if not(os.path.isdir('defect/')):
                    os.mkdir('defect')
                break
            else:
                print("Not a hero try again!")

        hero_html = 'https://spirelogs.com/stats/'+hero+'/card-choices.php'
        if os.path.isfile(hero+'/'+hero+'.txt'):
            if os.path.isfile(hero+'/'+hero+'_last_check.txt'):
                try:
                    with open(hero+'/'+hero+'_last_check.txt') as f:
                        lines = f.readlines()
                    last_check = convert(lines[0])
                    one_day = datetime.datetime.now() - last_check
                    if one_day.days > 1:
                        new_stats(hero_html, hero)
                        work(hero, color)
                    else:
                        work(hero, color)

                except Exception as e:
                    print(e)
            else:
                new_stats(hero_html, hero)
                work(hero, color)
        else:
            new_stats(hero_html, hero)
            work(hero, color)
    except KeyboardInterrupt:
        print(Fore.LIGHTYELLOW_EX + "\nSlay Them Spires" + Style.RESET_ALL)


if __name__ == "__main__":
    main()