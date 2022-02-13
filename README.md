# WordleBot
A bot that can solve wordle fast

## Discord invite
[Click here](https://discord.com/oauth2/authorize?client_id=941982914541916200&permissions=377957174272&scope=bot)

## Discord tutorial
| Commands                                                      | Usage                          |
|---------------------------------------------------------------|--------------------------------|
| !wordle         | To initiate a new wordle game, other commands except *!wordle_help* won't work unless this command is used |
| !get_words \[number_of_suggestions (default is 5)\] | Get wordle suggestions based on the expected infomation they provide, sorted from best to worst. For example: **!get_words 10** |
| !guess \[word\] \[pattern\]      | Started guessing, *word* the chosen word and *pattern* is the word's pattern on wordle: 0 is gray, 1 is yellow and 2 is green. For example: **!guess raise 11020** |
| !get_history          | Get the guess history |
| !wordle_help          | Get help using the bot |

## Demo
[Click here to watch the demo](https://www.youtube.com/watch?v=YCPlbhvTXLg)

## Installation
1. Firstly, install [python](https://www.python.org/downloads/), preferably version 3.8

2. Secondly, install dependencies
```
pip install -r requirement.txt
```

3. Lastly, run the program
```
python bot.py
```

## Usage
- The bot will give you a list of suggestions based on the expected infomation it provides, sorted from best to worst.
- Type your chosen word.
- Type the pattern that wordle gives
- The bot will process the pattern and give other suggesstions based on that.
- Repeat the process until only one word remains.
- Type ".exit" to quit.
