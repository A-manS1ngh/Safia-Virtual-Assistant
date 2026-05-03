import os
import pickle
from datetime import datetime

class UserProfile:
    """Handles user personalization and preferences"""
    def __init__(self):
        self.name = ''
        self.preferences = {
            'use_gtts': True,
            'preferred_volume': 0.8,
            'last_seen': None
        }
        self.history = []
        self.load_profile()

    def set_name(self, name):
        self.name = name.strip()
        self.save_profile()

    def update_preference(self, key, value):
        if key in self.preferences:
            self.preferences[key] = value
            self.save_profile()

    def add_history(self, command):
        self.history.append({
            'command': command,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.history) > 50:  # Keep last 50 commands
            self.history.pop(0)
        self.save_profile()

    def save_profile(self):
        profile_path = os.path.join('user_data', 'profile.pkl')
        os.makedirs('user_data', exist_ok=True)
        with open(profile_path, 'wb') as f:
            pickle.dump({
                'name': self.name,
                'preferences': self.preferences,
                'history': self.history
            }, f)

    def load_profile(self):
        profile_path = os.path.join('user_data', 'profile.pkl')
        if os.path.exists(profile_path):
            with open(profile_path, 'rb') as f:
                data = pickle.load(f)
                self.name = data.get('name', '')
                self.preferences = data.get('preferences', {})
                self.history = data.get('history', [])

class SystemInfo:
    """Provides system information and utilities"""
    @staticmethod
    def get_system_status():
        return {
            'cpu_usage': os.popen("top -bn1 | grep 'Cpu(s)'").read().strip(),
            'memory_usage': os.popen("free -m").read().strip(),
            'disk_usage': os.popen("df -h").read().strip()
        }

    @staticmethod
    def get_weather(city="current"):
        try:
            import requests
            api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with actual key
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = f"{base_url}appid={api_key}&q={city}"
            response = requests.get(complete_url)
            return response.json()
        except:
            return None

class KnowledgeBase:
    """Handles knowledge and information retrieval"""
    def __init__(self):
        self.facts = {
            'creator': "I was created by my developer using Python",
            'capabilities': "I can search the web, answer questions, play games, and more",
            'birthday': "My code was first initialized recently"
        }

    def query(self, question):
        question = question.lower()
        for key in self.facts:
            if key in question:
                return self.facts[key]
        return None

    def learn(self, fact, value):
        self.facts[fact.lower()] = value
        return f"I've learned about {fact}"

class Entertainment:
    """Handles games and entertainment features"""
    @staticmethod
    def play_game(game_name):
        games = {
            'rock paper scissors': {
                'moves': ['rock', 'paper', 'scissors'],
                'rules': {
                    ('rock', 'scissors'): 'Rock crushes scissors',
                    ('scissors', 'paper'): 'Scissors cut paper',
                    ('paper', 'rock'): 'Paper covers rock'
                }
            },
            'coin flip': {
                'outcomes': ['heads', 'tails']
            }
        }
        
        if game_name in games:
            return games[game_name]
        return None

    @staticmethod
    def tell_joke():
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them."
        ]
        return random.choice(jokes)

# Initialize components when module is imported
user_profile = UserProfile()
system_info = SystemInfo()
knowledge_base = KnowledgeBase()
entertainment = Entertainment()