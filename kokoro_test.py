from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code='a')   # American English

text = """
I'm Calma.
I'm really happy to finally have a voice.
"""

generator = pipeline(
    text,
    voice='af_heart',
    speed=1,
)

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f"output_{i}.wav", audio, 24000)

print("Done!")