# utils.py
import os
from elevenlabs.client import ElevenLabs
from datetime import datetime

class APIBridge:
    def __init__(self, eleven_key):
        self.eleven_key = eleven_key
        self.eleven = ElevenLabs(api_key=eleven_key) if eleven_key else None
        self.voice_id = "JBFqnCBsd6RMkjVDRZzb" # Rachel
        self.decision_file = 'data/decision_log.txt'
        
        # Ensure data directory
        os.makedirs('data', exist_ok=True)

    def capture_voice(self, audio_file_path):
        """Transcribes verbal input using ElevenLabs Scribe."""
        if not self.eleven:
            print("ElevenLabs API Key not present.")
            return "No Audio Transcription"
            
        try:
            with open(audio_file_path, "rb") as audio:
                # Using Scribe v1 for high-accuracy financial transcription
                response = self.eleven.scribe.transcribe(model="scribe_v1", file=audio)
                return response.text
        except Exception as e:
            print(f"Scribe Error: {e}")
            return ""

    def speak_advice(self, text):
        """Converts the final advice into verbal output."""
        if not self.eleven:
            print("ElevenLabs API Key not present. Skipping TTS.")
            return None
            
        try:
            audio = self.eleven.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            
            output_path = "data/latest_advice.mp3"
            with open(output_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)
            
            print(f"Advice spoken and saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"TTS Error: {e}")
            return None

    def log_decision_to_file(self, decision_data):
        """
        Maintains the 'Decision Log' as a financier's audit trail.
        decision_data: dict containing 'trigger', 'advice', 'rationale', 'impact'
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"ID: {timestamp.replace(' ', '-').replace(':', '')}\n"
            f"DATE: {timestamp}\n"
            f"CONTEXT/TRIGGER: {decision_data.get('trigger')}\n"
            f"ADVICE: {decision_data.get('advice')}\n"
            f"RATIONALE: {decision_data.get('rationale')}\n"
            f"PROBABILITY/IMPACT: {decision_data.get('impact')}\n"
            f"{'='*40}\n"
        )
        with open(self.decision_file, "a") as f:
            f.write(entry)