# main.py

import os
import numpy as np
import bot as wordle_bot
from user import User
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

# Get token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

prefix = '!'
client = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=None)

users = {}


# To create a wordle instance.
@client.command(name="wordle")
async def wordle(ctx):
    user_id = ctx.author.id
    if user_id in users:
        del users[user_id]

    users[user_id] = User(words_space=wordle_bot.possible_words)

    await ctx.reply(f"New wordle game created.")
    

# To get suggestions from wordle bot.
@client.command(name="get_words")
async def get_words(ctx, num_best="5"):
    try:
        num_best = int(num_best)
    except:
        await ctx.reply(f"The number of suggestions is invalid!")
        return

    user_id = ctx.author.id
    # User hasn't created a wordle instance.
    if user_id not in users:
        await ctx.reply(f"You haven't created any wordle games. Type !wordle_help to know how to use me.")
        return

    if num_best > 15:
        await ctx.reply(f"This is too much suggestions. Try to guess with less than 15.")
        return

    user = users[user_id]

    suggestions = None
    if len(user.guess_history) == 0:
        infos = wordle_bot.entropy_data
        num_best = min(num_best, len(infos))
        infos_id = np.argpartition(infos, -num_best)[-num_best:]
        infos_id = infos_id[np.argsort(-infos[infos_id])]
        suggestions = infos_id, infos[infos_id]
    else:
        suggestions = wordle_bot.get_best_words(user.words_space, num_best)

    if len(suggestions[1]) == 0:
        await ctx.reply(f"There is no suggestion.")
        return

    ranks, answer, infomation = "", "", ""
    for i, info in enumerate(suggestions[1]):
        ranks += f"{i + 1}\n"
        answer += f"{user.words_space[suggestions[0][i]]}\n"
        infomation += f"{info:.4f}\n"

    embed = Embed(
        title = "Wordle Suggestions",
        color = int(hex(int("#ffdab9".replace("#", ""), 16)), 0)
    )
    embed.set_thumbnail(url = "https://media.newyorker.com/photos/61e989e14c20ec321e63f851/master/pass/wordle_big_animation2.gif")
    embed.set_footer(text = '⨯ Type !wordle_help to know how to use me.')

    embed.add_field(name = "#", value = ranks)
    embed.add_field(name = "Words", value = answer)
    embed.add_field(name = "Infomation", value = infomation)

    await ctx.reply(embed=embed)


@client.command(name="guess")
async def guess(ctx, word="", patt=""):
    user_id = ctx.author.id
    # User hasn't created a wordle instance.
    if user_id not in users:
        await ctx.reply(f"You haven't created any wordle games. Type !wordle_help to know how to use me.")
        return

    user = users[user_id]

    if len(word) != 5 or len(patt) != 5:
        await ctx.reply(f"Invalid arguments")
        return

    for p in patt:
        x = -1
        try:
            x = int(p)
        except:
            await ctx.reply(f"The pattern is invalid!")
            return
        if x < 0 or x > 2:
            await ctx.reply(f"The pattern is invalid!")
            return

    pattern = 0
    for x in reversed(patt):
        pattern = pattern * 3 + int(x)

    user.words_space = wordle_bot.get_remaining_words_space(word, pattern, user.words_space)
    user.guess_history.append((word, patt))
    await ctx.reply(f"Processed your guess, use !get_words to get suggestions.")


@client.command(name="get_history")
async def get_history(ctx):
    user_id = ctx.author.id
    # User hasn't created a wordle instance.
    if user_id not in users:
        await ctx.reply(f"You haven't created any wordle games. Type !wordle_help to know how to use me.")
        return

    user = users[user_id]

    if len(user.guess_history) == 0:
        await ctx.reply(f"You haven't guessed. Type !wordle_help to know how to use me.")
        return

    ranks, answer, infomation = "", "", ""
    for i, (word, pattern) in enumerate(user.guess_history):
        ranks += f"{i + 1}\n"
        answer += f"{word}\n"

        info = ""
        for p in pattern:
            info += f"{wordle_bot.STATE_COLOR[int(p)]}"
        infomation += f"{info}\n"

    embed = Embed(
        title = "Wordle History",
        color = int(hex(int("#ffdab9".replace("#", ""), 16)), 0)
    )
    embed.set_thumbnail(url = "https://media.newyorker.com/photos/61e989e14c20ec321e63f851/master/pass/wordle_big_animation2.gif")
    embed.set_footer(text = '⨯ Type !wordle_help to know how to use me.')

    embed.add_field(name = "#", value = ranks)
    embed.add_field(name = "Words", value = answer)
    embed.add_field(name = "Pattern", value = infomation)

    await ctx.reply(embed=embed)
    
 
@client.command(name="wordle_help")
async def wordle_help(ctx):
    await ctx.reply(file=File("tutorial.png"))


@client.command(name="gay")
async def gay(ctx):
    await ctx.channel.send("No, you")


@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

client.run(TOKEN)
