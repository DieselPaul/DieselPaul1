from pathlib import Path

from gtts import gTTS
from mutagen.mp3 import MP3
from rich.progress import track

from utils.console import print_step, print_substep


def save_text_to_mp3(reddit_obj):
    """Saves Text to MP3 files.

    Args:
        reddit_obj : The reddit object you received from the reddit API in the askreddit.py file.
    """
    length = 0

    print_step("Saving Text to MP3 files...")

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    tts = gTTS(text=reddit_obj["thread_title"], lang="en", slow=False)
    tts.save("assets/mp3/title.mp3")
    length += MP3("assets/mp3/title.mp3").info.length

    for idx, comment in track(enumerate(reddit_obj["comments"]), "Saving..."):
        # ! Stop creating mp3 files if the length is greater than 50 seconds.
        # ! This can be longer, but this is just a good starting point
        if length > 50:
            break
        tts = gTTS(text=comment["comment_body"], lang="en", slow=False)
        tts.save(f"assets/mp3/{idx}.mp3")
        length += MP3(f"assets/mp3/{idx}.mp3").info.length

    print_substep("Saved Text to MP3 files successfully.", style="bold green")
    # ! Return the index so we know how many screenshots of comments we need to make.
    return length, idx
