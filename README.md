# StreamDownloader

StreamDownloader is a Python script to download streams. Currently only working on https://www.myfidelio.at; soon going to add other popular websites (Netflix and more).
## Reuirements:
Windows users: Python 3 and above.
Linux users: Debian-based distro (Debian, Ubuntu, Kali, etc.)

## Installation

1. Download installation file for your platform (Linux\Windows).

2. Run the file:

Windows: Download StreamDownloader.exe and list.json, and place them in the same folder. Run the exe file, and there youhave it.

Linux:
```bash
cd /path/to/file
chmod +x install
sudo ./install
```
Install location will be user's directory (Windows: C:\Users\user\.StreamDownloader | Linux: /home/user/.StreamDownloader)    
## Current supported sources:
1. https://www.myfidelio.at/

## Usage (Linux)
CLI (Console interface):

```bash
python3 path/to/installation/folder/CLI.py
```

GUI (Graphical interface):
```bash
Command set during installation process
```

### Find source (Only required in CLI):
1. Open the stream in desktop browser.
2. Press F12 to open Developer tools.
3. Open "Network" tab.
4. Play the stream.
5. Wait for a file name segment* OR init.* to show up, and press its row.
6. Copy the URL given, like so:
```html
Given url:
https://www.example.com/random-string/random-string/<video\audio>/...

Copy:
www.example.com/random-string/random-string
```
Paste in script, and the script will do everything else.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
