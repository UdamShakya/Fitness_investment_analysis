from apscheduler.schedulers.background import BackgroundScheduler
from dashboard.data import fetch_stock_data
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=fetch_stock_data,
        trigger='interval',
        hours=1,
        id='stock_refresh',
        name='Hourly stock data refresh',
        replace_existing=True,
    )
    scheduler.start()
    logger.info("✅ Scheduler started — stock data refreshes every hour")
    return scheduler