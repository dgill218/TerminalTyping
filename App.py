import curses
from curses import wrapper
import time
import requests, json
from datetime import date

RANDOM_QUOTE_API_URL = 'http://api.quotable.io/random'


def start_screen(stdscr):
  stdscr.clear()
  stdscr.addstr(0, 0, "Welcome to the speed typing test!", curses.A_BOLD)
  stdscr.addstr("\nPress any key to begin")
  stdscr.refresh()  
  stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
  stdscr.addstr(target)
  stdscr.addstr(1, 0, f"WPM: {wpm}", curses.A_BOLD)
  for i, c in enumerate(current):
    correct_char = target[i]
    color = curses.color_pair(1)
    if c != correct_char:
      color = curses.color_pair(2)
      
    stdscr.addstr(0, i, c, color)

def load_text():
  res = requests.get(RANDOM_QUOTE_API_URL)
  data = res.json()
  return data['content']

def wpm_test(stdscr):
  target_text = load_text()
  current_text = []
  wpm = 0
  start_time = time.time()
  stdscr.nodelay(True)
  
  while True:
    time_elapsed = max(time.time() - start_time, 1)
    wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
    
    stdscr.clear()
    display_text(stdscr, target_text, current_text, wpm)
    
    stdscr.refresh()
    
    if "".join(current_text) == target_text:
      stdscr.nodelay(False)
      break
    
    try:
      key = stdscr.getkey()
    except:
      continue
    
    if ord(key) == 27:
      break
    if key in ("KEY_BACKSPACE", "\b", "\x7f"):
      if len(current_text) > 0:
        current_text.pop()
    elif len(current_text) < len(target_text):
      current_text.append(key)
  
  my_dict = {
    'name': 'Reetam',
    'wpm': wpm,
    'date': date.today().strftime("%b-%d-%Y")
  }
  with open('database.json', 'r') as file_obj:
    dataObj = json.load(file_obj)
  
  dataObj.append(my_dict)
  with open('database.json', 'w') as json_file:
    json.dump(dataObj, json_file, indent=4, separators=(',', ': '))
  
    

def main(stdscr):
  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
  
  start_screen(stdscr)
  while True:
    wpm_test(stdscr)
    
    stdscr.addstr(2, 0, "You've completed the text! Press any key to continue or escape to get out...")
    key = stdscr.getkey()
    if ord(key) == 27:
      break

wrapper(main)