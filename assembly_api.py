import assemblyai as aai

aai.settings.api_key = "8962055919874d63a7bc498e783e41aa"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("https://assembly.ai/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)