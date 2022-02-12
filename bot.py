# bot.py
from audioop import reverse
import sys
import itertools as it
from time import sleep
import tqdm as display
import matplotlib.pyplot as plt
import numpy as np
import json
import os

MISS = 0
MISPLACED = 1
EXACT = 2
WORDLE_DATA_DIRECTORY = "WordleData/"
STATE_COLOR = {MISS: "⬜", MISPLACED: "🟨", EXACT: "🟩"}


possible_words_file = open(os.path.join(WORDLE_DATA_DIRECTORY, "possible_words.txt"))
possible_words = [word.strip() for word in possible_words_file]
words_index = json.load(open(os.path.join(WORDLE_DATA_DIRECTORY, "words_index.json")))
entropy_data = np.array(list(json.load(open(os.path.join(WORDLE_DATA_DIRECTORY, "entropy_data.json"))).values()))
pattern_matrix_data = np.load(os.path.join(WORDLE_DATA_DIRECTORY, "pattern_matrix_data.npy"))


def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')


def entropy(words_space_size, universe_space_size):
    prob = words_space_size / universe_space_size
    prob = np.where(prob == 0, 1, prob)
    return -prob * np.log2(prob) 


def expected_entropy(word, words_space):
    num_state = 3 ** 5
    this_word_index = words_index[word]
    resulted_words_space = np.zeros(num_state)
    for w in words_space:
        resulted_words_space[pattern_matrix_data[this_word_index, words_index[w]]] += 1
    return np.sum(entropy(resulted_words_space, len(words_space)))


def get_best_words(words_space, num_best=10):
    infos = np.array([expected_entropy(word, words_space) for word in words_space])
    num_best = min(num_best, len(infos))
    infos_id = np.argpartition(infos, -num_best)[-num_best:]
    infos_id = infos_id[np.argsort(-infos[infos_id])]
    return infos_id, infos[infos_id]


def get_entropy_data():
    pbar = display.tqdm(possible_words)
    wordle_data = {}
    for word in pbar:
        pbar.set_description_str(f"Processing: {word}")
        info = expected_entropy(word, possible_words)
        wordle_data[word] = info
    
    f = open("entropy_data.json", "w")
    f.write(json.dumps(wordle_data, indent=4))
    f.close()


def get_remaining_words_space(word, pattern, words_space):
    new_space = []
    this_word_index = words_index[word]
    for w in words_space:
        text = pattern_matrix_data[this_word_index, words_index[w]]
        if(pattern == text):
            new_space.append(w)
    return new_space


if __name__ == "__main__":

    while True:
        print("----------------WORDLE BOT----------------")
        best_start = get_best_words(possible_words)
        print(f"Suggestions:")
        for i, info in enumerate(best_start[1]):
            print(f"{best_start[0][i]}")
            print(f"Word: {possible_words[best_start[0][i]]:<12} E[I] = {info:.4f}")
        print("            ------------------")
        word = input("Type your guess: ")
        if word == ".exit":
            break
        patt = input("Type the pattern: ")

        if len(word) != 5 or len(patt) != 5:
            print("INVALID INPUT!")
            break
        
        pattern = 0
        for x in reversed(patt):
            pattern = pattern * 3 + int(x)

        possible_words = get_remaining_words_space(word, pattern, possible_words)
        screen_clear()
        print(len(possible_words))

    pass



# 4
# 2
# 26
# 1
# 22