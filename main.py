import discord
import os
import random
import zipfile
import requests
import re
from io import BytesIO
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
from PIL import Image, ImageDraw, ImageFont



# Initialize the bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/",
                   intents=intents)  # Set your command prefix

# Create Flask app
app = Flask('')


@app.route('/')
def home():
    return "Bot is running!"


# Run Flask web server in a separate thread
def run():
    app.run(host="0.0.0.0", port=80)


# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        # Sync commands with Discord
        await bot.tree.sync()  # Sync commands with Discord
        print("Slash commands synced successfully!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


# Slash command for killer builds
@bot.tree.command(name="killer", description="Get killer build images")
async def killer(interaction: discord.Interaction, names: str):
    killer_builds = {
        "trapper": [
            "https://files.catbox.moe/fcu22n.png",
            "https://files.catbox.moe/7fo699.png",
            "https://files.catbox.moe/ubeeym.png",
            "https://files.catbox.moe/v8x62s.png"
        ],
        "nurse": [
            "https://files.catbox.moe/dlk0s4.png",
            "https://files.catbox.moe/uwf8a5.png",
            "https://files.catbox.moe/u60q08.png",
            "https://files.catbox.moe/v4ns5t.png"
        ],
        "executioner": ["https://files.catbox.moe/jhlwch.png"],
        "chucky": ["https://files.catbox.moe/dalgas.png"],
        "dracula": ["https://files.catbox.moe/alexqv.png"],
        "huntress": ["https://files.catbox.moe/1nymef.png"],
        "doctor": ["https://files.catbox.moe/uoq8yc.png"],
        "nightmare": ["https://files.catbox.moe/pfttvq.png"],
        "legion": ["https://files.catbox.moe/l4eygh.png"],
        "ghostface": ["https://files.catbox.moe/6z2ntb.png"],
        "oni": ["https://files.catbox.moe/9dw0vl.png"],
        "trickster": ["https://files.catbox.moe/r1pqvq.png"],
        "onryo": ["https://files.catbox.moe/22cr9f.png"],
        "unknown": ["https://files.catbox.moe/74sj3w.png"],
    }

    names = names.lower()  # Ensure name is lowercase
    if names in killer_builds:
        embeds = []
        icon_url = "https://files.catbox.moe/mqboky.png"
        for url in killer_builds[names]:
            embed = discord.Embed(
                title=f"{names.capitalize()} Build",
                description="Here are the images for the build:",
                color=discord.Color.red())
            embed.set_thumbnail(url=icon_url)
            embed.set_image(url=url)  # Add the image to the embed
            embeds.append(embed)

        # Send the embeds
        await interaction.response.send_message(embeds=embeds, ephemeral=True)
    else:
        await interaction.response.send_message(
            "Killer not found. Please try again with a valid killer name (e.g., 'trapper', 'nurse').",
            ephemeral=True)


# Slash command for survivor builds
@bot.tree.command(name="sur", description="Get survivor build images")
async def survivor(interaction: discord.Interaction, build: str):
    survivor_builds = {
        "genrush": [
            "https://files.catbox.moe/c67tbu.png",
            "https://files.catbox.moe/mwljzd.png",
            "https://files.catbox.moe/7uixtl.png"
        ],
        "team": ["https://files.catbox.moe/jpu6e8.png"],
        "speed": [
            "https://files.catbox.moe/son4s6.png",
            "https://files.catbox.moe/v89igx.png"
        ],
        "boonbuild": ["https://files.catbox.moe/fwbq3r.png"],
        "flashlight": [],
        "solo": ["https://files.catbox.moe/ei0pvy.png"],
    }

    build = build.lower()
    if build in survivor_builds:
        embeds = []

        icon_url = "https://files.catbox.moe/mqboky.png"

        for i, url in enumerate(survivor_builds[build]):

            embed = discord.Embed(title=f"{build.capitalize()} Build",
                                  description="BuildBringer:",
                                  color=discord.Color.blue())
            embed.set_image(url=url)
            embed.set_thumbnail(url=icon_url)
            embeds.append(embed)

    # Send the embeds
        for i in range(0, len(embeds), 10):
            await interaction.response.send_message(embeds=embeds[i:i + 10],
                                                    ephemeral=True)
    else:
        await interaction.response.send_message(
            "Survivor not found. Please try again with a valid survivor name (e.g., 'meg', 'claudette').",
            ephemeral=True)

    # Example hard-coded zip URL (replace this with your zip file link)


# Download and extract images from a zip file, returning images and their original names
def get_images_from_zip(zip_url):
    try:
        response = requests.get(zip_url)
        zip_file = BytesIO(response.content)

        images = []
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for name in zip_ref.namelist():
                if name.endswith(('.png', '.jpg', '.jpeg')):
                    img = Image.open(BytesIO(
                        zip_ref.read(name))).convert("RGBA")
                    images.append((img, name))
        return images
    except zipfile.BadZipFile:
        print("Error: The provided file is not a valid zip file.")
        return None


def download_and_extract_font(zip_url, font_filename, extract_path='./fonts'):
    # Create the directory to extract the font to, if it doesn't exist
    os.makedirs(extract_path, exist_ok=True)

    try:
        # Download the zip file from the URL
        response = requests.get(zip_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Open the zip file from the downloaded content
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            # Check if the font file exists inside the zip
            if font_filename not in zip_file.namelist():
                print(f"Error: The font file '{font_filename}' was not found in the zip.")
                return None

            # Extract the font file to the specified path
            zip_file.extract(font_filename, path=extract_path)

            # Return the path to the extracted font file
            font_path = os.path.join(extract_path, font_filename)
            print(f"Font extracted to: {font_path}")
            return font_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the font zip file: {e}")
        return None
    except zipfile.BadZipFile:
        print("Error: The provided file is not a valid zip file.")
        return None

# Example usage
FONT_ZIP_URL = 'https://files.catbox.moe/4md411.zip'  # Replace with your font zip URL
FONT_FILENAME = 'custom_font.ttf'  # Replace with your font filename in the zip

font_path = download_and_extract_font(FONT_ZIP_URL, FONT_FILENAME)

if font_path:
    print(f"Font file path: {font_path}")
else:
    print("Failed to download and extract the font.")
def clean_image_name(name):
    name_without_extension = os.path.splitext(name)[0]
    clean_name = re.sub(r'\d+', '', name_without_extension)
    clean_name = clean_name.replace('_', '').replace('Portrait', '').replace(
        'K', '').replace('T_iconPerks', '').replace('iconPerks',
                                                    '').replace('new',
                                                                '').title()
    return clean_name.strip()

def create_killer_perk_layout(killer_image, killer_name, perk_images, font_file):
    layout_width = 650
    layout_height = 750
    killer_image_size = 220
    perk_image_size = 130
    killer_font_size = 60
    perk_font_size = 30

    # Load font
    try:
        killer_font = ImageFont.truetype(font_file, killer_font_size)
        perk_font = ImageFont.truetype(font_file, perk_font_size)
    except OSError:
        killer_font = ImageFont.load_default()
        perk_font = ImageFont.load_default()

    # Create layout canvas
    layout = Image.new("RGB", (layout_width, layout_height), (0, 0, 0))
    draw = ImageDraw.Draw(layout)

    # Resize and position killer image and name
    killer_image_resized = killer_image.resize((killer_image_size, killer_image_size))
    layout.paste(killer_image_resized, (layout_width // 2 - killer_image_size // 2, 20))
    draw.text(
        (layout_width // 2, killer_image_size + 30),
        killer_name.upper(),
        font=killer_font,
        fill=(255, 255, 255),
        anchor="mm",
    )

    # Position perks in a 2x2 grid (below the killer image)
    start_x = layout_width // 4 - perk_image_size // 2
    start_y = killer_image_size + 80
    for i, (perk_image, perk_name) in enumerate(perk_images):
        x = start_x + (i % 2) * (layout_width // 2)
        y = start_y + (i // 2) * (perk_image_size + 90)

        perk_image_resized = perk_image.resize((perk_image_size, perk_image_size))
        layout.paste(perk_image_resized, (x, y))

        draw.text(
            (x + perk_image_size // 2, y + perk_image_size + 20),
            perk_name.capitalize(),
            font=perk_font,
            fill=(255, 255, 255),
            anchor="mm",
        )

    # Save the layout to a buffer and return it
    output_buffer = BytesIO()
    layout.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return output_buffer

def get_random_killer(killer_images):
    if not killer_images:
        return None, None
    killer_image, killer_name = random.choice(killer_images)
    return killer_image, clean_image_name(killer_name)


@bot.tree.command(name="rk", description="Random Killer and Perk layout.")
async def random_images(interaction: discord.Interaction):
    # Defer the interaction response to prevent timeout
    await interaction.response.defer(ephemeral=True)

    # Debug: Ensure that the interaction is being received
    print(f"Command triggered by: {interaction.user.name}")

    # Define the URL for the zip containing the images and the font
    killer_zip_url = 'https://files.catbox.moe/nljc6n.zip'  # Replace with actual URL
    perk_zip_url = 'https://files.catbox.moe/106i49.zip'  # Replace with actual URL
    font_zip_url = 'https://files.catbox.moe/4md411.zip'  # Replace with URL to the font zip file
    font_filename = 'custom_font.ttf'  # Replace with actual font filename in the zip

    # Fetch killer and perk images
    killer_images = get_images_from_zip(killer_zip_url)
    perk_images = get_images_from_zip(perk_zip_url)

    if not killer_images or not perk_images:
        await interaction.followup.send(
            "Error: Could not retrieve images from the provided zip files.",
            ephemeral=True)  # Message will only be visible to the user
        return

    # Extract the font from the font zip file
    font_file = download_and_extract_font(font_zip_url, font_filename)
    if not font_file:
        await interaction.followup.send(
            "Error: Could not find the font in the zip file.",
            ephemeral=True)  # Message will only be visible to the user
        return

    # Randomly select one killer and four perks
    selected_killer = random.choice(killer_images)
    selected_perks = random.sample(perk_images, 4)

    # Prepare image and names
    killer_image, killer_name = selected_killer[0], clean_image_name(selected_killer[1])
    perk_images = [(img, clean_image_name(name)) for img, name in selected_perks]

    # Debug: Ensure that the image and perk names are being selected correctly
    print(f"Selected Killer: {killer_name}")
    print(f"Selected Perks: {[perk[1] for perk in perk_images]}")

    # Create the layout
    image_grid = create_killer_perk_layout(killer_image, killer_name, perk_images, font_file)

    await interaction.followup.send(
           file=discord.File(image_grid, filename="layout.png"),
           ephemeral=True)

# Run the bot with your token
def start_bot():
    bot.run(
        "discordbottoken"
    )


# Start Flask and Bot in separate threads
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()  # Start Flask server
    start_bot()  # Start the Discord bot
