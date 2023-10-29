import discord
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import random

load_dotenv()

# Holds the card IDs to be selected
card_deck = {
    "1": ":regional_indicator_a:",
    "2": ":two:",
    "3": ":three:",
    "4": ":four:",
    "5": ":five:",
    "6": ":six:",
    "7": ":seven:",
    "8": ":eight:",
    "9": ":nine:",
    "10": ":keycap_ten:",
    "11": ":regional_indicator_j:",
    "12": ":regional_indicator_q:",
    "13": ":regional_indicator_k:"
}

# Holds the values of each card for calculation
card_values = {
    ":regional_indicator_a:": [1, 11],
    ":two:": 2,
    ":three:": 3,
    ":four:": 4,
    ":five:": 5,
    ":six:": 6,
    ":seven:": 7,
    ":eight:": 8,
    ":nine:": 9,
    ":keycap_ten:": 10,
    ":regional_indicator_j:": 10,
    ":regional_indicator_q:": 10,
    ":regional_indicator_k:": 10
}

# Code for grabbing player IDS

# while 1:
#     message.content.startswith
# P1 = f"<@{message.author.id}>"
# P2 = message.content.split()
# P2 = P2[1]
# print(P1)
# print(P2)


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # If the message is from the bot do nothing
        if (message.author.bot):
            return

        # Check if its a valid command
        def check_hit(m):
            if m.content == '!hit':
                return m.content == '!hit'
            elif m.content == '!end':
                return m.content == '!end'

        # Two versions of calculations
        # One case with Aces
        # One case without Aces
        def value_calc(l):
            total = 0
            for x in l:
                x = f":{x}:"
                total += card_values[x]
            return total

        def value_calc_A(l):
            total1 = 0
            total2 = 0
            for x in l:
                x = f":{x}:"
                if x == ":regional_indicator_a:":
                    total1 += 1
                    total2 += 11
                else:
                    total1 += card_values[x]
                    total2 += card_values[x]
            return total1, total2

        if message.content.startswith('!bj'):

            # Get first 2 cards and print them out
            num1 = random.randint(1, 13)
            num2 = random.randint(1, 13)
            await message.channel.send("Starting Hand:")
            await message.channel.send(card_deck.get(str(num1)))
            await message.channel.send(card_deck.get(str(num2)))

            # Adds the cards to a list so it can be added on later with subsequent hits
            current = card_deck.get(str(num1)) + card_deck.get(str(num2))
            current = current.replace(':', ' ')
            current = current.split()

            # Two cases one with an ACE and one without an ACE for resolving events
            if "regional_indicator_a" in current:
                tup = value_calc_A(current)
                tup1 = tup[0]
                tup2 = tup[1]
                await message.channel.send(f"Your totals are: {tup1} and {tup2}")
                if tup1 == 21 or tup2 == 21:
                    await message.channel.send(f"You Win!")
                    return
            else:
                await message.channel.send(f"Your total is: {value_calc(current)}")
                if value_calc == 21:
                    await message.channel.send(f"You Win!")
                    return

            # Infinite While to simulate the game till game over or player ends
            # Player can do two comamnds here !hit and !end
            # !hit will add a card and will allow the player to go again or game over them for going over 21
            # !end will stop the player from drawing more cards and allow them to VS the dealer
            while True:
                msg = await self.wait_for("message", check=check_hit)
                if msg.content == "!hit":

                    num = random.randint(1, 13)
                    # Gets all the values and sends them again
                    for x in current:
                        await message.channel.send(f":{x}:")
                    await message.channel.send(card_deck.get(str(num)))
                    current.append(card_deck.get(str(num)).replace(':', ''))

                    # Two cases again one for ACES and one without
                    if "regional_indicator_a" in current:
                        tup = value_calc_A(current)
                        tup1 = tup[0]
                        tup2 = tup[1]
                        await message.channel.send(f"Your totals are: {tup1} and {tup2}")
                        if tup1 > 21 and tup2 > 21:
                            await message.channel.send(f"Bust!")
                            return
                        if tup1 == 21 or tup2 == 21:
                            await message.channel.send(f"You Win!")
                            return
                    else:
                        await message.channel.send(f"Your total is: {value_calc(current)}")
                        if value_calc(current) > 21:
                            await message.channel.send(f"Bust!")
                            return
                        if value_calc(current) == 21:
                            await message.channel.send(f"You Win!")
                            return
                elif msg.content == "!end":

                    # Calculate the dealers hand based on a random roll
                    dealer_num = 0
                    roll = random.randint(1, 3)
                    if roll == 1:
                        dealer_num = random.randint(10, 21)
                    elif roll == 2:
                        dealer_num = random.randint(15, 21)
                    elif roll == 3:
                        dealer_num = random.randint(18, 21)

                    # Two cases again Aces or no Aces
                    if "regional_indicator_a" in current:
                        tup = value_calc_A(current)
                        tup1 = tup[0]
                        tup2 = tup[1]
                        await message.channel.send(f"Dealer total is: {dealer_num}")
                        if tup1 < dealer_num and tup2 < dealer_num:
                            await message.channel.send(f"Dealer Wins!")
                            return
                        else:
                            await message.channel.send(f"You Win!")
                            return
                    else:
                        await message.channel.send(f"Dealer total is: {dealer_num}")
                        if value_calc(current) < dealer_num:
                            await message.channel.send(f"Dealer Wins!")
                            return
                        else:
                            await message.channel.send(f"You Win!")
                            return
        elif message.content.startswith('!img'):
            query = message.content[5:]
            if query == '':
                return
            url = 'https://www.google.com/search?tbm=isch&q=' + query
            page = requests.get(url)

            # gets html file of the url
            soup = BeautifulSoup(page.content, 'html.parser')

            # gets any data in the html file that has the 'img' tag on it
            image_tags = soup.find_all('img')

            links = []
            for image_tag in image_tags:
                # out of the gathered data, only get the one with links
                links.append(image_tag['src'])

            await message.channel.send('Inserting image')
            # returns the first link in the list (links[0] is the link to the logo not the image)
            await message.channel.send(links[1])
        else:
            return


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('TOKEN'))
