# Discord Translator Bot

This repository contains the source code for TransBot, a real-time message translation bot for Discord. TransBot is an abbreviation for "Translator Bot".

## Overview

This project is implemented using the Pycord library. This README provides detailed instructions on how to configure and deploy the bot on your local machine.

## Prerequisites

Before proceeding with the setup, ensure that the following requirements are met:

- A Discord bot
- Python programming language
- Py-cord library

## Bot Configuration

1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications), sign in, and select the "New Application" button.
   
   ![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/6efc3a3a-6610-40e4-a309-9b63cbdfb9f2)


2. Enter the desired bot name and accept the Terms of Service.
   
   ![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/0c739128-a584-410c-9f27-a16008d7a156)


3. Provide a description and tags for the bot, then select "Save Changes".
   
   ![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/b5687685-9fa9-456d-9561-204c0a8bfd9d)


4. Navigate to the "Bot" tab and create a new bot.
   
   ![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/e3ae443f-c6e0-48b9-9686-330cad0dd078)

5. Reset the bot token and store it in a secure location.
   
   ![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/5c2425e9-61e8-48c7-9abb-616f098d5f7a)
   
   ![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/f2ac7128-7c4e-478f-9edb-eb50c90aed0a)

## Repository Setup

1. Clone this repository using the command `git clone https://github.com/yakovexplorer/DiscordTranslateBot.git`.
2. Change the current working directory to the repository using `cd DiscordTranslateBot`.
3. Rename the file "env.example" to ".env" and open it for editing.
4. Add the values for "DISCORD_TOKEN", and "OPENAI_API_KEY" in the .env file, with your information, as shown below, and save the changes.
   - `DISCORD_TOKEN='YOUR DISCORD BOT TOKEN'`
   - `OPENAI_API_KEY='YOUR OPENAI API KEY'`

## Dependency Installation

1. Install Python by visiting the [Python Downloads](https://www.python.org/downloads/) page and following the provided instructions.
2. Open a command prompt or terminal window and enter `pip install py-cord` to install the Py-cord library.
3. Enter `pip install translatepy` to install the Translatepy library.
4. Enter `pip install python-dotenv` to install the Python-dotenv library.
5. Enter `pip install psutil` to install the Psutil library.
6. Enter `pip install aiofiles` to install the Aiofiles library.

## Bot Execution

1. Navigate to the DiscordTransBot directory on your local machine.
2. Execute the command `python3 DiscordBot.py` or `python DiscordBot.py` to start the bot.

## Bot Invitation

1. Return to the Discord Developer Portal and access your bot's OAuth2 page.
   
2. Use the URL generator tool to create an invitation link for your bot.
![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/97098c81-f07a-4b16-adae-b3e19b156ed9)
![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/b38b9fa5-35c6-459f-b1b6-5ad2c303cb93)

3. Copy the generated link and paste it into your web browser to invite your bot to your server.

## Screenshots

The following images showcase some of the features provided by this bot:

![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/654f4ea9-62ac-4f08-bb39-d3a56bb18caa)

![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/1a1b3423-5dda-4dd1-9f3d-188033365043)

![image](https://github.com/yakovexplorer/DiscordTransBot/assets/130591120/9a4b2a2f-2afa-49cc-9df6-a2c330e758cc)

## Licensing

The source code contained within this repository is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). We strongly recommend reviewing the licensing terms specified in this [file](https://github.com/yakovexplorer/DiscordTranslateBot/blob/main/LICENSE).
