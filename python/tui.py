import sys
import tty
import termios
import time

class RawTerminal:
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

def read_key():
    ch1 = sys.stdin.read(1)
    if ch1 == '\x1b':
        ch2 = sys.stdin.read(1)
        if ch2 == '[':
            ch3 = sys.stdin.read(1)
            if ch3 == 'A':
                return 'UP'
            elif ch3 == 'B':
                return 'DOWN'
            elif ch3 == 'C':
                return 'RIGHT'
            elif ch3 == 'D':
                return 'LEFT'
        return 'ESC'
    else:
        return ch1

def clear_screen():
    sys.stdout.write('\x1b[2J\x1b[H')
    sys.stdout.flush()

def move_cursor(row, col):
    sys.stdout.write(f'\x1b[{row};{col}H')
    sys.stdout.flush()

def set_reverse_video(on=True):
    if on:
        sys.stdout.write('\x1b[7m')
    else:
        sys.stdout.write('\x1b[0m')
    sys.stdout.flush()

def draw_menu(items, selected):
    clear_screen()
    for idx, text in enumerate(items):
        if idx == selected:
            # \x1b[7m = reverse-video on; \x1b[0m = reset attributes
            sys.stdout.write('\x1b[7m> ' + text + '\x1b[0m\n')
        else:
            sys.stdout.write('  ' + text + '\n')
    sys.stdout.flush()

def run_menu(items):

    selected = 0
    draw_menu(items, selected)

    with RawTerminal():
        while True:
            key = read_key()
            if key == 'UP':
                selected = (selected - 1) % len(items)
                draw_menu(items, selected)
            elif key == 'DOWN':
                selected = (selected + 1) % len(items)
                draw_menu(items, selected)
            elif key in ('\r', '\n'):  # Enter
                return selected
            elif key in ('q', 'Q', 'ESC'):
                return None
     

if __name__ == '__main__':
    menu_items = ["Option 1", "Option 2", "Option 3", "Quit"]
    choice = run_menu(menu_items)
    clear_screen()
    move_cursor(1, 1)
    if choice is None or menu_items[choice] == "Quit":
        print("Goodbye!")
    else:
        print(f"You selected '{menu_items[choice]}'")
