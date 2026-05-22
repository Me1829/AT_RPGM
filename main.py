import json
import re
import time
from deep_translator import GoogleTranslator
from os import system,path,mkdir
from glob import glob

system("clear")

if not path.isdir("hasil"):
    mkdir("hasil")

NAMA_FILE = glob("../*.json")

print ("\n")
import lgm
print ("\n")

target1 = input("game language from?? : ")
target2 = input("wanna translate to language??  : ")

translator = GoogleTranslator(source=target1, target=target2)

pattern = re.compile(
    r'['

    # Jepang
    r'\u3040-\u309F'   # Hiragana
    r'\u30A0-\u30FF'   # Katakana
    r'\u31F0-\u31FF'   # Katakana Extensions
    r'\u3400-\u4DBF'   # CJK Extension A
    r'\u4E00-\u9FFF'   # Kanji

    # Korea
    r'\uAC00-\uD7AF'
    r'\u1100-\u11FF'
    r'\u3130-\u318F'

    # Chinese tambahan
    r'\uF900-\uFAFF'

    # Cyrillic / Rusia
    r'\u0400-\u04FF'

    # Greek
    r'\u0370-\u03FF'

    # Thai
    r'\u0E00-\u0E7F'

    # Arabic
    r'\u0600-\u06FF'
    r'\u0750-\u077F'

    # Hebrew
    r'\u0590-\u05FF'

    # Hindi / Devanagari
    r'\u0900-\u097F'

    # Bengali
    r'\u0980-\u09FF'

    # Tamil
    r'\u0B80-\u0BFF'

    # Telugu
    r'\u0C00-\u0C7F'

    # Kannada
    r'\u0C80-\u0CFF'

    # Malayalam
    r'\u0D00-\u0D7F'

    # Georgian
    r'\u10A0-\u10FF'

    # Armenian
    r'\u0530-\u058F'

    # Ethiopic
    r'\u1200-\u137F'

    # Fullwidth chars
    r'\uFF00-\uFFEF'

    # Emoji
    r'\U0001F300-\U0001FAFF'

    r']'
)


def contains_japanese(text):
    return bool(pattern.search(text))

def translate_block(text):
    if text in cache:
        return cache[text]

    try:
        system("clear")
        translated = translator.translate(text)
        cache[text] = translated

        print ("========================\nAUTO TRANSLATE GAME RPGM\n========================\n")
        print (target1+" :")
        print (text)
        print (target2+" :")
        print (translated)
        print ("========================")

        time.sleep(0.5)

        return translated

    except Exception as e:
        print ("ERROR:", e)
        return text

for LOOP_FILE in NAMA_FILE:

    with open(LOOP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)


    cache = {}


    for common_event in data:

        if not common_event:
            continue

        if "list" not in common_event:
            continue

        cmds = common_event["list"]

        i = 0

        while i < len(cmds):

            cmd = cmds[i]

            if cmd.get("code") == 401:

                block_indexes = []
                block_texts = []

                while i < len(cmds) and cmds[i].get("code") == 401:

                    txt = cmds[i]["parameters"][0]

                    block_indexes.append(i)
                    block_texts.append(txt)

                    i += 1

                joined = "\n".join(block_texts)

                if joined.strip():

                    translated = translate_block(joined)

                    if not translated:
                        translated = joined

                    split_lines = str(translated).split("\n")

                    while len(split_lines) < len(block_indexes):
                        split_lines.append("")

                    for idx, line in zip(block_indexes, split_lines):
                        cmds[idx]["parameters"][0] = line

            else:
                i += 1

    FINAL_FILE = "hasil/"+LOOP_FILE

    with open(FINAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


    print ("DONE")
    print ("Saved as:", FINAL_FILE)
