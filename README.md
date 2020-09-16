# StreamDownloader

StreamDownloader is a Python script to download streams. Currently only working on https://www.myfidelio.at; soon going to add other popular websites (Netflix and more).
## Installation

Use git to clone the repository:

```bash
git clone https://github.com/rchenwh1te/StreamDownloader.git
```
install required dependencies:
```bash
cd StreamDownloader
pip install -r requirements.txt
```
Or:
```bash
cd StreamDownloader
python3 -m pip install -r requirements.txt
```

##Current supported sources:
1. https://www.myfidelio.at/ (Requires VPN outside Austria, Germany, Switzerland)

## Usage

```bash
python3 downloader.py
```

### Find source:
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
