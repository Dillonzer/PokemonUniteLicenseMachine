import asyncio
import aiohttp
from consts import Consts
from data import Data
from embedTypes import EmbedTypes
from postgres import PostgresDB
import interactions
from interactions.ext.wait_for import setup
from interactions.ext.tasks import IntervalTrigger, create_task

guild_ids = [642081591371497472]

client = interactions.Client(token=Consts.TOKEN,
presence=interactions.ClientPresence(
    status=interactions.StatusType.ONLINE,
    activities=[
        interactions.PresenceActivity(
            name="Pokémon Unite",
            type=interactions.PresenceActivityType.COMPETING
            )
        ]
    )
)

setup(client)

data = Data()
database = PostgresDB()

def BuildEmbed(dataBlock,typeOfEmbed,move_tier,level):
    e = interactions.Embed()
    e.title= dataBlock['name']
    e.color = interactions.Color.yellow()
    e.set_thumbnail(url=dataBlock['imageLink'])
    e.set_footer(icon_url="https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/unite-db-icon.png",text="Powered by unite-db")
    if(typeOfEmbed != EmbedTypes.ITEM and typeOfEmbed != EmbedTypes.EMBLEM):
        e.description = f"{dataBlock['type']['distance']} - {dataBlock['type']['style']} - {dataBlock['type']['difficulty']}"
        if(typeOfEmbed == EmbedTypes.LICENSE or typeOfEmbed == EmbedTypes.STATS):
            e.add_field(name="Attack Type",value=dataBlock['type']['attackType'],inline=False)            
            if(typeOfEmbed == EmbedTypes.STATS):
                stats = f"HP: {dataBlock['stats']['levelStats'][level]['hp']}\nAttack: {dataBlock['stats']['levelStats'][level]['attack']}\nDefense: {dataBlock['stats']['levelStats'][level]['defense']}\nSp.A: {dataBlock['stats']['levelStats'][level]['sp_Attack']}\nSp.D: {dataBlock['stats']['levelStats'][level]['sp_Defense']}\nCrit: {dataBlock['stats']['levelStats'][level]['critRate']}%\nCooldown Reduction: {dataBlock['stats']['levelStats'][level]['cooldownReduction']}\nLifesteal: {dataBlock['stats']['levelStats'][level]['lifesteal']}"
                e.add_field(name=f"Stats at Level {level+1}", value=stats, inline=True)        
        if(typeOfEmbed == EmbedTypes.LICENSE or typeOfEmbed == EmbedTypes.MOVES):
            if(move_tier == "all"):
                e.add_field(name="Default",value=f"• **{dataBlock['moves'][0]['name']}** ({dataBlock['moves'][0]['type']}): {dataBlock['moves'][0]['description']}\n• **{dataBlock['moves'][1]['name']}** ({dataBlock['moves'][1]['type']}): {dataBlock['moves'][1]['description']}",inline=False) 
                e.add_field(name="Moves 1 / 2",value=f"• **{dataBlock['moves'][2]['name']} ({dataBlock['moves'][2]['level']})** ({dataBlock['moves'][2]['type']})  {dataBlock['moves'][2]['cooldown']}s 🕓: {dataBlock['moves'][2]['description']} [UPGRADE: {dataBlock['moves'][2]['upgrade']}]\n• **{dataBlock['moves'][3]['name']} ({dataBlock['moves'][3]['level']})** ({dataBlock['moves'][3]['type']})  {dataBlock['moves'][3]['cooldown']}s 🕓: {dataBlock['moves'][3]['description']} [UPGRADE: {dataBlock['moves'][3]['upgrade']}]",inline=False)  
                e.add_field(name="Move 1 Upgrades",value=f"• **{dataBlock['moves'][4]['name']} (Level {dataBlock['moves'][4]['level']})** ({dataBlock['moves'][4]['type']})  {dataBlock['moves'][4]['cooldown']}s 🕓: {dataBlock['moves'][4]['description']} [UPGRADE: Level {dataBlock['moves'][4]['upgrade']}]\n• **{dataBlock['moves'][5]['name']} (Level {dataBlock['moves'][5]['level']})** ({dataBlock['moves'][5]['type']})  {dataBlock['moves'][5]['cooldown']}s 🕓: {dataBlock['moves'][5]['description']} [UPGRADE: Level {dataBlock['moves'][5]['upgrade']}]",inline=False)
                e.add_field(name="Move 2 Upgrades",value=f"• **{dataBlock['moves'][6]['name']} (Level {dataBlock['moves'][6]['level']})** ({dataBlock['moves'][6]['type']})  {dataBlock['moves'][6]['cooldown']}s 🕓: {dataBlock['moves'][6]['description']} [UPGRADE: Level {dataBlock['moves'][6]['upgrade']}]\n• **{dataBlock['moves'][7]['name']} (Level {dataBlock['moves'][7]['level']})** ({dataBlock['moves'][7]['type']})  {dataBlock['moves'][7]['cooldown']}s 🕓: {dataBlock['moves'][7]['description']} [UPGRADE: Level {dataBlock['moves'][7]['upgrade']}]",inline=False)
                e.add_field(name="Unite Move",value=f"• **{dataBlock['moves'][8]['name']} (Level {dataBlock['moves'][8]['level']})** ({dataBlock['moves'][8]['type']}): {dataBlock['moves'][8]['description']}",inline=False)
            elif(move_tier == "default"):
                e.add_field(name="Default",value=f"• **{dataBlock['moves'][0]['name']}**: {dataBlock['moves'][0]['description']}\n• **{dataBlock['moves'][1]['name']}** ({dataBlock['moves'][1]['type']}): {dataBlock['moves'][1]['description']}",inline=False)               
            elif(move_tier == "stage1"):
                e.add_field(name="Moves 1 / 2",value=f"• **{dataBlock['moves'][2]['name']} ({dataBlock['moves'][2]['level']})** ({dataBlock['moves'][2]['type']})  {dataBlock['moves'][2]['cooldown']}s 🕓: {dataBlock['moves'][2]['description']} [UPGRADE: {dataBlock['moves'][2]['upgrade']}]\n• **{dataBlock['moves'][3]['name']} ({dataBlock['moves'][3]['level']})** ({dataBlock['moves'][3]['type']})  {dataBlock['moves'][3]['cooldown']}s 🕓: {dataBlock['moves'][3]['description']} [UPGRADE: {dataBlock['moves'][3]['upgrade']}]",inline=False)  
            elif(move_tier == "stage2"):
                e.add_field(name="Move 1 Upgrades",value=f"• **{dataBlock['moves'][4]['name']} (Level {dataBlock['moves'][4]['level']})** ({dataBlock['moves'][4]['type']})  {dataBlock['moves'][4]['cooldown']}s 🕓: {dataBlock['moves'][4]['description']} [UPGRADE: Level {dataBlock['moves'][4]['upgrade']}]\n• **{dataBlock['moves'][5]['name']} (Level {dataBlock['moves'][5]['level']})** ({dataBlock['moves'][5]['type']})  {dataBlock['moves'][5]['cooldown']}s 🕓: {dataBlock['moves'][5]['description']} [UPGRADE: Level {dataBlock['moves'][5]['upgrade']}]",inline=False)
            elif(move_tier == "stage3"):
                e.add_field(name="Move 2 Upgrades",value=f"• **{dataBlock['moves'][6]['name']} (Level {dataBlock['moves'][6]['level']})** ({dataBlock['moves'][6]['type']})  {dataBlock['moves'][6]['cooldown']}s 🕓: {dataBlock['moves'][6]['description']} [UPGRADE: Level {dataBlock['moves'][6]['upgrade']}]\n• **{dataBlock['moves'][7]['name']} (Level {dataBlock['moves'][7]['level']})** ({dataBlock['moves'][7]['type']})  {dataBlock['moves'][7]['cooldown']}s 🕓: {dataBlock['moves'][7]['description']} [UPGRADE: Level {dataBlock['moves'][7]['upgrade']}]",inline=False)
            elif(move_tier == "unite"): 
                e.add_field(name="Unite Move",value=f"• **{dataBlock['moves'][8]['name']} (Level {dataBlock['moves'][8]['level']}) ** ({dataBlock['moves'][8]['type']}): {dataBlock['moves'][8]['description']}",inline=False)
        if(typeOfEmbed == EmbedTypes.ATTACK_FORMULAS):         
            printFormulaPassive = "N/A"
            printFormulaBasic = "N/A"
            try:  
                for formulaMoves in dataBlock['moves'][1]['attacks']:
                    if(printFormulaBasic == "N/A"):
                        printFormulaBasic = f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                    else:                    
                        printFormulaBasic += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"                        
            except:
                printFormulaBasic = "N/A"

            printFormula1 = "N/A"
            try:
                for formulaMoves in dataBlock['moves'][2]['attacks']:
                    if(printFormula1 == "N/A"):
                        printFormula1 = f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                    else:                    
                        printFormula1 += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
            except:
                printFormula1 = "N/A"

            printFormula2 = "N/A"
            try:
                for formulaMoves in dataBlock['moves'][3]['attacks']:                        
                    if(printFormula2 == "N/A"):
                        printFormula2 = f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                    else:                    
                        printFormula2 += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"            
            except:
                printFormula1 = "N/A"

            printFormula3NonUpgrade = "N/A"
            printFormula3Upgrade = "N/A"

            try:
                for formulaMoves in dataBlock['moves'][4]['attacks']:
                    if(not formulaMoves['upgradeFormula']):                    
                        if(printFormula3NonUpgrade == "N/A"):
                            printFormula3NonUpgrade = f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                        else:                    
                            printFormula3NonUpgrade += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                    else:
                        if(printFormula3Upgrade == "N/A"):
                            printFormula3Upgrade = f"{formulaMoves['type']} `{formulaMoves['formula']}`"
                        else:                    
                            printFormula3Upgrade += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
            except:
                printFormula3NonUpgrade = "N/A"
                printFormula3Upgrade = "N/A"

            printFormula4NonUpgrade = "N/A"
            printFormula4Upgrade = "N/A"

            try:            
                for formulaMoves in dataBlock['moves'][5]['attacks']:
                    if(not formulaMoves['upgradeFormula']):     
                        if(printFormula4NonUpgrade == "N/A"):
                            printFormula4NonUpgrade = f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                        else:                    
                            printFormula4NonUpgrade += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                    else:
                        if(printFormula4Upgrade == "N/A"):
                            printFormula4Upgrade = f"{formulaMoves['type']} `{formulaMoves['formula']}`"
                        else:                    
                            printFormula4Upgrade += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`" 
            except:
                printFormula4NonUpgrade = "N/A"
                printFormula4Upgrade = "N/A"

            printFormula5NonUpgrade = "N/A"
            printFormula5Upgrade = "N/A"

            try:
                for formulaMoves in dataBlock['moves'][6]['attacks']:
                    if(not formulaMoves['upgradeFormula']):           
                        if(printFormula5NonUpgrade == "N/A"):
                            printFormula5NonUpgrade = f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                        else:                    
                            printFormula5NonUpgrade += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                    else:
                        if(printFormula5Upgrade == "N/A"):
                            printFormula5Upgrade = f"{formulaMoves['type']} `{formulaMoves['formula']}`"
                        else:                    
                            printFormula5Upgrade += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`" 
            except: 
                printFormula5NonUpgrade = "N/A"
                printFormula5Upgrade = "N/A"


            printFormula6NonUpgrade = "N/A"
            printFormula6Upgrade = "N/A"

            try:
                for formulaMoves in dataBlock['moves'][7]['attacks']:
                    if(not formulaMoves['upgradeFormula']):           
                        if(printFormula6NonUpgrade == "N/A"):
                            printFormula6NonUpgrade = f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                        else:                    
                            printFormula6NonUpgrade += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                    else:
                        if(printFormula6Upgrade == "N/A"):
                            printFormula6Upgrade = f"{formulaMoves['type']} `{formulaMoves['formula']}`"
                        else:                    
                            printFormula6Upgrade += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`" 
            except:
                printFormula6NonUpgrade = "N/A"
                printFormula6Upgrade = "N/A"

            printFormulaUnite = "N/A"
            try:
                for formulaMoves in dataBlock['moves'][8]['attacks']:
                    if(printFormulaUnite == "N/A"):
                        printFormulaUnite = f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
                    else:                    
                        printFormulaUnite += f"\n{formulaMoves['type']} `{formulaMoves['formula']}`"
            except:
                printFormulaUnite = "N/A"

            if(move_tier == "all"):
                e.add_field(name="Default",value=f"• **{dataBlock['moves'][0]['name']}**: {printFormulaPassive}\n• **{dataBlock['moves'][1]['name']}** ({dataBlock['moves'][1]['type']}): {printFormulaBasic}",inline=False)       
                e.add_field(name="Moves 1 / 2",value=f"• **{dataBlock['moves'][2]['name']} ({dataBlock['moves'][2]['level']})** ({dataBlock['moves'][2]['type']})  {dataBlock['moves'][2]['cooldown']}s 🕓: {printFormula1}\n• **{dataBlock['moves'][3]['name']} ({dataBlock['moves'][3]['level']})** ({dataBlock['moves'][3]['type']})  {dataBlock['moves'][3]['cooldown']}s 🕓: {printFormula2}",inline=False)  
                if(dataBlock['name'] == 'Snorlax'):
                    e.add_field(name="Move 1 Upgrades",value=f"**{dataBlock['moves'][4]['name']} (Level {dataBlock['moves'][4]['level']})** ({dataBlock['moves'][4]['type']})  {dataBlock['moves'][4]['cooldown']}s 🕓: {printFormula3NonUpgrade}\n[UPGRADE: {printFormula3Upgrade}]\n• **{dataBlock['moves'][5]['name']} (Level {dataBlock['moves'][5]['level']})** ({dataBlock['moves'][5]['type']})  {dataBlock['moves'][5]['cooldown']}s 🕓: Flail is very complicated and cannot fit inside a Discord Embed. Please check out the details on https://unite-db.com/pokemon/snorlax")
                else:
                    e.add_field(name="Move 1 Upgrades",value=f"• **{dataBlock['moves'][4]['name']} (Level {dataBlock['moves'][4]['level']})** ({dataBlock['moves'][4]['type']})  {dataBlock['moves'][4]['cooldown']}s 🕓: {printFormula3NonUpgrade}\n[UPGRADE: {printFormula3Upgrade}]\n• **{dataBlock['moves'][5]['name']} (Level {dataBlock['moves'][5]['level']})** ({dataBlock['moves'][5]['type']})  {dataBlock['moves'][5]['cooldown']}s 🕓: {printFormula4NonUpgrade}\n[UPGRADE: {printFormula4Upgrade}]",inline=False)
                e.add_field(name="Move 2 Upgrades",value=f"• **{dataBlock['moves'][6]['name']} (Level {dataBlock['moves'][6]['level']})** ({dataBlock['moves'][6]['type']})  {dataBlock['moves'][6]['cooldown']}s 🕓: {printFormula5NonUpgrade}\n[UPGRADE: {printFormula5Upgrade}]\n• **{dataBlock['moves'][7]['name']} (Level {dataBlock['moves'][7]['level']})** ({dataBlock['moves'][7]['type']})  {dataBlock['moves'][7]['cooldown']}s 🕓: {printFormula6NonUpgrade}\n[UPGRADE: {printFormula6Upgrade}]",inline=False)
                e.add_field(name="Unite Move",value=f"• **{dataBlock['moves'][8]['name']} (Level {dataBlock['moves'][8]['level']}) ** ({dataBlock['moves'][8]['type']}): {printFormulaUnite}",inline=False)
            elif(move_tier == "default"):
                e.add_field(name="Default",value=f"• **{dataBlock['moves'][0]['name']}**: {printFormulaPassive}\n• **{dataBlock['moves'][1]['name']}** ({dataBlock['moves'][1]['type']}): {printFormulaBasic}",inline=False)               
            elif(move_tier == "stage1"):
                e.add_field(name="Moves 1 / 2",value=f"• **{dataBlock['moves'][2]['name']} ({dataBlock['moves'][2]['level']})** ({dataBlock['moves'][2]['type']})  {dataBlock['moves'][2]['cooldown']}s 🕓: {printFormula1}\n• **{dataBlock['moves'][3]['name']} ({dataBlock['moves'][3]['level']})** ({dataBlock['moves'][3]['type']})  {dataBlock['moves'][3]['cooldown']}s 🕓: {printFormula2}",inline=False)  
            elif(move_tier == "stage2"):
                if(dataBlock['name'] == 'Snorlax'):
                    e.add_field(name="Move 1 Upgrades",value=f"**{dataBlock['moves'][4]['name']} (Level {dataBlock['moves'][4]['level']})** ({dataBlock['moves'][4]['type']})  {dataBlock['moves'][4]['cooldown']}s 🕓: {printFormula3NonUpgrade} [UPGRADE: {printFormula3Upgrade}]\n• **{dataBlock['moves'][5]['name']} (Level {dataBlock['moves'][5]['level']})** ({dataBlock['moves'][5]['type']})  {dataBlock['moves'][5]['cooldown']}s 🕓: Flail is very complicated and cannot fit inside a Discord Embed. Please check out the details on https://unite-db.com/pokemon/snorlax")
                else:
                    e.add_field(name="Move 1 Upgrades",value=f"• **{dataBlock['moves'][4]['name']} (Level {dataBlock['moves'][4]['level']})** ({dataBlock['moves'][4]['type']})  {dataBlock['moves'][4]['cooldown']}s 🕓: {printFormula3NonUpgrade} [UPGRADE: {printFormula3Upgrade}]\n• **{dataBlock['moves'][5]['name']} (Level {dataBlock['moves'][5]['level']})** ({dataBlock['moves'][5]['type']})  {dataBlock['moves'][5]['cooldown']}s 🕓: {printFormula4NonUpgrade} [UPGRADE: {printFormula4Upgrade}]",inline=False)
            elif(move_tier == "stage3"):
                e.add_field(name="Move 2 Upgrades",value=f"• **{dataBlock['moves'][6]['name']} (Level {dataBlock['moves'][6]['level']})** ({dataBlock['moves'][6]['type']})  {dataBlock['moves'][6]['cooldown']}s 🕓: {printFormula5NonUpgrade} [UPGRADE: {printFormula5Upgrade}]\n• **{dataBlock['moves'][7]['name']} (Level {dataBlock['moves'][7]['level']})** ({dataBlock['moves'][7]['type']})  {dataBlock['moves'][7]['cooldown']}s 🕓: {printFormula6NonUpgrade} [UPGRADE: {printFormula6Upgrade}]",inline=False)
            elif(move_tier == "unite"): 
                e.add_field(name="Unite Move",value=f"• **{dataBlock['moves'][8]['name']} (Level {dataBlock['moves'][8]['level']}) ** ({dataBlock['moves'][8]['type']}): {printFormulaUnite}",inline=False)
            
            e.color = interactions.Color.yellow()
    elif(typeOfEmbed == EmbedTypes.ITEM):
        e.description = dataBlock['description']
        e.add_field(name="Type",value=dataBlock['type'], inline=False)
        if(dataBlock["levelPerk"] != None):
            levelPerks = f"Level 1: {dataBlock['levelPerk']['level1']}\nLevel 10: {dataBlock['levelPerk']['level10']}\nLevel 20: {dataBlock['levelPerk']['level20']}"
            e.add_field(name="Level Perks",value=levelPerks,inline=False)
        if(dataBlock['bonus'] != None and len(dataBlock['bonus']) > 0):
            bonuses = ""
            for bonus in dataBlock['bonus']:
                bonuses += "• " + bonus + "\n"
            e.add_field(name="Bonuses",value=bonuses, inline=False)
        e.color = interactions.Color.blurple()
    elif(typeOfEmbed == EmbedTypes.EMBLEM):
        stats = f"HP: {dataBlock['stats']['hp']}\nSp. Attack: {dataBlock['stats']['spAttack']}\nDefense: {dataBlock['stats']['defense']}\nAttack: {dataBlock['stats']['attack']}\nSp. Defense: {dataBlock['stats']['spDefense']}\nCrit: {dataBlock['stats']['crit']}\nSpeed: {dataBlock['stats']['speed']}"
        e.add_field(name="Stat Weights",value=stats, inline=False)
        if(dataBlock['grade'] == "Gold"):
            e.color = interactions.Color.yellow()
        if(dataBlock['grade'] == "Silver"):
            e.color = interactions.Color.white()
        if(dataBlock['grade'] == "Bronze"):
            e.color = interactions.Color.black()
        colour= ",".join(dataBlock['colour'])
        e.add_field(name="Colour",value=colour,inline=False)
        for perk in dataBlock['setPerks']:
            e.add_field(name=f"{perk['colour']} Bonus",value=f"{perk['bonusAmounts'][0]['amountNeeded']} - {perk['bonusAmounts'][0]['bonusAmount']}% {perk['statAffected']}\n{perk['bonusAmounts'][1]['amountNeeded']} - {perk['bonusAmounts'][1]['bonusAmount']}% {perk['statAffected']}\n{perk['bonusAmounts'][2]['amountNeeded']} - {perk['bonusAmounts'][2]['bonusAmount']}% {perk['statAffected']}")
    return e
        
@client.command(name="info",
            description="Get information about the bot")
async def PrintCommands(ctx):
    e = interactions.Embed()
    e.color = interactions.Color.blurple()
    e.set_author(name="Pokemon Unite License Viewer",icon_url=Consts.LOGO_ADDRESS)
    e.title = "Information!"
    e.description = "Thanks for using Pokemon Unite License Checker powered by [unite-db](https://unite-db.com/)! Visit my [Top.GG](https://top.gg/bot/867595735380918272) page! If you'd like to support what I do please follow me on [Patreon](https://www.patreon.com/bePatron?u=34112337)\nDue to memory issues I have temporarily disabled profiles. It's costing me too much on my hosting provider currently. Looking into other options. Thank you for your patience."
    commands = "• `/license`: Displays information for that License!\n"
    commands += "• `/item`: Displays information for that Item!\n"
    commands += "• `/emblem`: Displays information about specific Emblems!\n"
    commands += "• `/moves`: Displays the move set you want to see for that Pokemon!\n"
    commands += "• `/attack_math`: Displays the attack formulas for a specific Pokemon!\n"
    commands += "• `/stats`: Shows you the stats for that Pokemon!\n"
    commands += "• `/medals`: Shows you a list of the Medals and what they are for!\n"
    
    e.add_field(name="Commands", value=commands, inline=False)
    e.set_footer(text="Created by Dillonzer")

    await ctx.send(embeds = e, ephemeral=True)

@client.command(name="license",
            description="Get all the information about the Pokemon!",
            options=[
            interactions.Option(
                name="name",
                description="Name of the Pokemon",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ])
async def LicenseGrabber(ctx,name):
    await ctx.defer()
    spellingCorrection = data.nameCorrection(name.lower())
    
    if(spellingCorrection != name.lower() and spellingCorrection != ""):
        name = spellingCorrection
    try:
        for val in data.pokemon:
            if name.lower() == val['name'].lower():
                e = BuildEmbed(val,EmbedTypes.LICENSE,"all",None) 
                await ctx.send(embeds = e)
                return          
    except Exception as error:
        for val in data.pokemon:
            if name.lower() == val['name'].lower():
                e = interactions.Embed()
                e.title= val['name']
                e.set_thumbnail(url=val['imageLink'])
                e.set_footer(icon_url="https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/unite-db-icon.png",text="Powered by unite-db")
                e.description = "Looks like the info you are looking for doesn't fit into a Discord Embed! (Max 1024 Characters). You can check out the information on [Unite-DB](https://unite-db.com/pokemon/"+val['name']+")!"
                e.color = interactions.Color.blurple()  
                await ctx.send(embeds = e)
                return          
         

    e = interactions.Embed()
    e.title= "Woops!"
    e.description = f"Looks like we cannot find {name}."
    e.color = interactions.Color.red()
    await ctx.send(embeds = e)

@client.autocomplete(command="license",name="name")
async def autocomplete_license(ctx, user_input: str = ""):
    try:
        choices = [
        interactions.Choice(name=item, value=item) for item in data.autocompleteNames if user_input.lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.populate(choices)
    except:
        pass

@client.command(name="item",
            description="Get information about the item!",
            options=[
            interactions.Option(
                name="name",
                description="Name of the Item",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            )
        ])
async def ItemGrabber(ctx,name):
    await ctx.defer()
    spellingName = name.lower().replace("sp atk specs","sp. atk. specs")
    spellingName = spellingName.replace("special attack specs","sp. atk. specs")
    spellingName = spellingName.replace("exp share","exp. share")
    spellingName = spellingName.replace("experience share","exp. share")
    
    spellingCorrection = data.itemCorrection(spellingName)
    
    if(spellingCorrection != spellingName and spellingCorrection != ""):
        spellingName = spellingCorrection
    try:
        for val in data.items:
            if spellingName == val['name'].lower():
                pkmnData = val
                e = BuildEmbed(pkmnData,EmbedTypes.ITEM,None,None)
                await ctx.send(embeds = e)
                return
    except Exception as error:
        print(error)  
    
    

    e = interactions.Embed()
    e.title= "Woops!"
    e.description = f"Looks like we cannot find {name}."
    e.color = interactions.Color.red()
    await ctx.send(embeds = e)

@client.autocomplete(command="item",name="name")
async def autocomplete_item(ctx, user_input: str = ""):
    try:
        choices = [
        interactions.Choice(name=item, value=item) for item in data.autocompleteItems if user_input.lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.populate(choices)
    except:
        pass

@client.command(name="emblem",
            description="Get information about specific Emblems!",
            options=[
            interactions.Option(
                name="colour_one",
                description="One colour of the Emblem",
                type=interactions.OptionType.STRING,
                required=False,
                choices=[
                    interactions.Choice(
                    name="Black",
                    value="Black"
                    ),
                    interactions.Choice(
                    name="Blue",
                    value="Blue"
                    ),
                    interactions.Choice(
                    name="Green",
                    value="Green"
                    ),
                    interactions.Choice(
                    name="Brown",
                    value="Brown"
                    ),
                    interactions.Choice(
                    name="Pink",
                    value="Pink"
                    ),
                    interactions.Choice(
                    name="Purple",
                    value="Purple"
                    ),
                    interactions.Choice(
                    name="Red",
                    value="Red"
                    ),
                    interactions.Choice(
                    name="Yellow",
                    value="Yellow"
                    ),
                    interactions.Choice(
                    name="White",
                    value="White"
                    )
                ]
            ),
            interactions.Option(
                name="colour_two",
                description="Second colour of the Emblem",
                type=interactions.OptionType.STRING,
                required=False,
                choices=[
                    interactions.Choice(
                    name="Black",
                    value="Black"
                    ),
                    interactions.Choice(
                    name="Blue",
                    value="Blue"
                    ),
                    interactions.Choice(
                    name="Green",
                    value="Green"
                    ),
                    interactions.Choice(
                    name="Brown",
                    value="Brown"
                    ),
                    interactions.Choice(
                    name="Pink",
                    value="Pink"
                    ),
                    interactions.Choice(
                    name="Purple",
                    value="Purple"
                    ),
                    interactions.Choice(
                    name="Red",
                    value="Red"
                    ),
                    interactions.Choice(
                    name="Yellow",
                    value="Yellow"
                    ),
                    interactions.Choice(
                    name="White",
                    value="White"
                    )
                ]
            ),            
            interactions.Option(
                name="name",
                description="Name of the Pokemon on the Emblem",
                type=interactions.OptionType.STRING,
                required=False,
                autocomplete=True
            ),
            interactions.Option(
                name="tier",
                description="Tier of Emblem",
                type=interactions.OptionType.STRING,
                required=False,
                choices=[
                    interactions.Choice(
                    name="Bronze",
                    value="bronze"
                    ),
                    interactions.Choice(
                    name="Silver",
                    value="silver"
                    ),
                    interactions.Choice(
                    name="Gold",
                    value="gold"
                    )
                ]
            )
        ])
async def EmblemGrabber(ctx,colour_one = None,colour_two = None,name = None,tier = None):
    await ctx.defer()
    user = ctx.author
    count = 0
    embeddedArray = []
    foundEmblem = False
    try:        
        if(name is not None):
            spellingCorrection = data.emblemCorrection(name)
            
            if(spellingCorrection != name and spellingCorrection != ""):
                name = spellingCorrection

        for val in data.emblems:
            if(colour_one is None and colour_two is None and name is None and tier is None):                
                e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                embeddedArray.append(e)
                foundEmblem = True
            if(colour_one is not None and colour_two is None and name is None and tier is None):
                if colour_one in val['colour']:
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is None and colour_two is not None and name is None and tier is None):
                if colour_two in val['colour']:
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is None and colour_two is None and name is not None and tier is None):                
                if name.lower() == val['name'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is None and colour_two is None and name is None and tier is not None):
                if tier == val['grade'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is not None and colour_two is not None and name is None and tier is None):
                if colour_one in val['colour'] and colour_two in val['colour']:
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is not None and colour_two is None and name is not None and tier is None):
                if colour_one in val['colour'] and name.lower() == val['name'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is not None and colour_two is None and name is None and tier is not None):
                if colour_one in val['colour'] and tier == val['grade'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is not None and colour_two is not None and name is not None and tier is None):
                if colour_one in val['colour'] and colour_two in val['colour'] and name.lower() == val['name'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True            
            if(colour_one is not None and colour_two is not None and name is None and tier is not None):
                if colour_one in val['colour'] and colour_two in val['colour'] and tier == val['grade'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True                   
            if(colour_one is not None and colour_two is not None and name is not None and tier is not None):
                if colour_one in val['colour'] and colour_two in val['colour'] and tier == val['grade'].lower() and name.lower() == val['name'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is None and colour_two is not None and name is not None and tier is None):
                if colour_two in val['colour'] and name.lower() == val['name'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
            if(colour_one is None and colour_two is not None and name is None and tier is not None):
                if colour_two in val['colour'] and tier == val['grade'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True            
            if(colour_one is None and colour_two is None and name is not None and tier is not None):
                if name.lower() == val['name'].lower() and tier == val['grade'].lower():
                    e = BuildEmbed(val,EmbedTypes.EMBLEM,None,None)
                    embeddedArray.append(e)
                    foundEmblem = True
    except Exception as error:
        print(error)  

    if not foundEmblem:
        e = interactions.Embed()
        e.title= "Woops!"
        e.description = f"Looks like we couldn't find those Emblems."
        e.color = interactions.Color.red()
        embeddedArray.append(e) 

    maxEmbed = len(embeddedArray)

    async def ButtonClick(button_ctx: interactions.ComponentContext):
        nonlocal count
        if button_ctx.custom_id == f"prev{ctx.id}" and button_ctx.author == user:
            if count - 1 >= 0:                        
                count = count - 1
                await button_ctx.edit(embeds = embeddedArray[count])
            else:
                count = maxEmbed - 1
                await button_ctx.edit(embeds = embeddedArray[count])
        elif button_ctx.custom_id == f"next{ctx.id}" and button_ctx.author == user:
            if count + 1 < maxEmbed:
                count = count + 1
                await button_ctx.edit(embeds = embeddedArray[count])
            else:
                count = 0
                await button_ctx.edit(embeds = embeddedArray[count])                        
        else:
            try:                                                    
                await button_ctx.author.send(Consts.ONLY_REQUESTOR_CAN_TOGGLE)
            except:
                pass

    if maxEmbed > 1:  
        descCount = 0
        for es in embeddedArray:
            descCount = descCount + 1
            es.description = "Showing " + str(descCount) + "/" + str(maxEmbed) + ". Traverse the Emblems with the buttons below."

        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="Previous",
                custom_id=f"prev{ctx.id}"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="Next",
                custom_id=f"next{ctx.id}"
            )
        ]
        action_row = interactions.ActionRow.new(*buttons)
        await ctx.send(embeds = embeddedArray[0], components=action_row) 
        try:       
            button_ctx: interactions.ComponentContext = await client.wait_for_component(components=action_row, check=ButtonClick, timeout=60)  
        except asyncio.TimeoutError:
            # When it times out, edit the original message and remove the button(s)
            return await ctx.edit(components=[])
    else:        
        msg = await ctx.send(embeds = embeddedArray[0]) 

@client.autocomplete(command="emblem",name="name")
async def autocomplete_emblem(ctx, user_input: str = ""):
    try:
        choices = [
        interactions.Choice(name=item, value=item) for item in data.autocompleteEmblems if user_input.lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.populate(choices)
    except:
        pass

@client.command(name="stats",
            description="Get stats of the Pokemon!",
            options=[
            interactions.Option(
                name="name",
                description="Name of the Pokemon",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True,
            ),
            interactions.Option(
                name="level",
                description="What level do you want to look at?",
                type=interactions.OptionType.INTEGER,
                required = True,
                choices=[
                    interactions.Choice(
                    name="1",
                    value=0
                    ),
                    interactions.Choice(
                    name="2",
                    value=1
                    ),
                    interactions.Choice(
                    name="3",
                    value=2
                    ),
                    interactions.Choice(
                    name="4",
                    value=3
                    ),
                    interactions.Choice(
                    name="5",
                    value=4
                    ),
                    interactions.Choice(
                    name="6",
                    value=5
                    ),
                    interactions.Choice(
                    name="7",
                    value=6
                    ),
                    interactions.Choice(
                    name="8",
                    value=7
                    ),
                    interactions.Choice(
                    name="9",
                    value=8
                    ),
                    interactions.Choice(
                    name="10",
                    value=9
                    ),
                    interactions.Choice(
                    name="11",
                    value=10
                    ),
                    interactions.Choice(
                    name="12",
                    value=11
                    ),
                    interactions.Choice(
                    name="13",
                    value=12
                    ),
                    interactions.Choice(
                    name="14",
                    value=13
                    ),
                    interactions.Choice(
                    name="15",
                    value=14
                    )
                ]
            )
        ])
async def StatsGrabber(ctx,name,level):
    await ctx.defer()

    async def NewStat(button_ctx: interactions.ComponentContext):
        try:
            if(button_ctx.author == ctx.author):
                levelSelect = button_ctx.data.values[0].replace(str(ctx.id),"")
                e = BuildEmbed(val,EmbedTypes.STATS,None,int(levelSelect))
                await button_ctx.edit(embeds = e)          
            else:                    
                try:                                                    
                    await button_ctx.author.send(Consts.ONLY_REQUESTOR_CAN_TOGGLE)
                except:
                    pass
        except Exception as e:
                print(e) 

    try:
       for val in data.pokemon:
            if name.lower() == val['name'].lower():
                e = BuildEmbed(val,EmbedTypes.STATS,None,level) 
                select = interactions.SelectMenu(
                    options=[
                        interactions.SelectOption(
                        label="1",
                        value=f"0{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="2",
                        value=f"1{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="3",
                        value=f"2{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="4",
                        value=f"3{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="5",
                        value=f"4{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="6",
                        value=f"5{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="7",
                        value=f"6{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="8",
                        value=f"7{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="9",
                        value=f"8{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="10",
                        value=f"9{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="11",
                        value=f"10{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="12",
                        value=f"11{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="13",
                        value=f"12{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="14",
                        value=f"13{ctx.id}"
                        ),
                        interactions.SelectOption(
                        label="15",
                        value=f"14{ctx.id}"
                        )
                    ],
                    placeholder="Select a level",
                    min_values=1,
                    max_values=1,
                    custom_id="stat_menu"
                )
                action_row = interactions.ActionRow.new(select)

                await ctx.send(embeds = e, components=action_row)

                button_ctx: interactions.ComponentContext = await client.wait_for_component(components=action_row, check=NewStat, timeout=60)     
                return            
    except asyncio.TimeoutError:
        # When it times out, edit the original message and remove the button(s)
        return await ctx.edit(components=[])

    suggestions = ""
    spellingCorrection = data.nameCorrection(name.lower())
    
    if(spellingCorrection != name.lower() and spellingCorrection != ""):
        suggestions = "Attempted Spelling Correction: `" + spellingCorrection + "`\n"

    e = interactions.Embed()
    e.title= "Woops!"
    e.description = f"Looks like we cannot find {name}. {suggestions}"
    e.color = interactions.Color.red()
    await ctx.send(embeds = e)

@client.autocomplete(command="stats",name="name")
async def autocomplete_stats(ctx, user_input: str = ""):
    try:
        choices = [
        interactions.Choice(name=item, value=item) for item in data.autocompleteNames if user_input.lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.populate(choices)
    except:
        pass

@client.command(name="moves",
            description="Get moves of the Pokemon!",
            options=[
            interactions.Option(
                name="name",
                description="Name of the Pokemon",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            ),
            interactions.Option(
                name="move_tier",
                description="What tiers of moves do you want to see?",
                type=interactions.OptionType.STRING,
                required = True,
                choices=[
                    interactions.Choice(
                    name="All Moves",
                    value="all"
                    ),
                    interactions.Choice(
                    name="Default",
                    value="default"
                    ),
                    interactions.Choice(
                    name="Moves 1 / 2",
                    value="stage1"
                    ),
                    interactions.Choice(
                    name="Move 1 Upgrades",
                    value="stage2"
                    ),
                    interactions.Choice(
                    name="Move 2 Upgrades",
                    value="stage3"
                    ),
                    interactions.Choice(
                    name="Unite",
                    value="unite"
                    )
                ]
            )
        ])
async def MovesGrabber(ctx,name,move_tier):
    await ctx.defer()
    try:
        async def MoveChange(select_ctx):
            try:
                if(select_ctx.author == ctx.author):
                    moveset = select_ctx.data.values[0].replace(str(ctx.id),"")
                    e = BuildEmbed(val,EmbedTypes.MOVES,moveset,None)
                    await select_ctx.edit(embeds = e)          
                else:                    
                    try:                                                    
                        await select_ctx.author.send(Consts.ONLY_REQUESTOR_CAN_TOGGLE)
                    except:
                        pass
            except Exception as error: 
                e = interactions.Embed()
                e.title= val['name']
                e.set_thumbnail(url=val['imageLink'])
                e.set_footer(icon_url="https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/unite-db-icon.png",text="Powered by unite-db")
                e.description = "Looks like the info you are looking for doesn't fit into a Discord Embed! (Max 1024 Characters). You can check out the information on [Unite-DB](https://unite-db.com/pokemon/"+val['name']+")!"
                e.color = interactions.Color.blurple()  
                await ctx.send(embeds = e)  
                return  

        for val in data.pokemon:
            if name.lower() == val['name'].lower():
                e = BuildEmbed(val,EmbedTypes.MOVES,move_tier,None)  
                select = interactions.SelectMenu(
                    options=[
                            interactions.SelectOption(
                            label="All Moves",
                            value=f"all{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Default",
                            value=f"default{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Moves 1 / 2",
                            value=f"stage1{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Move 1 Upgrades",
                            value=f"stage2{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Move 2 Upgrades",
                            value=f"stage3{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Unite",
                            value=f"unite{ctx.id}"
                            )
                    ],
                    placeholder="Choose the moveset",
                    min_values=1,
                    max_values=1,
                    custom_id="moves_menu"
                )
                action_row = interactions.ActionRow.new(select)

                await ctx.send(embeds = e, components=action_row)
               
                try:
                    select_ctx: interactions.ComponentContext = await client.wait_for_component(components=action_row, check=MoveChange, timeout=60)                   
                except asyncio.TimeoutError:
                    pass
                    # When it times out, edit the original message and remove the button(s)
                    # return await ctx.edit(components=[])                         
                return     
    except Exception as error:
        for val in data.pokemon:
            if name.lower() == val['name'].lower():
                e = interactions.Embed()
                e.title= val['name']
                e.set_thumbnail(url=val['imageLink'])
                e.set_footer(icon_url="https://pkmn-tcg-api-images.sfo2.cdn.digitaloceanspaces.com/%21Logos/unite-db-icon.png",text="Powered by unite-db")
                e.description = "Looks like the info you are looking for doesn't fit into a Discord Embed! (Max 1024 Characters). You can check out the information on [Unite-DB](https://unite-db.com/pokemon/"+val['name']+")!"
                e.color = interactions.Color.blurple()
                await ctx.send(embeds = e)
                return

    suggestions = ""
    spellingCorrection = data.nameCorrection(name.lower())
    
    if(spellingCorrection != name.lower() and spellingCorrection != ""):
        suggestions = "Attempted Spelling Correction: `" + spellingCorrection + "`\n"

    e = interactions.Embed()
    e.title= "Woops!"
    e.description = f"Looks like we cannot find {name}. {suggestions}"
    e.color = interactions.Color.red()
    await ctx.send(embeds = e)

@client.autocomplete(command="moves",name="name")
async def autocomplete_moves(ctx, user_input: str = ""):
    try:
        choices = [
        interactions.Choice(name=item, value=item) for item in data.autocompleteNames if user_input.lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.populate(choices)
    except:
        pass

@client.command(name="medals",
            description="Show what each medal means")
async def MedalList(ctx):
    await ctx.defer()
    e = interactions.Embed()
    e.title = "Medals"
    genericMedals = "<:assist:885929525832196147> - Had the most assists\n<:bestscore:885929525865762877> - Scored the most goals\n<:healer:885929525886738432> - Healed most damage\n<:injury:885929525878353920> - Most damaged recieved\n<:ko:885929525937057832> - Most Knock Outs\n<:scoreinterrupt:885929525702189077> - Interrupted most goals"
    silverMvp = "<:betterbalance:885929525899313262> - All-Rounder\n<:betterattack:885929525844770886> - Attacker\n<:betterdefense:885929525865767014> - Defender\n<:betteragility:885929525874147368> - Speedster\n<:bettersupport:885929525874147418> - Supporter"
    goldMvp = "<:bestbalance:885929525857374278> - All-Rounder\n<:bestattack:885929525895127100> - Attacker\n<:bestdefense:885929525807050802> - Defender\n<:bestagility:885929525811216384> - Speedster\n<:bestsupport:885929525794463784> - Supporter"
    e.add_field(name="Generic",value=genericMedals,inline=False)
    e.add_field(name="Silver MVP (70+ Points)",value=silverMvp,inline=False)
    e.add_field(name="Gold MVP (80+ Points)",value=goldMvp,inline=False)
    
    await ctx.send(embeds = e)


@client.command(name="attack_math",
            description="Displays the attack formulas for a specific Pokemon",
            options=[
            interactions.Option(
                name="name",
                description="Name of the Pokemon",
                type=interactions.OptionType.STRING,
                required=True,
                autocomplete=True
            ),
            interactions.Option(
                name="move_tier",
                description="What tiers of moves do you want to see?",
                type=interactions.OptionType.STRING,
                required = True,
                choices=[
                    interactions.Choice(
                    name="All Moves",
                    value="all"
                    ),
                    interactions.Choice(
                    name="Default",
                    value="default"
                    ),
                    interactions.Choice(
                    name="Moves 1 / 2",
                    value="stage1"
                    ),
                    interactions.Choice(
                    name="Move 1 Upgrades",
                    value="stage2"
                    ),
                    interactions.Choice(
                    name="Move 2 Upgrades",
                    value="stage3"
                    ),
                    interactions.Choice(
                    name="Unite",
                    value="unite"
                    )
                ]
            )
        ])
async def AttackFormulas(ctx,name,move_tier):
    await ctx.defer()
    try:
        async def NewAttackFormula(button_ctx: interactions.ComponentContext):
            try:
                if(button_ctx.author == ctx.author):
                    moveset = button_ctx.data.values[0].replace(str(ctx.id),"")
                    e = BuildEmbed(val,EmbedTypes.ATTACK_FORMULAS,moveset,None)
                    await button_ctx.edit(embeds = e)          
                else:                    
                    try:                                                    
                        await button_ctx.author.send(Consts.ONLY_REQUESTOR_CAN_TOGGLE)
                    except:
                        pass
            except Exception as e:
                    print(e) 

        for val in data.pokemon:
            if name.lower() == val['name'].lower():
                e = BuildEmbed(val,EmbedTypes.ATTACK_FORMULAS,move_tier,None)  
                select = interactions.SelectMenu(
                    options=[
                            interactions.SelectOption(
                            label="All Moves",
                            value=f"all{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Default",
                            value=f"default{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Moves 1 / 2",
                            value=f"stage1{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Move 1 Upgrades",
                            value=f"stage2{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Move 2 Upgrades",
                            value=f"stage3{ctx.id}"
                            ),
                            interactions.SelectOption(
                            label="Unite",
                            value=f"unite{ctx.id}"
                            )
                    ],
                    placeholder="Choose the moveset",
                    min_values=1,
                    max_values=1,
                    custom_id="attack_menu"
                )
                action_row = interactions.ActionRow.new(select)

                await ctx.send(embeds = e, components=action_row)

                try:
                    button_ctx: interactions.ComponentContext = await client.wait_for_component(components=action_row, check=NewAttackFormula, timeout=60)                   
                except asyncio.TimeoutError:
                    pass
                    # When it times out, edit the original message and remove the button(s)
                    # return await ctx.edit(components=[])    
                return        
        
    except Exception as error:
        print(error)
    
    
    suggestions = ""
    spellingCorrection = data.nameCorrection(name.lower())
    
    if(spellingCorrection != name.lower() and spellingCorrection != ""):
        suggestions = "Attempted Spelling Correction: `" + spellingCorrection + "`\n"

    e = interactions.Embed()
    e.title= "Woops!"
    e.description = f"Looks like we cannot find {name}. {suggestions}"
    e.color = interactions.Color.red()
    await ctx.send(embeds = e)


@client.autocomplete(command="attack_math",name="name")
async def autocomplete_attackFormulas(ctx, user_input: str = ""):
    try:
        choices = [
        interactions.Choice(name=item, value=item) for item in data.autocompleteNames if user_input.lower() in item.lower()
    ] 

        if(len(choices) > 25):
            choices = choices[0:25]

        await ctx.populate(choices)
    except:
        pass

@create_task(IntervalTrigger(500))
async def ListServers():
    if(Consts.TOPGG_AUTHTOKEN is not None):
        async with aiohttp.ClientSession() as session:
            headers = {
                    'Content-Type': "application/json",
                    'Authorization': f"Bearer {Consts.TOPGG_AUTHTOKEN}",
                    'Accept': "*/*",
                    'Host': "top.gg",
                    }
            servercount = len(client.guilds)
            async with session.post(url="https://top.gg/api/bots/867595735380918272/stats", json={'server_count': servercount}, headers=headers) as response:            
                print("List Server POST Status:", response.status)
                


ListServers.start()
client.start()