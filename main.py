from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
from discord import app_commands
import os

# =========================
# BOT SETUP
# =========================
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# BOT READY
# =========================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# =========================
# BUTTON SYSTEM
# =========================
class MMView(discord.ui.View):

    @discord.ui.button(label="Understand", style=discord.ButtonStyle.green)
    async def understand(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Good 👍", ephemeral=True)

    @discord.ui.button(label="Confused", style=discord.ButtonStyle.red)
    async def confused(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Read rules again!", ephemeral=True)

# =========================
# MM COMMAND
# =========================
@bot.tree.command(name="mminfo", description="Detailed middleman info")
@app_commands.checks.has_role("Server Middleman")  # change role name if needed
async def mminfo(interaction: discord.Interaction):

    embed = discord.Embed(
        title="💎 Middleman System Explained",
        description=(
            "**A Middleman (MM)** is a trusted person who ensures safe trades between buyer and seller.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**🔄 How MM Works:**\n"
            "1️⃣ Seller gives item to MM\n"
            "2️⃣ Buyer sends payment to seller\n"
            "3️⃣ MM verifies payment\n"
            "4️⃣ MM gives item to buyer\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**🛡️ Why use MM?**\n"
            "• Prevents scams\n"
            "• Safe & secure trading\n"
            "• Trusted process\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**⚠️ IMPORTANT RULES:**\n"
            "• Only use official server MMs\n"
            "• Do NOT trust random users\n"
            "• Always confirm MM identity\n"
            "• Screenshare if needed\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**💰 Supported Trades:**\n"
            "• Robux / Accounts\n"
            "• Game items\n"
            "• Real money deals\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Click below to confirm 👇"
        ),
        color=discord.Color.purple()
    )

    embed.set_image(url="https://cdn.discordapp.com/attachments/1482442530753871873/1487852412151529683/ChatGPT_Image_Mar_29_2026_10_03_27_PM.png")
    embed.set_footer(text="V.I.P Trades • Safe Trading")

    await interaction.response.send_message(embed=embed, view=MMView())

# =========================
# PING COMMAND
# =========================
@bot.tree.command(name="ping", description="Check bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")

# =========================
# BAN COMMAND
# =========================
@bot.tree.command(name="ban", description="Ban a user")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(user="User to ban")
async def ban(interaction: discord.Interaction, user: discord.Member):

    await user.ban()
    await interaction.response.send_message(f"{user} banned 🔨")

# =========================
# FLASK SERVER (RENDER)
# =========================
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=3000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# =========================
# START BOT
# =========================
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))