import subprocess
import tkinter as tk
from tkinter.filedialog import askopenfilename
import json

import time
import sys
import os
import shutil

if sys.platform == "win32":
    from ctypes import windll

def type_out(text, speed=0.0175):
    for char in str(text):
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

def get_ffprobe_path():
    system_ffprobe = shutil.which("ffprobe")
    if system_ffprobe:
        return system_ffprobe
    
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    ffprobe_name = "ffprobe.exe" if sys.platform == "win32" else "ffprobe"
    ffprobe_path = os.path.join(base_dir, "ffprobe", ffprobe_name)

    if not os.path.exists(ffprobe_path):
        raise FileNotFoundError(
            f"FFprobe not found. Either install system-wide or bundle {ffprobe_name} "
            f"in the 'ffprobe' directory. Searched at: {ffprobe_path}"
        )

    return ffprobe_path
        
def is_video(filepath):
    try:
        ffprobe_path = get_ffprobe_path()

        cmd = [
            ffprobe_path,  # The ffprobe executable
            "-v", "error",  # Only show errors (suppresses other output)
            "-select_streams", "v",  # Select only video streams
            "-show_entries", "stream=codec_type",  # Show the type of each stream
            "-of", "csv=p=0",  # Output format: CSV with no headers or wrappers
            filepath  # The file to analyze
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0  # Hide console on Windows
        )

        return result.returncode == 0 and "video" in result.stdout
    except Exception:
        return False

def user_input():
    print("__________________________________")
    print("Video GOP and Frame Metadata Analysis Tool")
    error = False
    first_run = True

    while True:
        if not first_run:
            type_out("Choose your video or enter full video path (press Enter to browse): ", 0.004)
        else:
            print("Choose your video or enter full video path (press Enter to browse): ")
            first_run = False

        cli_input = input().strip()
        if cli_input:
            filepath = os.path.normpath(cli_input.strip('"\''))
            if not os.path.isfile(filepath):
                if error:
                    print("\033[F\033[K", end="")
                    error = False
                print("\033[F\033[K", end="")
                print("\033[F\033[K", end="")
                print(f"\033[KFile not found: {filepath}")
                error = True
                continue
        else:
            if sys.platform == "win32":
                windll.shcore.SetProcessDpiAwareness(2)
            root = tk.Tk()
            root.withdraw()
            filepath = askopenfilename(title="Select a Video File", 
                                       filetypes = [
                                           ("Video files", 
                                            "*.mp4 *.m4v *.mov *.avi *.wmv *.mkv *.flv *.webm *.mts *.m2ts *.3gp *.ogv "
                                            "*.mpg *.mpeg *.vob *.ts *.m2v *.m4p *.m4b *.m4r *.3g2 *.f4v *.f4p *.f4a *.f4b "
                                            "*.asf *.divx *.rm *.rmvb *.viv *.amv *.svi *.mxf *.roq *.nsv *.flv *.f4v "
                                            "*.yuv *.drc *.gif *.gifv *.mng *.qt *.yuv *.wmv *.wm *.wma *.webm "
                                            "*.dv *.dvd *.m2p *.m2t *.m2ts *.m4v *.mp2 *.mpv *.mpe *.mpeg1 *.mpeg2 *.mpeg4 "
                                            "*.ogg *.ogx *.ogm *.spx *.opus *.mj2 *.mjp2 *.mxf *.nut *.oma *.opus *.pva *.rcv *.rv "
                                            "*.svi *.swf *.vob *.wtv *.xvid"
                                            ),
                                            ("All files", "*.*")
                                            ])
            if not filepath:  # User canceled dialog
                if error:
                    print("\033[F\033[K", end="")
                    error = False
                print("\033[F\033[K", end="")
                print("\033[F\033[K", end="")
                print("\033[KCancelled. Try again.")
                error = True
                continue

        if is_video(filepath):
            if error:
                print("\033[F\033[K", end="")
            print("\033[F\033[K", end="")
            print("\033[F\033[K", end="")
            print(f"\033[KVideo selected: {filepath}")
            break
        else:
            if error:
                print("\033[F\033[K", end="")
                error = False
            print("\033[F\033[K", end="")
            print("\033[F\033[K", end="")
            print(f"\033[KInvalid video file: {filepath}")
            error = True

    print("\nInstructions:")
    print("- PTS offset enabled by default to ensure 0-based timestamps.")
    print("- Type 1p or 2p instead of 1 or 2 to disable.")
    print("- Ignore if unsure.\n")

    error = False
    while True:
        analysis_type = input("Enter 1 for [key-frame interval analysis] (fast) or 2 for [full, frame-analysis] (slower): ")
        if analysis_type in ['1', '2', '1p', '2p']:
            if error:
                print("\033[F", end="")
                print("\033[F\033[2K\033[M", end="")
                print("\033[F\033[2K\033[M", end="")
                print("\033[E", end="")
            break
        else:
            if error:
                print("\033[F", end="")
                print("\033[F\033[2K\033[M", end="")
                print("\033[F\033[2K\033[M", end="")
                print("\033[E", end="")
            else:
                error = True 
            type_out("Invalid input.")
            
    
    print("__________________________________")

    return filepath, analysis_type

