import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Speed typing test", curses.color_pair(3))
    stdscr.addstr("\nPress any key begin!", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getkey()

def end_screen(stdscr):
    stdscr.addstr(2, 0, "Test completed! Press any key to continue... Press esc to quit.")

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def display_text(stdscr, target, current, cpm=0):
    stdscr.addstr(target, curses.color_pair(3))
    stdscr.addstr(1, 0, f"Characters per minute: {cpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def cpm_test(stdscr):
    target_text = load_text()
    current_text = []
    cpm = 0 # Characters per minute
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        cpm = round(len(current_text) / (time_elapsed / 60))

        stdscr.clear()
        display_text(stdscr, target_text, current_text, cpm)
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
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

        

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        cpm_test(stdscr)
        end_screen(stdscr)
        key = stdscr.getkey()
        if ord(key) == 27:
            break
        
        


wrapper(main)