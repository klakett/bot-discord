import discord
from discord.ext import commands
from discord.utils import get 

bot = commands.Bot(command_prefix = "?", description = "bot de klakette test") #command_prefix pour definir le prefix du bot (comment l'appeler, ex: mee6 c'est !)

#event qui dit "ready !" dans la console lorsqu'il se lance
@bot.event
async def on_ready():
    print('ready !')

bot.remove_command('help')

@bot.command()
async def addrole(ctx, role : discord.Role, user = discord.Member):
    await user.add_roles(role)
    await ctx.send (f'{user.mention} à obtenue le role {role.mention}.')

#commande pour repondre a une commande "?coucou", await context.send("Coucou !") repond dans discord
@bot.command()
async def coucou(context):
    await context.send("Coucou !")

@bot.command()
async def serverinfo(context):
    server = context.guild #obtient les infos du serveur OBLIGATOIRE POUR LES COMMANDES QUI SUIVENT SINON PYTHON NE SAIT PAS OU CHERCHER LES INFORMATIONS ou ecrire les commandes avec context.guild au debut (context.guild.server.name)
    servername = server.name #obtenir nom du serveur
    numberoftextchannels = len(server.text_channels) #liste channels textuels du servers, len recupere seulement le nombre
    numberofvoicechannels =len(server.voice_channels) #liste channels vocaux du servers, len recupere seulement le nombre
    serverdescription = server.description #obtenir description serveur
    numberofperson = server.member_count #nombre de membre
    if (numberoftextchannels)<=1 and (numberofvoicechannels) >1: #si il ya 1 ou moins d'1 salon textuel mais qu'ils ya plus d'un salons vocals
        messageserverinfo = f"**{servername}** contient {numberofperson} utilisateurs, {numberoftextchannels} salon textuel et {numberofvoicechannels} salons vocaux. \nLa description du serveur {serverdescription}" 
    elif (numberofvoicechannels)<=1 and (numberoftextchannels) >1: #si il ya 1 ou moins d'1 salon vocal mais qu'ils ya plus d'un salons textuels
        messageserverinfo = f"**{servername}** contient {numberofperson} utilisateurs, {numberoftextchannels} salons textuels et {numberofvoicechannels} salon vocal. \nLa description du serveur {serverdescription}"
    elif (numberoftextchannels)and(numberofvoicechannels) <=1: #si il ya 1 ou moins d'1 salons textuels mais qu'ils ya 1 ou moins d'1 salons vocal
        messageserverinfo = f"**{servername}** contient {numberofperson} utilisateurs, {numberoftextchannels} salon textuel et {numberofvoicechannels} salon vocal. \nLa description du serveur {serverdescription}"
    else: #sinon (si il ya plus d'1 salons vocals et plus d'1 salons textuels)
        messageserverinfo = f"**{servername}** contient {numberofperson} utilisateurs, {numberoftextchannels} salons textuels et {numberofvoicechannels} salons vocaux. \nLa description du serveur {serverdescription}" #f permet d'integrer un variable dans chaine de caractère, \n permet un retour a la ligne
    await context.send(messageserverinfo) #envoyer le message sur discord
#**pour ecrire en gras**, *pour ecrire en italique*

@bot.command()
async def bonjour(context):
    server = context.guild
    servername = server.name
    await context.send(f"Bonjour jeune *padawan* ! Savais tu que tu te trouvais dans le serveur *{servername}*, c'est d'ailleurs un super \nserveur puisque **JE** suis dedans. ")

@bot.command()
async def say(ctx, *texte): #*sert a montrer l'on ne connait le nombre de caractere que l'argument aurat (espaces, etc...), donc impossible de mettre un autre argument apres
    await ctx.send (" ".join(texte)) #" ".join sert a mettre un espace entre chaque element de la liste (car python comprend l'argument texte comme une liste donc chaque mots sont separer par des guillemets), ca sert donc a faire un texte normal

