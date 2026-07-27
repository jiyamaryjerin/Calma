from kokoro import KPipeline
import soundfile as sf
import subprocess
import os
import uuid


class KokoroService:

    def __init__(self):
        print("Loading Kokoro...")
        self.pipeline = KPipeline(lang_code="a")
        print("Kokoro Loaded!")

    def generate_audio(self, text: str) -> str:

        generator = self.pipeline(
            text,
            voice="af_heart",
            speed=1,
        )

        audio_dir = "audio"
        os.makedirs(audio_dir, exist_ok=True)

        uid = str(uuid.uuid4())

        wav_path = os.path.join(audio_dir, f"{uid}.wav")
        mp3_path = os.path.join(audio_dir, f"{uid}.mp3")

        audio_chunks = []

        for _, _, audio in generator:
            audio_chunks.append(audio)

        if not audio_chunks:
            raise Exception("Failed to generate speech")

        # Combine all Kokoro chunks
        import numpy as np

        full_audio = np.concatenate(audio_chunks)

        sf.write(
            wav_path,
            full_audio,
            24000,
            subtype="PCM_16",
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                wav_path,
                "-codec:a",
                "libmp3lame",
                "-qscale:a",
                "2",
                mp3_path,
            ],
            check=True,
        )

        if os.path.exists(wav_path):
            os.remove(wav_path)

        return f"/audio/{uid}.mp3"


kokoro_service = KokoroService()