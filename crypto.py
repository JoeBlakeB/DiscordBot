#!/usr/bin/env python3

import requests
import discord

class crypto:
    help = {"list": True, "ListPriority": 8, "Title":"Crypto",
        "ShortHelp": "Get info on a cryptocurrency. *@{displayName} crypto <coin>*",
        "LongHelp": "Gives info for a cryptocurrency.\n"+
        "**@{displayName} crypto <coin>** to view cryptocurrency info.\n"+
        "For example: **@{displayName} crypto doge** for information about dogecoin.\n"+
        "Sources: *messari.io* & *exchangeratesapi.io*"}
    async def __new__(self, message, command, parentClass):
        if command[1].lower() in ["doge", "dogecoin", "btc", "bitcoin"]:
            command[1:2] = ["crypto", command[1]]

        if len(command) < 3:
            await message.channel.send("The fuck do you want? You need to say what crypto you want.")
            return

        name = command[2].upper()

        response = requests.get("https://data.messari.io/api/v1/assets/"+name+"/metrics")
        cryptoMetrics = response.json()

        try:
            if cryptoMetrics["status"]["error_code"] != 200:
                raise Exception(str(cryptoMetrics["status"]["error_code"]) +" "+ cryptoMetrics["status"]["error_message"])
        except KeyError: pass

        response = requests.get("https://data.messari.io/api/v1/assets/"+name+"/profile")
        cryptoProfile = response.json()
        response = requests.get("https://api.exchangeratesapi.io/latest?base=USD&symbols=GBP")
        exchangeRate = response.json()

        embed = discord.Embed()
        embed.title = cryptoMetrics["data"]["name"] + " stats (" +cryptoMetrics["data"]["symbol"]+ ")"
        embed.color = parentClass.__embedColor__()
        embed.url = "https://messari.io/asset/" + cryptoMetrics["data"]["symbol"]

        value = float(cryptoMetrics["data"]["market_data"]["price_usd"]) * float(exchangeRate["rates"]["GBP"])
        if 7 - len(str(int(value))) <= 2:
            value = round(value, 2)
        else:
            value = round(value, 7-len(str(int(value))))
        embed.description = "Value: **£{:,.6f}".format(value)
        for i in range(4):
            if embed.description[-1] == "0":
                embed.description = embed.description[:-1]

        embed.description += "**\n\n" + cryptoProfile["data"]["tagline"]

        embed.description += "\n\nAll Time High: £{:,.2f} at ".format(float(cryptoMetrics["data"]["all_time_high"]["price"]) * float(exchangeRate["rates"]["GBP"])) + cryptoMetrics["data"]["all_time_high"]["at"][:10]
        embed.description += "\nVolume (24 hours): " + str(cryptoMetrics["data"]["market_data"]["volume_last_24_hours"])
        embed.description += "\nReal Bolume (24 hours): " + str(cryptoMetrics["data"]["market_data"]["real_volume_last_24_hours"])
        embed.description += "\nPercent Change (1 hour): " + str(cryptoMetrics["data"]["market_data"]["percent_change_usd_last_1_hour"])
        embed.description += "\nPercent Change (24 hours): " + str(cryptoMetrics["data"]["market_data"]["percent_change_usd_last_24_hours"])
        embed.description += "\nMarket Cap: £{:,.2f}".format(float(cryptoMetrics["data"]["marketcap"]["current_marketcap_usd"]) * float(exchangeRate["rates"]["GBP"]))

        embed.description += "\n\nSupply: " + str(int(cryptoMetrics["data"]["supply"]["circulating"]))
        embed.description += "\nActive Addresses (24 hours): " + str(cryptoMetrics["data"]["blockchain_stats_24_hours"]["count_of_active_addresses"])
        embed.description += "\nTransaction Volume (24 hours): " + str(int(cryptoMetrics["data"]["blockchain_stats_24_hours"]["transaction_volume"]))

        await message.channel.send(embed=embed)

    def getValue(name):
        try:
            response = requests.get("https://data.messari.io/api/v1/assets/"+name+"/metrics")
            cryptoMetrics = response.json()
            response = requests.get("https://api.exchangeratesapi.io/latest?base=USD&symbols=GBP")
            exchangeRate = response.json()
            value = float(cryptoMetrics["data"]["market_data"]["price_usd"]) * float(exchangeRate["rates"]["GBP"])
            return value
        except:
            return 0
