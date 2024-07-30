import discord, requests, time, datetime, math
from discord.ext.commands import bot
from discord.ext import commands
import sys


class bard:
    def __init__(self):
        pass
    # main method running the bot
    def run(self):
        client = discord.Client(intents=discord.Intents.default())
        com = commands.Bot(command_prefix = 'bard ', intents=discord.Intents.default())
        riot = RiotGames()
        @com.event
        async def on_ready():
            print('bot running')
            channel = com.get_channel(949705034218762240)
            message = await channel.fetch_message(949757922332770394)
            await message.edit(content=self.create_rankings(949705034218762240))
            sys.exit()

        '''
        @com.event
        async def on_message(msg):
                if msg.content == "bard update":
                    print("updating")
                    channel = com.get_channel(949705034218762240)
                    message = await channel.fetch_message(949757922332770394)
                    await message.edit(content=self.create_rankings(949705034218762240))
                    msg.delete()
                    '''
        

        # starts bot
        with open("C:/Users/thoma/Desktop/VS code/Bard/API_Keys.txt") as f:
            for i, line in enumerate(f):
                if i == 1:
                    discord_key = line.rstrip()
        com.run(discord_key)

    

    def get_names(self, id):
        names = []
        with open(f'C:/Users/thoma/Desktop/VS code/Bard/{id}.txt', 'r', encoding = "utf-8") as f:
            for line in f:
                names.append(line.rstrip())
        return names

    def create_rankings(self, channelid):
        rankids = {'iron' : 0, 'bronze' : 1, 'silver' : 2, 'gold' : 3, 'platinum' : 4, 'diamond' : 5, 'master': 6, 'grandmaster' : 7, 'challenger' : 8}
        riot = RiotGames()
        names = self.get_names(channelid)
        people = {}
        peopleranks = {}
        for name in names:
            id = riot.get_summoner_id_new(name)
            response = riot.get_ranked_data(id).json()
            soloduo = list(filter(self.contains_soloduo, response))
            print(name)
            people[name] = soloduo[0]
            peopler = people[name]
            peopleranks[name] = peopler['tier']
        sortedpeople = {k: v for k, v in sorted(peopleranks.items(), key=lambda item: rankids[item[1].lower()])}
        peoplebyrank = list(sortedpeople.keys())
        for i in range(len(peoplebyrank)-1):
            for j in range(len(peoplebyrank) - 1):
                if people[peoplebyrank[j]]['rank'] < people[peoplebyrank[j+1]]['rank'] and people[peoplebyrank[j]]['tier'] == people[peoplebyrank[j+1]]['tier']:
                    peoplebyrank[j], peoplebyrank[j+1] = peoplebyrank[j+1], peoplebyrank[j]
        for i in range(len(peoplebyrank)-1):
            for j in range(len(peoplebyrank) - 1):
                if people[peoplebyrank[j]]['leaguePoints'] > people[peoplebyrank[j+1]]['leaguePoints'] and people[peoplebyrank[j]]['tier'] == people[peoplebyrank[j+1]]['tier'] and people[peoplebyrank[j]]['rank'] == people[peoplebyrank[j+1]]['rank']:
                    peoplebyrank[j], peoplebyrank[j+1] = peoplebyrank[j+1], peoplebyrank[j]
        peoplebyrank.reverse()

        str = ""
        i = 1
        for person in peoplebyrank:
            tier = people[person]['tier']
            rank = people[person]['rank']
            leaguePoints = people[person]['leaguePoints']
            wr = math.floor((people[person]['wins'] /(people[person]['wins'] + people[person]['losses']))*100)
            games = people[person]['wins'] + people[person]['losses']
            str += f'{i}: {person} - {tier} {rank} {leaguePoints} LP with a {wr}% win rate in {games} games\n'
            i+=1
        return str
        
    
    def contains_soloduo(self, info):
        if ('queueType', 'RANKED_SOLO_5x5') in info.items():
            return True
        return False
        
    


class RiotGames:
    def __init__(self):
        with open("C:/Users/thoma/Desktop/VS code/Bard/API_Keys.txt") as f:
            self.APIkey = f.readline().rstrip()
    def get_summoner_id(self, summonername):
        response = requests.get(f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonername}?api_key={self.APIkey}')
        responsejson = response.json()
        print(responsejson)
        summonerid = responsejson['id']
        return summonerid
    def get_summoner_id_new(self, summonername):
        gameName = summonername.split('#')[0]
        tagLine = summonername.split('#')[1]
        response = requests.get(f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={self.APIkey}')
        responsejson = response.json()
        print(responsejson)
        puuid = responsejson['puuid']
        response = requests.get(f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.APIkey}')
        responsejson = response.json()
        summonerid = responsejson['id']
        return summonerid
    def get_ranked_data(self, id):
        response = requests.get(f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={self.APIkey}')
        return response
        


def main():
    bot = bard()
    bot.run()

if __name__ == "__main__":
    main()