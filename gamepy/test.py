from screen import Recorder
from pynput.keyboard import KeyCode

rec = Recorder()

small_bbox = [50,161,850,550]
large_bbox = [0,200,1440,900]
#rec.record('C:/Data/Games/Burnout/validate/image.png', bbox = large_bbox)
print(KeyCode.from_char('w'))
