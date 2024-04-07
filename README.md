# AI Notetaker
### Written by Jayden John
## Summary
This is an AI powered nearly live transcription based notetaker built using Python's Tkinter and OpenAI's Whisper and ChatGPT.

![Screenshot 2024-04-07 132638](https://github.com/Jumpy-display/Whisper-GPT-Notetaker/assets/124234331/b68bd9f7-13d1-49b6-9fb4-9bbb00b97f10)

## Installation
1. Make sure you have python installed on you computer. To make it work with Whisper it must be between versions 3.8-3.11.
2. Whisper requires the command-line tool [`ffmpeg`](https://ffmpeg.org/) to be installed on your system, which is available from most package managers:
```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
3. Download whisper from https://github.com/openai/whisper using the following command:
```
pip install -U openai-whisper
```
5. Clone the repository:
```bash
git clone https://github.com/Jumpy-display/Whisper-GPT-Notetaker.git
```
5. Install the dependencies:
```bash
pip install -r requirements.txt
```
## Usage
Run the script:
```bash
python noteTaker.py
```
## Features
- Nearly live transcriptions powered by Whisper
- Notes created from the live transcription by chatgpt

## Credits
This project includes code from [gpt4free](https://github.com/xtekky/gpt4free.git), which is licensed under the GNU General Public License v3.0. 
