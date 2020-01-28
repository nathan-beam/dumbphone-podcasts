from pydub import AudioSegment, effects
import os
from Settings import Settings
from pathlib import Path
import time

settings = Settings()
for file in list(Path(settings.InputDir).rglob("*.mp3")):
    sound = AudioSegment.from_mp3(str(file))
    length = len(sound)
    i = 1
    start = 0
    end = 0
    segment_length = settings.SegmentLen * settings.PlaybackSpeed
    if settings.Debug: print(f"-----Splitting file {file.name}-----")
    while end < length:
        start_segment = time.perf_counter()
        end = min(start+segment_length, length)
        if settings.Debug: print(f"Splitting segment {i}: {start/1000}s - {end/1000}s")
        start_action = time.perf_counter()
        segment = sound[start:end]
        end_action = time.perf_counter()
        if settings.Debug: print(f"Split complete in {end_action - start_action:0.4f} seconds")
        if(settings.PlaybackSpeed > 1):
            if settings.Debug: print("Adjusting playback speed")
            start_action = time.perf_counter()
            segment = effects.speedup(segment, playback_speed=settings.PlaybackSpeed)
            end_action = time.perf_counter()
            if settings.Debug: print(f"Playback speed ajdusted in {end_action - start_action:0.4f} seconds")

        start+=segment_length-settings.OverlapLen
        outFile = settings.OutputDir+str(i)+"-"+file.name
        if settings.Debug: print("Exporting to "+outFile)
        start_action = time.perf_counter()
        segment.export(outFile, format="mp3")
        end_action = time.perf_counter()
        if settings.Debug: 
            print(f"Export complete to {outFile} in {end_action - start_action:0.4f} seconds")
            print(f"Total time for this segment: {end_action - start_segment:0.4f} seconds\n")
        i+=1
