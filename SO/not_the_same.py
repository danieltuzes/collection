import time
import random
random.seed(0)


def playsound(sound: str):
    """Define your function instead of printing these."""
    print("start: " + sound)
    time.sleep(1)
    print(sound + " ended")


sounds = ["test1.mp3", "test2.mp3", "test3.mp3", "test4.mp3"]
prev = None  # the last played song
while True:
    nominees = sounds.copy()
    if prev is not None:
        nominees.remove(prev)

    prev = random.choice(nominees)
    playsound(prev)
