from apscheduler.schedulers.background import BackgroundScheduler
from crud import token_crud
from db.database import SessionLocal
import logging

sched = BackgroundScheduler(daemon=True)
logger = logging.getLogger()


# Run the cron to remove expired tokens from database every day
@sched.scheduled_job('interval', days=1)
def delete_expired_tokens():
    db = SessionLocal()
    db_tokens = token_crud.delete_expired_tokens(db=db)
    logger.info(f"Tokens: Expired tokens deleted: {db_tokens}")
    db.close()
