# from playsound import playsound
import random
import time
random.seed(0)


def my_playsound(fname: str) -> None:
    """Mocking playsound for debugging."""
    print(f"Playing {fname}")


sounds = ["en.mp3", "to.mp3", "tre.mp3", "fire.mp3"]

while True:
    i = random.randrange(len(sounds))
    print(i)
    my_playsound(sounds[i])
    time.sleep(1)
