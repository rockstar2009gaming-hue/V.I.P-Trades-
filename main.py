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
intents.message_content = True  # recommended

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
@app_commands.checks.has_role("Server Middleman")
async def mminfo(interaction: discord.Interaction):

    embed = discord.Embed(
        title="💎 Middleman System Explained",
        description=(
            "**A Middleman (MM)** is a trusted person who ensures safe trades.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**🔄 How MM Works:**\n"
            "1️⃣ Seller → MM\n"
            "2️⃣ Buyer pays seller\n"
            "3️⃣ MM verifies\n"
            "4️⃣ MM gives item\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**🛡️ Why use MM?**\n"
            "• Prevent scams\n"
            "• Safe trading\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "**⚠️ RULES:**\n"
            "• Only official MM\n"
            "• Verify identity\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Click below 👇"
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

# =========================
# START BOT + FLASK
# =========================
def start_bot():
    try:
        token = os.getenv("DISCORD_TOKEN")
        print("TOKEN:", token)

        if not token:
            print("❌ TOKEN NOT FOUND")
            return

        bot.run(token)

    except Exception as e:
        print("❌ BOT ERROR:", e)

# Run bot in background thread
Thread(target=start_bot).start()

# Run Flask in main thread
app.run(host='0.0.0.0', port=int(os.environ["PORT"]))