def return_frame_data(filepath, analysis_type):
    ffprobe_path = get_ffprobe_path()

    keyframe_command = [
        ffprobe_path, 
        "-loglevel", "error", 
        "-select_streams", "v:0", 
        "-show_packets", 
        "-show_entries", "packet=pts_time,flags", 
        "-show_entries", "stream=codec_name,width,height,avg_frame_rate",
        "-show_entries", "format=duration,size",
        "-of", "json", 
        filepath
    ]

    full_frames_command = [
        ffprobe_path, 
        "-loglevel", "error", 
        "-select_streams", "v:0",  
        "-show_frames",
        "-show_packets", 
        "-show_entries", "packet=pts_time,flags", 
        "-show_entries", "frame=pict_type,pkt_size",
        "-show_entries", "stream=codec_name,width,height,avg_frame_rate",
        "-show_entries", "format=duration,size",
        "-of", "json",
        filepath
    ]
    
    if analysis_type in ['1','1p']:
        result = subprocess.run(keyframe_command, capture_output=True, text=True, check=True)
    elif analysis_type in ['2', '2p']:
        result = subprocess.run(full_frames_command, capture_output=True, text=True, check=True)

    return json.loads(result.stdout)

def process_frame_data_to_keyframes(frame_data):
    keyframe_packets = []

    for key in ["packets", "packets_and_frames"]:
        try:
            for packet in frame_data[key]:
                if packet.get("type") == "packet" and "K" in packet["flags"]:
                    keyframe_packets.append(packet)
                elif "flags" in packet and "K" in packet.get("flags"):
                    keyframe_packets.append(packet)
        except KeyError:
            continue

    specs = frame_data["streams"][0]
    specs['duration'] = frame_data["format"]["duration"]
    specs['size'] = frame_data["format"]["size"]

    return keyframe_packets, specs

def process_all_frames(frame_data):
    frames_size = {'I':0, 'P':0, 'B':0}
    frames_count = {'I':0, 'P':0, 'B':0}

    for frame in frame_data["packets_and_frames"]:
        if frame.get("type") == "frame":
            frames_count[frame["pict_type"]] += 1
            frames_size[frame["pict_type"]] += int(frame["pkt_size"])
    
    return frames_size, frames_count

def process_keyframes(keyframe_packets, p):
    keyframe_count = len(keyframe_packets)
    keyframe_data = []
    first_loop = True
    pts_offset = 0

    for keyframe_dict in keyframe_packets:
        time = keyframe_dict["pts_time"]
    
        if first_loop and p:
            pts_offset = float(time)

        time = float(time) - pts_offset

        if first_loop or time == 0:
            keyframe_data.append((f"Keyframe position: {time:.6f} sec", " "))
            first_loop = False
        else:
            keyframe_data.append((f"Keyframe position: {time:.6f} sec", f"Interval: {time - last_keyframe_time:.6f} seconds"))

        last_keyframe_time = time

    return keyframe_data, keyframe_count

def parse_fraction(fraction_str):
    parts = fraction_str.split("/")
    numerator = int(parts[0])
    denominator = int(parts[1])
    return numerator / denominator

def main():
    filepath, analysis_type = user_input()

    print(f"\nUsing FFprobe at: {get_ffprobe_path()}")
    print(f"\nAnalysing {filepath}")

    frame_data = return_frame_data(filepath, analysis_type)
    keyframe_packets, specs = process_frame_data_to_keyframes(frame_data)

    if analysis_type in ["1p", "2p"]:
        keyframe_data, keyframe_count = process_keyframes(keyframe_packets, False)
    elif analysis_type in ["1", "2"]:
        keyframe_data, keyframe_count = process_keyframes(keyframe_packets, True)

    print("\n[Video Data]")
    print(f"Codec: {specs["codec_name"]}")
    print(f"Dimensions: {specs["width"]} x {specs["height"]} pixels")
    print(f"Frame Rate: {parse_fraction(specs["avg_frame_rate"])} fps")
    print(f"Video Duration: {float(specs["duration"]):.2f} seconds")
    print(f"Video Size: {specs["size"]} bytes")

    if analysis_type in ["2", "2p"]:
        frames_size, frames_count = process_all_frames(frame_data)
        total_frames_size = sum(frames_size.values())

        max_digits_frames = len(str(max(frames_count["I"], frames_count["P"], frames_count["B"])))
        max_digits_size = len(str(max(frames_size["I"], frames_size["P"], frames_size["B"])))
        
        print("\n[Frame Data]")
        for IPB in frames_count:
            print(f"[{IPB}-Frames]   Count: {frames_count[IPB]}{(max_digits_frames - len(str(frames_count[IPB]))) * " "}   Total Size: {frames_size[IPB]} bytes {(max_digits_size - len(str(frames_size[IPB]))) * " "} ({(frames_size[IPB] / total_frames_size)*100:.2f}%)")
        
    print("\n[Keyframes Data]")
    if analysis_type in ["1", "1p"]:
        print(f"Keyframe count: {keyframe_count} \n")

    first_run_flag = True
    for tuple in keyframe_data:
        if first_run_flag:
            position, interval = tuple
            print(f"{position}")
            first_run_flag = False
        else:
            position, interval = tuple
            print(f"{position},  {interval}")

    print("__________________________________")
    print("\n")

while True:    
    main()
    input_from_user = input("\nEnter to run again or type 'exit'... ")  # Forces the terminal to wait
    if input_from_user == "exit":
        break
