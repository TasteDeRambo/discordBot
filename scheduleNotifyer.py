import discord
from discord.ext import tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Your schedule
schedule = {
    "Monday": [
        {"class": "State and Local Government", "start": "08:00 AM", "end": "08:50 AM", "location": "Room 113, 215 Lamar St"},
        {"class": "FUNCTNS TRIG & LNR STM", "start": "11:30 AM", "end": "12:20 PM", "location": "Room 107, 466 Nagle St"},
        {"class": "HISTORY OF THE U S", "start": "12:40 PM", "end": "01:30 PM", "location": "Room M207, 423 Spence St"}
    ],
    "Tuesday": [
        {"class": "FUNCTNS TRIG & LNR STM", "start": "09:35 AM", "end": "10:25 AM", "location": "Room 104, 155 Ireland St"},
        {"class": "ENGR LAB I COMPUTATION", "start": "12:10 PM", "end": "02:00 PM", "location": "Room 340, 125 Spence St"}
    ],
    "Wednesday": [
        {"class": "State and Local Government", "start": "08:00 AM", "end": "08:50 AM", "location": "Room 113, 215 Lamar St"},
        {"class": "FUNCTNS TRIG & LNR STM", "start": "11:30 AM", "end": "12:20 PM", "location": "Room 107, 466 Nagle St"},
        {"class": "HISTORY OF THE U S", "start": "12:40 PM", "end": "01:30 PM", "location": "Room M207, 423 Spence St"}
    ],
    "Thursday": [
        {"class": "FUNCTNS TRIG & LNR STM", "start": "09:35 AM", "end": "10:25 AM", "location": "Room 104, 155 Ireland St"},
        {"class": "ENGR LAB I COMPUTATION", "start": "12:10 PM", "end": "02:00 PM", "location": "Room 340, 125 Spence St"}
    ],
    "Friday": [
        {"class": "State and Local Government", "start": "08:00 AM", "end": "08:50 AM", "location": "Room 113, 215 Lamar St"},
        {"class": "ENGR REGENTS SEMINAR", "start": "10:20 AM", "end": "11:10 AM", "location": "Room 160, 125 Spence St"},
        {"class": "FUNCTNS TRIG & LNR STM", "start": "11:30 AM", "end": "12:20 PM", "location": "Room 107, 466 Nagle St"},
        {"class": "HISTORY OF THE U S", "start": "12:40 PM", "end": "01:30 PM", "location": "Room M207, 423 Spence St"}
    ],
    "Saturday": [
        {"class": "Test message", "start": "5:30 PM", "end": "6:00 PM", "location": "G11, Walton Hall"}
    ]
}

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = discord.Client(intents=intents)
last_message = None

@tasks.loop(minutes=1)
async def check_schedule():
    global last_message
    now = datetime.now()
    day = now.strftime("%A")
    current_time = now.strftime("%I:%M %p")

    if day in schedule:
        for i, cls in enumerate(schedule[day]):
            if cls["end"] == current_time:
                if i + 1 < len(schedule[day]):
                    next_class = schedule[day][i + 1]
                    user = await client.fetch_user(478794727232241664)
                    if last_message:
                        await last_message.delete()
                    last_message = await user.send(f"Your next class is {next_class['class']} at {next_class['start']} in {next_class['location']}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    check_schedule.start()

client.run(TOKEN)
