# NSE PE Ratio and Bulk Deals Notification Bot

This repository contains two Python scripts that interact with the NSE (National Stock Exchange of India) to fetch P/E ratios for popular indices and the latest bulk and block deals. The results are sent to a specified Telegram chat using a Telegram bot.

## Overview

### Script 1: P/E Ratio Notification

This script retrieves the current and historical P/E ratios for the following indices:
- NIFTY 50
- NIFTY 500
- NIFTY SMALLCAP 250

It sends a formatted message to Telegram with the following details:
- Today's P/E ratio
- Average P/E ratios for the last week, month, and six months for NIFTY 50
- Today's P/E ratio and average for the last six months for NIFTY 500 and NIFTY SMALLCAP 250.

### Script 2: Bulk and Block Deals Notification

This script fetches the latest bulk and block deals from the NSE and sends the top 5 buying deals to the specified Telegram chat. 

## Requirements

- Python 3.x
- `nsepython`
- `pandas`
- `python-telegram-bot`
- `asyncio`
  
You can install the required packages using pip:

```bash
pip install nsepython pandas python-telegram-bot
```

## Configuration
Before running the scripts, replace the placeholders in the code with your actual Telegram Bot Token and Chat ID:

```
TOKEN = 'your_bot_token'  # Replace with your bot token
CHAT_ID = 'your_chat_id'  # Replace with your chat ID
```
You can visit these websites to know more about getting bot_token, and chat_id:
- [Bot Token](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token)
- [Chat ID](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)

## Scheduling the Scripts
You can schedule the scripts to run at specific times using cron. Here’s an example configuration:

To run the P/E Ratio Notification script every day at 6:30 AM from Monday to Friday:

Open the terminal in Mac, and then run the following steps in terminal:
```
chmod +x /path/to/pe_of_nifty_indices.py
crontab -e
30 6,11 * * 1-5 /usr/bin/python3 /path/to/pe_of_nifty_indices.py
```

## Contributing
Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.