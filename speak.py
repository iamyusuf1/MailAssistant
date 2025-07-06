import edge_tts
import asyncio
import re
import os
import time
import pygame

def clean_text(text):
    cleaned = re.sub(r'[*_#>`~\-]', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

async def speak_async(text):
    text = clean_text(text)
    filename = f"temp_{int(time.time())}.mp3"

    # You can change the voice below to try different male voices
    voice = "en-US-GuyNeural"  # Clear male voice (American)
    rate = "-40%"  # 🔊 Slows down speed (can adjust to -20%, etc.)
    
    
     # Add prosody tags to control speech rate
    slow_text = f"<speak><prosody rate='{rate}'>{text}</prosody></speak>"
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.5)

    pygame.mixer.quit()
    os.remove(filename)

def speak(text):
    asyncio.run(speak_async(text))
