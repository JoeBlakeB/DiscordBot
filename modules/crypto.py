#!/usr/bin/env python3

import requests
import traceback
import discord
import time

import baseClass
import keys

class crypto(baseClass.baseClass):
    async def crypto(self, message, commandContent):
        command = ["joebot"] + commandContent.split(" ")
        if command[1].lower()[0] == "!":
            command[0:1] = ["joebot", "crypto"]

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

        embed = discord.Embed()
        embed.title = cryptoMetrics["data"]["name"] + " stats (" +cryptoMetrics["data"]["symbol"]+ ")"
        embed.url = "https://messari.io/asset/" + cryptoMetrics["data"]["symbol"]

        value = float(cryptoMetrics["data"]["market_data"]["price_usd"]) * crypto.exchangeRate()
        if 7 - len(str(int(value))) <= 2:
            value = round(value, 2)
        else:
            value = round(value, 7-len(str(int(value))))
        embed.description = "Value: **£{:,.6f}".format(value)
        for i in range(4):
            if embed.description[-1] == "0":
                embed.description = embed.description[:-1]

        embed.description += "**\n\n" + cryptoProfile["data"]["tagline"]

        embed.description += "\n\nAll Time High: £{:,.2f} at ".format(float(cryptoMetrics["data"]["all_time_high"]["price"]) * crypto.exchangeRate()) + cryptoMetrics["data"]["all_time_high"]["at"][:10]
        embed.description += "\nVolume (24 hours): £{:,.2f}".format(cryptoMetrics["data"]["market_data"]["volume_last_24_hours"] * crypto.exchangeRate())
        try:
            embed.description += "\nReal Volume (24 hours): £{:,.2f}".format(cryptoMetrics["data"]["market_data"]["real_volume_last_24_hours"] * crypto.exchangeRate())
        except:
            pass
        try:
            embed.description += "\nPercent Change (1 hour): " + str(round(cryptoMetrics["data"]["market_data"]["percent_change_usd_last_1_hour"],4))
        except:
            pass
        try:
            embed.description += "\nPercent Change (24 hours): " + str(round(cryptoMetrics["data"]["market_data"]["percent_change_usd_last_24_hours"],4))
        except:
            pass
        try:
            embed.description += "\nMarket Cap: £{:,.2f}".format(float(cryptoMetrics["data"]["marketcap"]["current_marketcap_usd"]) * crypto.exchangeRate())
        except:
            pass

        embed.description += "\n\nSupply: " + str(int(cryptoMetrics["data"]["supply"]["circulating"]))
        embed.description += "\nActive Addresses (24 hours): " + str(cryptoMetrics["data"]["blockchain_stats_24_hours"]["count_of_active_addresses"])
        embed.description += "\nTransaction Volume (24 hours): " + str(int(cryptoMetrics["data"]["blockchain_stats_24_hours"]["transaction_volume"]))

        await message.channel.send(embed=embed)

    def getValue(name):
        try:
            response = requests.get("https://data.messari.io/api/v1/assets/"+name+"/metrics")
            cryptoMetrics = response.json()
            value = float(cryptoMetrics["data"]["market_data"]["price_usd"]) * crypto.exchangeRate()
            return value
        except requests.exceptions.ConnectionError:
            return 0
        except:
            traceback.print_exc()
            return 0

    lastGotRate = time.time() - (86400*3)
    oldRate = .72
    fixerIoAccessKey = keys.read("Fixer.io-Access-Key")

    def exchangeRate():
        try:
            if crypto.lastGotRate + (86400*2) < time.time():
                response = requests.get("http://data.fixer.io/api/latest?access_key=" + crypto.fixerIoAccessKey)
                exchangeRate = response.json()
                return exchangeRate["rates"]["GBP"] / exchangeRate["rates"]["USD"]
            else:
                return crypto.oldRate
        except KeyError:
             pass
        except:
            pass # shut up shut up shut up traceback.print_exc()
        return .72

crypto.mentionedCommands["crypto(?!\S)"] = [crypto.crypto, ["message", "commandContent", "typing"], {"self":crypto}]
crypto.exclamationCommands["crypto(?!\S)"] = [crypto.crypto, ["message", "commandContent", "typing"], {"self":crypto}]

crypto.exclamationCommands["doge(coin|)\Z"] = [crypto.crypto, ["message", "typing"], {"self":crypto, "commandContent":"crypto doge"}]
crypto.exclamationCommands["(btc|bitcoin)\Z"] = [crypto.crypto, ["message", "typing"], {"self":crypto, "commandContent":"crypto btc"}]

crypto.help["crypto"] = ["embed,include", {"title":"Crypto",
    "description": "Gives info for a cryptocurrency.\n"+
    "**<@796433833296658442> crypto <coin>** to view cryptocurrency info.\n"+
    "For example: **<@796433833296658442> crypto doge** for information about dogecoin.\n"+
    "Source: *messari.io*"}]
