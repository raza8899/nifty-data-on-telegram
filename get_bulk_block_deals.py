from nsepython import get_bulkdeals, get_blockdeals
from datetime import datetime
import pandas as pd
from telegram import Bot
from telegram.constants import ParseMode
import asyncio


# Telegram Bot Configuration
TOKEN = 'your_bot_token'  # Replace with your bot token
CHAT_ID = 'your_chat_id'  # Replace with your chat ID

async def send_telegram_message(message):
    """Send a formatted message to Telegram using python-telegram-bot"""
    bot = Bot(token=TOKEN)
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

def fetch_bulk_and_block_deals():
    """Fetches bulk and block deals from NSE and returns them."""
    
    # Get today's date
    today = datetime.now().strftime("%d-%m-%Y")
    
    # Fetch bulk deals
    bulk_deals = get_bulkdeals()
    
    # Fetch block deals
    block_deals = get_blockdeals()
    
    return today, bulk_deals, block_deals

def get_top_buying_deals(deals, top_n=5):
    """Filter and return top N buying deals."""
    # Check if deals DataFrame is empty
    if deals is None or deals.empty:
        return pd.DataFrame()  # Return empty DataFrame if no deals
    
    # Filter for buying deals and sort by quantity (or price as per your preference)
    buying_deals = deals[deals['Buy/Sell'] == 'BUY']
    top_buying_deals = buying_deals.nlargest(top_n, 'Quantity Traded')  # Change 'quantity' to 'price' if needed
    
    return top_buying_deals

def format_deals(today, bulk_top_buying, block_top_buying):
    """Format the top buying bulk and block deals into a presentable string."""
    
    message = f"<b>Top 5 Buying Bulk and Block Deals on {today}</b>\n\n"
    
    # Bulk Deals
    message += "<b>🔸 Top 5 Bulk Deals:</b>\n"
    if not bulk_top_buying.empty:
        for _, deal in bulk_top_buying.iterrows():
            message += (
                f"💼 <b>Stock:</b> {deal['Symbol']}, "
                f"<b>Quantity:</b> {deal['Quantity Traded']}, "
                f"<b>Price:</b> {deal['Trade Price / Wght. Avg. Price']}\n"
            )
    else:
        message += "No bulk buying deals available.\n"

    message += "\n"

    # Block Deals
    message += "<b>🔹 Top 5 Block Deals:</b>\n"
    if not block_top_buying.empty:
        for _, deal in block_top_buying.iterrows():
            message += (
                f"💼 <b>Stock:</b> {deal['Symbol']}, "
                f"<b>Quantity:</b> {deal['Quantity Traded']}, "
                f"<b>Price:</b> {deal['Trade Price / Wght. Avg. Price']}\n"
            )
    else:
        message += "No block buying deals available.\n"

    return message

async def caller_func():
    today, bulk_deals, block_deals = fetch_bulk_and_block_deals()
    
    # Get top buying deals
    bulk_top_buying = get_top_buying_deals(bulk_deals)
    block_top_buying = get_top_buying_deals(block_deals)
    
    # Format message
    message = format_deals(today, bulk_top_buying, block_top_buying)
    
    # Print or send the message to Telegram
    await send_telegram_message(message)


if __name__ == "__main__":
    # Run the async function
    asyncio.run(caller_func())