@bot.command()
async def chinese(ctx, *text):
    chinesechar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
    chinesetext = []
    for word in text:
        for char in word:
            if char.isalpha(): #verifie si le caractere est une lettre
                index = ord(char) - ord('a') #ord obtient position asqui du caractere
                transformed = chinesechar [index]
                chinesetext.append(transformed)
            else:
                chinesetext.append(char)
        chinesetext.append(' ')
    await ctx.send ("".join(chinesetext))
    
#caractere alphabet facon chinois 丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙

@bot.command()
async def dit(ctx, chiffre, *texte):
    for _ in range (int(chiffre)):
        await ctx.send (" ".join(texte))

@bot.command()
async def getinfo (ctx, text):
    server = ctx.guild
    if text =="membercount":
        await ctx.send (f"{server.member_count}")
    elif text == "numberofchannel" :
        await ctx.send (f"{len(server.text_channels) + len(server.voice_channels)}")
    elif text == "name":
        await ctx.send (f"{server.name}")
    else :
        await ctx.send ('info disponible :\n"membercount", "numberofchannel", "name"')

@bot.command()
async def cuisiner (ctx):
    await ctx.send ("Envoyez le plat que vous voulez.")

    def checkmessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel

    recette = await bot.wait_for("message", timeout = 10, check = checkmessage) #attendre pour un message, timeout = 10 veut dire au bout de 10 sec ça crash, check verifie que le message attendue vient du bon user
    message = await ctx.send (f'la préparation de {recette.content} va commencer, veuillez valider en réagissant avec ✅ ou ❌')
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkemoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji)) == "✅" or (str(reaction.emoji)) =="❌"

    reaction, user = await bot.wait_for('reaction_add', timeout = 10, check = checkemoji )
    if reaction.emoji == "✅":
        await ctx.send ("La recette à démarré.")
    else:
        await ctx.send ('La recette a bien été annulée.')

@bot.command()
async def aide(ctx):
    await ctx.send ('Commandes :\n?addrole (role) (user)\n?coucou\n?serverinfo\n?bonjour\n?dit (nombres de fois) (texte)\n?getinfo (texte) ')
    



#ADMINISTRATION ---------------------

@bot.command()
async def clear (ctx, number:int): #int montre que c'est un chiffre
    message = await ctx.channel.history(limit = number + 1).flatten() #recupere l'historique des message, flatten veut dire que c'est une liste
    for message in message:
        await message.delete()
    if number <=1 : 
        print ('--',number,' message à été clear.')
    else:
        print ('--',number,' messages ont été clear.')

@bot.command()
async def kick (ctx, user : discord.User, *raison): #user : discord.user montre que l'on parle d'un user 
    raison = " ".join(raison)
    await ctx.guild.kick(user, reason = raison)
    await ctx.send (f'{user} à été kick. Raison : " {raison}"')
    print ('--',user,'à été kick du serveur. Raison :',raison)

@bot.command()
async def ban (ctx, user : discord.User, *raison):
    raison = " ".join(raison)
    await ctx.guild.ban(user, reason = raison)
    await ctx.send (f'{user} à été ban. Raison : " {raison} "')
    print ('--',user, 'à été ban. Raison : ',raison)

@bot.command()
async def unban (ctx, user, *raison):
    raison = " ".join(raison)
    username, userid = user.split("#")
    bannedusers = await ctx.guild.bans()
    for x in bannedusers:
        if x.user.name == username and x.user.discriminator == userid:
            await ctx.guild.unban(x.user, reason = raison)
            await ctx.send (f'{user} à été unban. Raison " {raison} "')
            return
            print ('--',user,'à été deban. Raison : ',raison)
    await ctx.send (f"L'utilisateur {user} n'est pas dans la liste des ban.")


bot.run("ODcyNDYwNjU2MzYyNzkwOTgz.YQqMTg.BXt7g9QbekO8ESgNpd6RaXw7VGQ") #lancer le bot (avec le token du bot)