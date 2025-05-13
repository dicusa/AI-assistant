# assistant/commands.py

from config import PREDEFINED_QUERIES
from .web import open_application, open_website, search_wikipedia, google_search
from .utils import get_greeting
from .parsers import (
    extract_city_from_query,
    extract_topic_from_query,
    parse_email_details,
    parse_reminder
)
from .plugins import weather, news, emailer, reminders
from .nlu import ask_chatgpt

def handle_query(query, speech_engine):
    print(query)
    if query in PREDEFINED_QUERIES:
        # speech_engine.speak(PREDEFINED_QUERIES[query])
        return True,PREDEFINED_QUERIES[query]

    # Weather intent
    elif "weather" in query:
        city = extract_city_from_query(query) or "jaipur" # Implement a helper to parse city
        response = weather.fetch_weather(city or "your location")
        # speech_engine.speak(response)
        return True,response

    # News intent
    elif "news" in query:
        topic = extract_topic_from_query(query)  # Implement helper or default None
        response = news.get_top_headlines(topic)
        # speech_engine.speak(response)
        return True,response

    # Email intent example: "send email to xyz@example.com subject Hello body How are you"
    elif "send email" in query:
        # Parse email, subject, body from query (implement parsing)
        to_email, subject, body = parse_email_details(query)
        response = emailer.send_email(to_email, subject, body)
        # speech_engine.speak(response)
        return True,response

    # Reminder intent example: "remind me to call mom in 10 minutes"
    elif "remind me" in query:
        reminder, minutes = parse_reminder(query)  # Implement parsing
        reminders.add_reminder(reminder, minutes)
        # speech_engine.speak(f"Reminder set for {minutes} minutes from now.")
        return True,f"Reminder set for {minutes} minutes from now."

    elif "who is" in query or "about" in query:
        topic = query.replace("who is", "").replace("about", "").strip()
        result = search_wikipedia(topic)
        # speech_engine.speak(result)
        return True,result
    elif "open chrome" in query:
        # speech_engine.speak(open_application("chrome"))
        return True
    elif "open android studio" in query:
        # speech_engine.speak(open_application("android studio"))
        return True
    elif "open" in query or "launch" in query:
        words = query.split()
        idx = words.index("open") if "open" in words else words.index("launch")
        site = words[idx + 1] if idx + 1 < len(words) else ""
        if site:
            speech_engine.speak(open_website(site))
        else:
            speech_engine.speak("Please specify what to open.")
        return True
    elif "the time" in query:
        from datetime import datetime
        # speech_engine.speak(f"The time is {datetime.now().strftime('%H:%M:%S')}")
        print("time")
        return True,f"The time is {datetime.now().strftime('%H:%M:%S')}"
    elif "quit anna" in query:
        speech_engine.speak("Glad I could help you. Goodbye!")
        return False
    elif "spell" in query:
        words = query.split()
        idx = words.index("spell")
        word = words[idx + 1] if idx + 1 < len(words) else ""
        if word:
            for letter in word:
                speech_engine.speak(letter)
                return True,word
        else:
            speech_engine.speak("Please specify a word to spell.")
        return False,"Please specify a word to spell."
    else:
        # Use ChatGPT for unknown queries or general conversation
        if query not in PREDEFINED_QUERIES:
            success, response = ask_chatgpt(query)
            if success:
                speech_engine.speak(response)
            else:
                speech_engine.speak("Google search initiated.")
                speech_engine.speak(google_search(query))
        return True,f"https://www.google.com/search?q={query.replace(' ', '+')}"
    return False
