import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import os
import datetime
import random
import subprocess
import threading
import requests
from bs4 import BeautifulSoup
import winreg
import wikipedia
import pyautogui
import wolframalpha
import json
import smtplib
from email.message import EmailMessage
import screen_brightness_control as sbc
import psutil
import pyjokes
import sys
import re

class SafiaAssistant:
    def __init__(self):
        self.name = "Safia"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = self.init_engine()
        self.last_command_time = time.time()
        self.chrome_path = self.get_chrome_path()
        self.default_profile = "Profile 4"
        self.conversation_context = None
        self.command_history = []
        self.user_name = None
        self.wolfram_client = wolframalpha.Client('YOUR_WOLFRAMALPHA_APP_ID')
        self.email_config = self.load_email_config()
        
        self.commands = {
            'greetings': ['hello', 'hi', 'hey safia', 'hey'],
            'name': ["what is your name", "what's your name", "tell me your name"],
            'time': ['what time is it', 'current time', 'time now'],
            'date': ["today's date", "what day is it", "current date", "what is tomorrow's date"],
            'search': ['search for', 'look up', 'google', 'find', 'what is', 'who is'],
            'music': ['play song', 'play music', 'spotify', 'play'],
            'open': ['open mail', 'open chrome', 'open browser', 'open spotify'],
            'news': ['news', 'headlines', 'current affairs', 'latest news'],
            'apps': {
                'mail': ['https://mail.google.com', 'Opening your mailbox'],
                'chrome': [None, 'Opening Chrome browser'],
                'youtube': ['https://youtube.com', 'Opening YouTube'],
                'whatsapp': ['https://web.whatsapp.com', 'Opening WhatsApp Web'],
                'spotify': ['spotify', 'Opening Spotify'],
                'instagram': ['https://instagram.com', 'Opening Instagram'],
                'twitter': ['https://twitter.com', 'Opening Twitter'],
                'facebook': ['https://facebook.com', 'Opening Facebook'],
                'netflix': ['https://netflix.com', 'Opening Netflix'],
                'amazon': ['https://amazon.com', 'Opening Amazon'],
                'flipkart': ['https://flipkart.com', 'Opening Flipkart'],
                'swiggy': ['https://swiggy.com', 'Opening Swiggy'],
                'prime': ['https://primevideo.com', 'Opening Amazon Prime'],
                'drive': ['https://drive.google.com', 'Opening Google Drive'],
                'maps': ['https://maps.google.com', 'Opening Google Maps'],
                'meet': ['https://meet.google.com', 'Opening Google Meet'],
                'classroom': ['https://classroom.google.com', 'Opening Google Classroom'],
                'translate': ['https://translate.google.com', 'Opening Google Translate'],
                'linkedin': ['https://linkedin.com', 'Opening LinkedIn'],
                'pdfdrive': ['https://pdfdrive.com', 'Opening PDF Drive']
            },
            'system': ['brightness', 'volume', 'battery', 'system info', 'shutdown', 'restart'],
            'games': ['game', 'play game', 'rock paper scissors', 'toss coin'],
            'calculation': ['calculate', 'what is', 'plus', 'minus', 'multiply', 'divided by', 'times', '+', '-', '*', '/', '^'],
            'screenshot': ['take screenshot', 'capture screen'],
            'definition': ['definition of', 'what is the meaning of'],
            'weather': ['weather', 'weather report'],
            'joke': ['tell me a joke', 'make me laugh'],
            'email': ['send email', 'compose email'],
            'reminder': ['set reminder', 'remind me'],
            'exit': ['exit', 'goodbye', 'stop', 'shut down']
        }

    def get_chrome_path(self):
        try:
            paths = [
                os.getenv('PROGRAMFILES') + r'\Google\Chrome\Application\chrome.exe',
                os.getenv('LOCALAPPDATA') + r'\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    return path
            
            try:
                reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    path = winreg.QueryValue(key, None)
                    if os.path.exists(path):
                        return path
            except:
                pass
                
            if os.name == 'posix':
                if os.path.exists('/Applications/Google Chrome.app'):
                    return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                
            if os.path.exists('/usr/bin/google-chrome'):
                return '/usr/bin/google-chrome'
                
        except Exception as e:
            print(f"Chrome detection error: {e}")
        return None

    def open_in_chrome(self, url, profile=None):
        try:
            if not self.chrome_path:
                raise Exception("Chrome path not found")
                
            profile = profile or self.default_profile
            chrome_cmd = f'"{self.chrome_path}" {url} --profile-directory="{profile}" --new-window --start-maximized'
            
            if os.name == 'nt':
                os.system(f'start "" {chrome_cmd}')
                return True
            elif os.name == 'posix':
                subprocess.Popen(['open', '-a', 'Google Chrome', '--args', url])
                return True
            else:
                subprocess.Popen(chrome_cmd.split())
                return True
                
        except Exception as e:
            print(f"Chrome opening error: {e}")
            try:
                webbrowser.open(url)
                return False
            except Exception as fallback_error:
                print(f"Fallback browser error: {fallback_error}")
                return False

    def init_engine(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 170)
        return engine

    def speak(self, text, wait=False):
        print(f"{self.name}: {text}")
        self.engine.say(text)
        if wait:
            self.engine.runAndWait()
        else:
            threading.Thread(target=self.engine.runAndWait).start()
        
        self.command_history.append(('assistant', text))

    def listen(self):
        with self.microphone as source:
            print("\nListening...")
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You: {text}")
                self.last_command_time = time.time()
                self.command_history.append(('user', text))
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                self.speak("I'm having trouble with the speech service", wait=True)
                return None
            except Exception as e:
                print(f"Listening error: {e}")
                return None

    def load_email_config(self):
        try:
            with open('email_config.json') as f:
                return json.load(f)
        except:
            return None

    def handle_name_query(self, command):
        if any(phrase in command for phrase in self.commands['name']):
            if self.user_name:
                self.speak(f"My name is {self.name}. Your name is {self.user_name}.", wait=True)
            else:
                self.speak(f"My name is {self.name}. What should I call you?", wait=True)
                name = self.listen()
                if name:
                    self.user_name = name
                    self.speak(f"Nice to meet you, {self.user_name}!", wait=True)
            return True
        
        if "my name is" in command or "I am" in command:
            self.user_name = command.split("is")[-1].strip() if "is" in command else command.split("am")[-1].strip()
            self.speak(f"Okay, I'll remember that {self.user_name}", wait=True)
            return True
        
        return False

    def handle_system_commands(self, command):
        if 'brightness' in command:
            try:
                if 'increase' in command:
                    current = sbc.get_brightness()[0]
                    sbc.set_brightness(min(current + 20, 100))
                    self.speak("Increased brightness", wait=True)
                elif 'decrease' in command:
                    current = sbc.get_brightness()[0]
                    sbc.set_brightness(max(current - 20, 0))
                    self.speak("Decreased brightness", wait=True)
                elif 'set' in command:
                    try:
                        level = int(command.split()[-1])
                        sbc.set_brightness(level)
                        self.speak(f"Set brightness to {level}%", wait=True)
                    except:
                        self.speak("Please specify a brightness level between 0 and 100", wait=True)
                else:
                    current = sbc.get_brightness()[0]
                    self.speak(f"Current brightness is {current}%", wait=True)
                return True
            except:
                self.speak("Couldn't adjust brightness", wait=True)
                return True

        if 'battery' in command:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                status = "charging" if battery.power_plugged else "not charging"
                self.speak(f"Battery is at {percent}% and {status}", wait=True)
            else:
                self.speak("Couldn't get battery info", wait=True)
            return True

        if 'system info' in command:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            self.speak(f"CPU usage is {cpu}% and memory usage is {memory}%", wait=True)
            return True

        if 'shutdown' in command:
            self.speak("Shutting down the system in 10 seconds", wait=True)
            time.sleep(10)
            if os.name == 'nt':
                os.system('shutdown /s /t 1')
            else:
                os.system('shutdown now')
            return True

        if 'restart' in command:
            self.speak("Restarting the system in 10 seconds", wait=True)
            time.sleep(10)
            if os.name == 'nt':
                os.system('shutdown /r /t 1')
            else:
                os.system('reboot now')
            return True

        return False

    def handle_game(self, command):
        if "rock paper scissors" in command or "game" in command:
            moves = ["rock", "paper", "scissors"]
            self.speak("Choose rock, paper or scissors", wait=True)
            user_move = self.listen()
            comp_move = random.choice(moves)
            
            if user_move in moves:
                self.speak(f"I chose {comp_move}. You chose {user_move}.", wait=True)
                if user_move == comp_move:
                    self.speak("It's a tie!", wait=True)
                elif (user_move == "rock" and comp_move == "scissors") or \
                     (user_move == "paper" and comp_move == "rock") or \
                     (user_move == "scissors" and comp_move == "paper"):
                    self.speak("You win!", wait=True)
                else:
                    self.speak("I win!", wait=True)
            return True
        
        if "toss" in command or "flip" in command or "coin" in command:
            result = random.choice(["heads", "tails"])
            self.speak(f"It's {result}!", wait=True)
            return True
        
        return False

    def handle_calculation(self, command):
        try:
            # Basic arithmetic
            if '+' in command or 'plus' in command:
                nums = [float(s) for s in re.findall(r'\d+\.?\d*', command)]
                if len(nums) >= 2:
                    result = sum(nums)
                    self.speak(f"{' plus '.join(map(str, nums))} equals {result}", wait=True)
                    return True
            
            if '-' in command or 'minus' in command:
                nums = [float(s) for s in re.findall(r'\d+\.?\d*', command)]
                if len(nums) >= 2:
                    result = nums[0] - sum(nums[1:])
                    self.speak(f"{nums[0]} minus {' minus '.join(map(str, nums[1:]))} equals {result}", wait=True)
                    return True
            
            if '*' in command or 'times' in command or 'multiplied by' in command or 'multiply' in command:
                nums = [float(s) for s in re.findall(r'\d+\.?\d*', command)]
                if len(nums) >= 2:
                    result = 1
                    for num in nums:
                        result *= num
                    self.speak(f"{' times '.join(map(str, nums))} equals {result}", wait=True)
                    return True
            
            if '/' in command or 'divided by' in command:
                nums = [float(s) for s in re.findall(r'\d+\.?\d*', command)]
                if len(nums) >= 2:
                    try:
                        result = nums[0]
                        for num in nums[1:]:
                            result /= num
                        self.speak(f"{nums[0]} divided by {' divided by '.join(map(str, nums[1:]))} equals {result}", wait=True)
                        return True
                    except ZeroDivisionError:
                        self.speak("Cannot divide by zero", wait=True)
                        return True
            
            if '^' in command or 'power' in command:
                nums = [float(s) for s in re.findall(r'\d+\.?\d*', command)]
                if len(nums) >= 2:
                    result = nums[0] ** nums[1]
                    self.speak(f"{nums[0]} to the power of {nums[1]} equals {result}", wait=True)
                    return True
            
            # Wolfram Alpha for complex calculations
            if "calculate" in command or "what is" in command:
                question = command.replace("calculate", "").replace("what is", "").strip()
                res = self.wolfram_client.query(question)
                answer = next(res.results).text
                self.speak(f"The answer is {answer}", wait=True)
                return True
            
        except Exception as e:
            print(f"Calculation error: {e}")
            self.speak("I couldn't solve that calculation", wait=True)
        return False

    def handle_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            save_path = os.path.join(os.path.expanduser('~'), 'Pictures', 'Screenshots')
            os.makedirs(save_path, exist_ok=True)
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(os.path.join(save_path, filename))
            self.speak("Screenshot saved in your Pictures folder", wait=True)
            return True
        except Exception as e:
            print(f"Screenshot error: {e}")
            self.speak("Couldn't take screenshot", wait=True)
            return False

    def handle_definition(self, command):
        term = command.replace("definition of", "").replace("what is the meaning of", "").strip()
        try:
            definition = wikipedia.summary(term, sentences=1)
            self.speak(f"According to Wikipedia: {definition}", wait=True)
            return True
        except:
            self.speak(f"Couldn't find definition for {term}. Let me search online.", wait=True)
            self.open_in_chrome(f"https://google.com/search?q=define+{term}")
            return True

    def handle_weather(self):
        self.speak("Let me check the weather", wait=True)
        self.open_in_chrome("https://www.google.com/search?q=weather")
        return True

    def handle_joke(self):
        joke = pyjokes.get_joke()
        self.speak(joke, wait=True)
        return True

    def parse_email_address(self, spoken_text):
        """Convert spoken email address to proper format"""
        # Handle common email patterns
        spoken_text = spoken_text.lower().strip()
        
        # Replace common spoken patterns
        replacements = {
            ' at ': '@',
            ' dot ': '.',
            ' underscore ': '_',
            ' hyphen ': '-',
            ' dash ': '-',
            ' gmail ': 'gmail',
            ' outlook ': 'outlook',
            ' yahoo ': 'yahoo',
            ' hotmail ': 'hotmail'
        }
        
        for k, v in replacements.items():
            spoken_text = spoken_text.replace(k, v)
            
        # Remove spaces between characters
        spoken_text = spoken_text.replace(' ', '')
        
        # Validate email format
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', spoken_text):
            return spoken_text
        return None

    def handle_email(self, command):
        if not self.email_config:
            self.speak("Email configuration not set up. Please check email_config.json", wait=True)
            return True
            
        try:
            # Get recipient with improved parsing
            self.speak("Who should I send the email to? Please say the full address clearly.", wait=True)
            recipient = None
            attempts = 0
            
            while not recipient and attempts < 3:
                spoken_address = self.listen()
                if spoken_address:
                    recipient = self.parse_email_address(spoken_address)
                    if not recipient:
                        self.speak("I didn't get a valid email address. Please say it again like: user dot name at gmail dot com", wait=True)
                else:
                    self.speak("I didn't catch that. Please say the email address again.", wait=True)
                attempts += 1
                
            if not recipient:
                self.speak("Couldn't get valid email address. Cancelling email.", wait=True)
                return True
            
            # Get subject
            self.speak("What should be the subject?", wait=True)
            subject = None
            while not subject:
                subject = self.listen()
                if not subject:
                    self.speak("Please tell me the email subject.", wait=True)
            
            # Get body
            self.speak("What should I say in the email?", wait=True)
            body = None
            while not body:
                body = self.listen()
                if not body:
                    self.speak("Please tell me the email message.", wait=True)
            
            # Create and send email
            msg = EmailMessage()
            msg['From'] = self.email_config['email']
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.set_content(body)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.email_config['email'], self.email_config['password'])
                smtp.send_message(msg)
                
            self.speak(f"Email sent successfully to {recipient}", wait=True)
        except Exception as e:
            error_msg = str(e)
            print(f"Email error: {error_msg}")
            self.speak(f"Failed to send email. Error: {error_msg}", wait=True)
            
        return True

    def handle_reminder(self, command):
        self.speak("What should I remind you about?", wait=True)
        reminder_text = self.listen()
        
        self.speak("In how many minutes?", wait=True)
        minutes = self.listen()
        
        try:
            minutes = float(minutes)
            reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            with open('reminders.txt', 'a') as f:
                f.write(f"{reminder_time.isoformat()}|{reminder_text}\n")
                
            self.speak(f"I'll remind you about {reminder_text} in {minutes} minutes", wait=True)
        except:
            self.speak("Couldn't set reminder", wait=True)
            
        return True

    def check_reminders(self):
        try:
            with open('reminders.txt', 'r') as f:
                reminders = f.readlines()
                
            now = datetime.datetime.now()
            new_reminders = []
            notified = False
            
            for reminder in reminders:
                parts = reminder.strip().split('|')
                if len(parts) == 2:
                    time_str, text = parts
                    reminder_time = datetime.datetime.fromisoformat(time_str)
                    if reminder_time <= now:
                        self.speak(f"Reminder: {text}", wait=True)
                        notified = True
                    else:
                        new_reminders.append(reminder)
            
            if notified:
                with open('reminders.txt', 'w') as f:
                    f.writelines(new_reminders)
                    
        except:
            pass

    def handle_search(self, query):
        if not query:
            self.conversation_context = 'search'
            self.speak("What would you like me to search for?", wait=True)
            return True
            
        # Special cases
        if 'ipl' in query or 'cricket' in query:
            url = "https://www.google.com/search?q=today+ipl+match"
            self.speak("Showing today's IPL match details", wait=True)
            self.open_in_chrome(url)
            return True
            
        if 'gold price' in query:
            url = "https://www.google.com/search?q=today+gold+price"
            self.speak("Showing today's gold prices", wait=True)
            self.open_in_chrome(url)
            return True
            
        if any(word in query for word in self.commands['news']):
            if 'india' in query or 'indian' in query:
                url = "https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en"
                self.speak("Opening today's Indian news headlines", wait=True)
            else:
                url = "https://news.google.com"
                self.speak("Opening news headlines", wait=True)
            self.open_in_chrome(url)
            return True
            
        # General search
        search_terms = query.replace('search for', '').replace('look up', '').replace('google', '').strip()
        if not search_terms:
            search_terms = query
            
        url = f"https://www.google.com/search?q={search_terms.replace(' ', '+')}"
        success = self.open_in_chrome(url)
        if success:
            self.speak(f"Searching for {search_terms}", wait=True)
        else:
            self.speak(f"Searching for {search_terms}", wait=True)
        return True

    def play_music(self, query=None):
        try:
            if query and 'spotify' not in query.lower():
                url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
                self.open_in_chrome(url)
                self.speak(f"Playing {query} on Spotify", wait=True)
            else:
                if os.name == 'nt':
                    try:
                        os.system('start spotify:')
                        self.speak("Opening Spotify", wait=True)
                    except:
                        self.open_in_chrome("https://open.spotify.com")
                else:
                    self.open_in_chrome("https://open.spotify.com")
        except Exception as e:
            print(f"Spotify error: {e}")
            self.speak("Couldn't open Spotify right now", wait=True)

    def process_command(self, command):
        if not command:
            return False

        command = command.lower().strip()
        
        # Check reminders periodically
        if random.random() < 0.1:  # 10% chance to check reminders
            self.check_reminders()
        
        # Handle date queries first
        if any(phrase in command for phrase in ["what is tomorrow's date", "tomorrow's date"]):
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            response = tomorrow.strftime("%A, %B %d, %Y")
            self.speak(f"Tomorrow's date is {response}", wait=True)
            return True
            
        if any(word in command for word in self.commands['date']):
            today = datetime.date.today().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}", wait=True)
            return True

        if command in ['open chrome', 'hey open chrome', 'hi open chrome']:
            success = self.open_in_chrome("https://www.google.com")
            if success:
                self.speak("Opening Chrome browser", wait=True)
            else:
                self.speak("Opening your browser", wait=True)
            return True
            
        # Handle name queries
        if self.handle_name_query(command):
            return True
            
        # Handle system commands
        if any(word in command for word in self.commands['system']):
            return self.handle_system_commands(command)
            
        # Handle jokes
        if any(word in command for word in self.commands['joke']):
            return self.handle_joke()
            
        # Handle email
        if any(word in command for word in self.commands['email']):
            return self.handle_email(command)
            
        # Handle reminders
        if any(word in command for word in self.commands['reminder']):
            return self.handle_reminder(command)
            
        # Handle games
        if any(word in command for word in self.commands['games']):
            return self.handle_game(command)
            
        # Handle calculations - moved before search to catch math queries
        if any(word in command for word in self.commands['calculation']):
            return self.handle_calculation(command)
            
        # Handle screenshot
        if any(word in command for word in self.commands['screenshot']):
            return self.handle_screenshot()
            
        # Handle definitions
        if any(word in command for word in self.commands['definition']):
            return self.handle_definition(command)
            
        # Handle weather
        if any(word in command for word in self.commands['weather']):
            return self.handle_weather()
            
        if any(word in command.split()[:2] for word in self.commands['greetings']):
            if len(command.split()) <= 3:
                responses = [
                    "Hello there! How can I help?",
                    "Hi! What can I do for you?",
                    "Yes, I'm listening. How may I assist you?"
                ]
                self.speak(random.choice(responses), wait=True)
                return True

        if any(word in command for word in self.commands['time']):
            current_time = time.strftime("%I:%M %p")
            self.speak(f"The time is {current_time}", wait=True)
            return True

        if any(word in command for word in self.commands['music']):
            song = command.replace('play', '').replace('music', '').replace('song', '').replace('spotify', '').strip()
            if song:
                self.speak(f"Playing {song} on Spotify", wait=True)
            self.play_music(song if song else None)
            return True

        # Handle search - now more comprehensive
        if any(word in command for word in self.commands['search']):
            query = command
            return self.handle_search(query)

        if any(word in command for word in self.commands['news']):
            return self.handle_search(command)

        if 'open' in command:
            for app, details in self.commands['apps'].items():
                if app in command:
                    if app == 'chrome':
                        success = self.open_in_chrome("https://www.google.com")
                        if success:
                            self.speak("Opening Chrome browser", wait=True)
                        else:
                            self.speak("Opening your browser", wait=True)
                    elif app == 'spotify':
                        self.play_music()
                    else:
                        self.open_in_chrome(details[0])
                    self.speak(details[1], wait=True)
                    return True
            self.speak("Which app would you like me to open?", wait=True)
            return True

        if any(word in command for word in self.commands['exit']):
            self.speak("Goodbye! Have a wonderful day.", wait=True)
            exit()

        # If we get here, provide more specific help
        if "ipl" in command or "cricket" in command:
            return self.handle_search("today ipl match")
            
        if "gold" in command and "price" in command:
            return self.handle_search("today gold price")
            
        if len(self.command_history) > 3:
            self.speak("I'm not sure I understand. Try being more specific.", wait=True)
        else:
            help_msg = "I can help with many things including: "
            help_msg += "searching the web, calculations, system controls, jokes, emails, reminders, and more. "
            help_msg += "Try something like: 'search for today's IPL match', 'what is 2 plus 2', 'tell me a joke', or 'set brightness to 50%'"
            self.speak(help_msg, wait=True)
        return False

    def introduction(self):
        self.speak(f"Hello! I am {self.name}, your personal assistant.", wait=True)
        time.sleep(0.5)
        self.speak("How may I assist you today?", wait=True)

def main():
    safia = SafiaAssistant()
    safia.introduction()
    
    while True:
        command = safia.listen()
        
        if command:
            if not safia.process_command(command):
                pass
        elif time.time() - safia.last_command_time > 30:
            safia.speak("I'm here if you need anything.", wait=True)
            safia.last_command_time = time.time()

if __name__ == "__main__":
    main()