from pydub import AudioSegment, effects
import os
from Settings import Settings
from pathlib import Path
import eyed3
import time

settings = Settings()
for file in list(Path(settings.InputDir).rglob("*.mp3")):
    artist = ""
    if settings.TagArtistMetadata:
        audiofile = eyed3.load(str(file))
        artist = audiofile.tag.artist
        if len(artist) == 0:
                artist = audiofile.tag.album_artist
        if(len(artist) == 0 and settings.UseFolderNameIfNoArtist):
            artist = file.parts[-1]

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
        outFile = "{}{}{}{}{}".format(settings.OutputDir,file.name[:3],"-p",i,".mp3")
        if settings.Debug: print("Exporting to "+outFile)
        start_action = time.perf_counter()
        segment.export(outFile, format="mp3")
        end_action = time.perf_counter()
        if settings.Debug: print(f"Export complete to {outFile} in {end_action - start_action:0.4f} seconds")
        if settings.TagArtistMetadata:
            if settings.Debug: print("Tagging Metadata")
            start_action = time.perf_counter()
            audiofile = eyed3.load(outFile)
            audiofile.tag.artist = artist
            audiofile.tag.track_num = i
            audiofile.tag.save()
            end_action = time.perf_counter()
            if settings.Debug: print(f"Metadata tagged in {end_action - start_action:0.4f} seconds")
        print(f"Total time for this segment: {end_action - start_segment:0.4f} seconds\n")
        i+=1
