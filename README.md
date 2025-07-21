
# SourceStreamTool
A web-app used to update stream overlays

# Set Up
1. Install [Python](https://www.python.org/downloads/).
2. Extract SourceStreamTool-main to desired location.
3. Open [Scoreboard Tool](http://127.0.0.1:5000/).
4. Use OBS's built in text sources with "Read from file" checked.
5. Customize the text to you hearts conent!

# Please Note
The python script must be left running in order to update all data.

# Building EXE
python -m PyInstaller --onefile --name SourceStreamTool --add-data "templates;templates" main.py

# Credits
- Dcm05
- ChatGPT
