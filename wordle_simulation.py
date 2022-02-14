# wordle_simulation.py

import numpy as np
import bot as wordle_bot
from tqdm import tqdm as display
import matplotlib.pyplot as plt

from main import wordle


NUM_ANS = len(wordle_bot.possible_words)
words_space = wordle_bot.possible_words


def get_pattern(word, answ):
    return wordle_bot.pattern_matrix_data[wordle_bot.words_index[word], wordle_bot.words_index[answ]]


def get_best_word(is_first=False, space=None):
    global words_space
    if is_first:
        infos = wordle_bot.entropy_data 
    else:
        infos = np.array([wordle_bot.expected_entropy(word, words_space) for word in words_space])
    return words_space[np.argmax(infos)]


def solve(answer: str) -> str:
    global words_space
    word = get_best_word(True)
    score = 1
    while word != answer:
        words_space = wordle_bot.get_remaining_words_space(word, get_pattern(word, answer), words_space)
        word = get_best_word(space=words_space)
        score += 1
    return score


def simulate(num_games=NUM_ANS):
    global words_space
    scores = [0 for i in range(9)]
    sum_score = 0
    pbar = display(range(num_games))
    for game_id in pbar:
        words_space = wordle_bot.possible_words
        pbar.set_description_str(f"Simulating the {game_id}-th game")
        score = solve(wordle_bot.possible_words[game_id])
        scores[score] += 1
        sum_score += score
    return scores, sum_score / num_games


if __name__ == "__main__":
    d, a = simulate()
    # The average score is: 3.5991
    print(f"The average score is: {a:.4f}")

    x = np.arange(len(d))
    plt.bar(x, d)
    plt.xlabel("Scores")
    plt.ylabel("Number of games")
    plt.xticks(x, [i for i in range(len(d))])
    plt.show()
    
