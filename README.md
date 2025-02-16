## Demo screenshots

|Option 1 Example|Option 2 Example|
|--------|--------|
|![Demo Screenshot Option 1]()|![Demo Screenshot Option 2](https://github.com/miku4444/Video-GOP-and-Frame-Analysis-Tool/blob/main/demo%20screenshot%20option%202.png)|

## What does this tool do?

The Video GOP (Group of Pictures) and Frame Analysis Tool, shortened to VGFAT was built to calculate the keyframe intervals of a given video and display it in seconds. Initially based off the ffprobe commands provided here https://stackoverflow.com/a/18088156/

Wouldn't each keyframe intervals be the same length? Not always. Videos may have variable keyframe intervals. This is an option enabled by default in OBS for example (when keyframe interval is set to 0s).

This program has two options:

**Option 1** will display: 
- basic metadata
- keyframe timestamps
- each keyframe interval (seconds)

This is the fastest option as it only parses the metadata from every packet. 

**Option 2** will display:
- basic metadata
- keyframe timestamps
- each keyframe interval (seconds)
- the count of all B-frames, P-frames, I-frames and their respective sizes and proportion.
  
This option takes much longer compared to option 1 as every frame is decoded for the per-frame metadata to be read and analysed. Speed depends on disk i/o speed, complexity of decoding, video format, and video length. For example MP4 allows quicker metadata extraction from the file header compared to MKV which requires more extensive scanning.

If you want more extensive metadata there are already tools for that like [mediainfo](https://github.com/MediaArea/MediaInfo), a basic ffprobe prompt, or your local video player like mpv or vlc.

This tool will implement `ffprobe` commands, parse and filter the results, and perform necessary calculations. 

## How to use?
### [Releases are out of date, they haven't been updated yet]
**Option 1:**
- Download and run the standalone executables `(win/linux)` which are bundled with all required dependencies `(python, ffprobe)` and can be run straight out of the box.
- The tool will always use existing ffprobe installations when available, otherwise will fallback to the included `ffprobe` bundled at `v7.1`, current as of `24-01-25 (dd-mm-yy)`.

**Option 2:**
- Download and run the python file which contains only the script and requires you to have `ffprobe` and `python3` already installed and on your system PATH.
- If your distribution did not come with it, you also need `Tkinter` to access file system via gui.

For Debian/Ubuntu-based systems:

`python3 -m tkinter` to test

`sudo apt install python3-tk` to install

Supports Windows and Linux. Tested on Windows 11 x64 and WSL 2/Ubuntu.

## What does PTS offset do?

"Many file formats do not require timestamps to start at 0. In fact it can be important to have them start at other values if several files each make up part of a longer stream and you want to be able to non-destructively put them back together." - https://stackoverflow.com/a/10573528

This means the metadata of the first frame might not show it starting at 0.0 seconds - despite them playing from the "start" in a video player.  Enabling PTS (Presentation Time Stamp) offset means all Frame Presentation Time Stamps will be shifted back by an offset of the very first frame so that the analysis starts at the "correct" timing of 0.0 seconds as true to a video player.

Enabled or disabled won't affect the keyframe interval calculations, **these will always be correct**. An offset will apply to every frame and thus every calculation, so the final result will not be affected. It will however, affect the keyframe positions/timestamps shown. 

## Why is frame total sizes only displayed in bytes and not larger units of measurements like KB or MB?

To ensure accuracy and avoid confusion, this tool displays frame sizes strictly in bytes. Eliminating ambiguity between decimal or binary units.

Operating systems like Windows and Linux use the binary system and display the size of files in KB, MB, GB, etc. These are not true Kilobytes, Megabytes, and Gigabytes. Instead they are actually Kibibytes, Mebibytes, and Gibibytes. Their actual unit of measurement should be KiB, MiB, and GiB, but they omit the 'i' - leading to confusion between users. The reason they use the binary system is because calculations are based on powers of 2.

A Kilobyte (KB) is different from a Kibibyte (KiB).
- **1 KB (Kilobyte)** = **1000 bytes** as you would expect. However **1 KiB (Kibibyte) = 1024 bytes**.
- **1 MB (Megabyte)** = **1,000,000 bytes**. **1 "MB"** in Windows (actually an MiB) is **1,048,576 bytes** (1,024 × 1,024 bytes).
- **1 GB (Gigabyte)** = **1,000,000,000 bytes** in the decimal system. **1 GiB (Gibibyte) = 1,073,741,824 bytes** (1,024 × 1,024 × 1,024 bytes) in the binary system.

Most of the internets' websites like file hosters such as Google Drive or Discord use the decimal system. This is the system most people are used to.

This mismatch between decimal and binary risks misinterpretation for any non-byte units and so only bytes are used as the same term could mean different values to people.

## To Do
Priority
- use shlex.quote() on user-provided paths for subprocess sanitisation
- use pathlib.Path() for better path normalization
- switch ANSI escapes to curses library just in case of really old terminals 

Secondary
- transition to ijson ffprobe streamable output
    - can add progress bar for option 2 (can use rich progress bar)
    - change to progressive output and results
    - edit readme to add features column and include O(N) -> O(1) low memory overhead improvement over traditional ffprobe commands
- add unit tests with mocked ffprobe
- docstrings, function docs, typehinting
- update example pictures
- toggle to switch between bytes and larger units at the end, would probably need to replace terminal output, can also use rich
- use [rich](https://github.com/Textualize/rich) for nicer terminal output formatting
- pivot to object oriented code from current procedual code 

Ideas
- research into whether it's possible to implement application level multithreading by segmenting large videos and running ffprobe on each segment. would have to investigate temporary files after segmentation, or in-memory segmentation. Test if ffprobe can reliably analyze streamed input segments. https://stackoverflow.com/a/53267887
- could allow multiple files to be analysed at the same time
- gui?
- settings page to adjust p based times, enable/disable size formatting, decimal places
- could make bar graph of every frame against its size
