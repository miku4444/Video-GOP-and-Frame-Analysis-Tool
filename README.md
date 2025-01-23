## Demo screenshot
![Demo Screenshot](https://github.com/miku4444/Video-GOP-and-Frame-Analysis-Tool/blob/main/demo%20screenshot.png)

## What does this tool do?

Partly based off the ffprobe commands provided here https://stackoverflow.com/a/18088156.
This program has two options:

**Option 1** will display: 
- keyframe timestamps
- each keyframe interval

Wouldn't all keyframe intervals be the same? Not always. Videos can have variable keyframe intervals. This is an option enabled by default in OBS for example (when keyframe interval is set to 0s).

**Option 2** will display:
- keyframe timestamps
- each keyframe interval
- the count of B-frames, P-frames, I-frames and their respective sizes and proportion.
  
This option takes a lot longer as every frame must be decoded to be analysed, compared to just parsing the metadata from every packet in option 1. Speed depends on the strength of your cpu, the complexity to decode the video, and video length.

This tool will implement `ffprobe` commands, filter the results and perform necessary calculations. 
The standalone executables `(win/linux)` are bundled with all required dependencies `(python, ffprobe)` and you can be run straight out of the box. The tool will always use system installed ffprobe when possible, otherwise will fallback to the included `ffprobe` bundled at `v7.1`, current as of `24-01-25 (dd-mm-yy)`.

The python file contains only the script and requires you to have `ffprobe` and `python3` already installed and on your system PATH. If your distribution did not come with it, you also need `Tkinter` to access file system via gui.

`sudo apt install python3-tk`  # For Debian/Ubuntu-based systems

Supports Windows and Linux. Tested on Windows 11 and WSL 2/Ubuntu.

## What does PTS offset do?

"Many file formats do not require timestamps to start at 0. In fact it can be important to have them start at other values if several files each make up part of a longer stream and you want to be able to non-destructively put them back together." - https://stackoverflow.com/a/10573528

This means that not every video will have the first frame starting at 0.0 seconds.  Enabling PTS (Presentation Time Stamp) offset means all Frame Presentation Time Stamps will be shifted back by an offset of the very first frame so that the analysis starts at the "correct" timing of 0.0 seconds as true to a video player.

Enabled or disabled won't affect the keyframe interval calculations, **these will always be correct**. An offset will apply to every frame and thus every calculation, so the final result will not be affected. It will however, affect the keyframe positions/timestamps shown. 

## Why is frame total sizes only displayed in bytes and not larger units of measurements like KB or MB?

To ensure accuracy and avoid confusion, this tool displays frame sizes strictly in bytes. Eliminating ambiguity between decimal or binary units.

Operating systems like Windows and Linux use the binary system and display the size of files in KB, MB, GB, etc. These are not true Kilobytes, Megabytes, and Gigabytes. Instead they are actually Kibibytes, Mebibytes, and Gibibytes. Their actual unit of measurement should be KiB, MiB, and GiB, but they omit the 'i' - leading to confusion between users. The reason they use the binary system is beacuse calculations are based on powers of 2.

A Kilobyte (KB) is different from a Kibibyte (KiB).
- **1 KB (Kilobyte)** = **1000 bytes** as you would expect. However **1 KiB (Kibibyte) = 1024 bytes**.
- **1 MB (Megabyte)** = **1,000,000 bytes**. **1 "MB"** in Windows (actually an MiB) is **1,048,576 bytes**.
- **1 GB (Gigabyte)** = **1,000,000,000 bytes** in the decimal system. **1 GiB (Gibibyte) = 1,073,741,824 bytes** (1,024 × 1,024 × 1,024 bytes) in the binary system.

Most of the internets' websites like file hosters such as Google Drive or Discord use the decimal system. This is the system most people are used to.

This mismatch between decimal and binary risks misinterpretation for any non-byte units and so only bytes are used as the same term could mean different values to people.
