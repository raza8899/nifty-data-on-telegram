import asyncio
from nsepython import *
from datetime import datetime, timedelta
import pandas as pd
from telegram import Bot
from telegram.constants import ParseMode


# Telegram Bot Configuration
TOKEN = 'your_bot_token'  # Replace with your bot token
CHAT_ID = 'your_chat_id'  # Replace with your chat ID

async def send_telegram_message(message):
    """Send a formatted message to Telegram using python-telegram-bot"""
    bot = Bot(token=TOKEN)
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)


def format_pe_message(today_str, pe_today, pe_last_week_avg, pe_last_month_avg, pe_last_six_months_avg, pe_today_nifty500, pe_last_six_months_nifty500,
                      pe_today_smallcap250, pe_last_six_months_smallcap250):
    """Format the P/E ratio data into a Telegram message"""
    message = (
        f"<b>P/E Ratio Report</b>\n\n"
        
        f"📊 <b>NIFTY 50</b>\n\n"
        f"📅 <b>Today ({today_str}):</b> {round(pe_today.values[0], 2) if not pe_today.empty else 'Data not available'}\n \n"
        f"📈 <b>Last 7 days:</b> {pe_last_week_avg if pe_last_week_avg else 'Data not available'}\n \n"
        f"📅 <b>Last 30 days:</b> {pe_last_month_avg if pe_last_month_avg else 'Data not available'}\n \n"
        f"📅 <b>Last 180 days:</b> {pe_last_six_months_avg if pe_last_six_months_avg else 'Data not available'}\n \n \n"

        f"📊 <b>NIFTY 500</b>\n\n"
        f"📅 <b>Today ({today_str}):</b> {round(pe_today_nifty500.values[0], 2) if not pe_today_nifty500.empty else 'Data not available'}\n\n"
        f"📅 <b>Last 180 days average:</b> {pe_last_six_months_nifty500 if pe_last_six_months_nifty500 else 'Data not available'}\n\n\n"
        
        f"📊 <b>NIFTY SMALLCAP 250</b>\n\n"
        f"📅 <b>Today ({today_str}):</b> {round(pe_today_smallcap250.values[0], 2) if not pe_today_smallcap250.empty else 'Data not available'}\n\n"
        f"📅 <b>Last 180 days average:</b> {pe_last_six_months_smallcap250 if pe_last_six_months_smallcap250 else 'Data not available'}\n\n"
    )
    return message

def get_pe_data(symbol, start_date, end_date):
    """Fetch PE data for the given date range and clean it"""
    try:
        # Fetch data using index_pe_pb_div method
        index_data = index_pe_pb_div(symbol, start_date, end_date)
        
        # Clean and split concatenated PE data
        pe_values = index_data['pe']
        return pd.Series(pe_values, dtype=float)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.Series([])  # Return empty series on error
    

async def calculate_pe_ratios():
    indices = ["NIFTY 50", "NIFTY 500", "NIFTY SMALLCAP 250"]
    
    # Get today's date
    today = datetime.now()
    today_str = today.strftime("%d-%b-%Y")
    
    # Calculate date ranges for last week, month, and six months
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=30)
    six_months_ago = today - timedelta(days=180)
    
    one_week_ago_str = one_week_ago.strftime("%d-%b-%Y")
    one_month_ago_str = one_month_ago.strftime("%d-%b-%Y")
    six_months_ago_str = six_months_ago.strftime("%d-%b-%Y")
    
    # Get PE ratio for today
    pe_today = get_pe_data(indices[0], today_str, today_str)
    
    # Get PE ratios for the last week, month, and six months
    pe_last_week = get_pe_data(indices[0], one_week_ago_str, today_str)
    pe_last_month = get_pe_data(indices[0], one_month_ago_str, today_str)
    pe_last_six_months = get_pe_data(indices[0], six_months_ago_str, today_str)
    
    # Calculate averages, handling empty series and rounding to 2 decimal places
    pe_last_week_avg = round(pe_last_week.mean(), 2) if not pe_last_week.empty else None
    pe_last_month_avg = round(pe_last_month.mean(), 2) if not pe_last_month.empty else None
    pe_last_six_months_avg = round(pe_last_six_months.mean(), 2) if not pe_last_six_months.empty else None
    
    pe_today_nifty500 = get_pe_data(indices[1], today_str, today_str)
    pe_last_six_months_nifty500 = get_pe_data(indices[1], six_months_ago_str, today_str).mean()

    pe_today_smallcap250 = get_pe_data(indices[2], today_str, today_str)
    pe_last_six_months_smallcap250 = get_pe_data(indices[2], six_months_ago_str, today_str).mean()

    # Format message
    message = format_pe_message(today_str, pe_today, pe_last_week_avg, pe_last_month_avg, pe_last_six_months_avg, pe_today_nifty500, 
                                round(pe_last_six_months_nifty500, 2) if pe_last_six_months_nifty500 else None,
                                pe_today_smallcap250, round(pe_last_six_months_smallcap250, 2) if pe_last_six_months_smallcap250 else None)
    
    # Send message to Telegram
    await send_telegram_message(message)

if __name__ == "__main__":
    # Run the async function
    asyncio.run(calculate_pe_ratios())