from gamepy import Recorder
from pynput.keyboard import KeyCode, Key

rec = Recorder(['w','a','s','d'])

small_bbox = [50,161,850,550]
large_bbox = [0,200,1440,900]
rec.record('./test/image.png', bbox = large_bbox)
