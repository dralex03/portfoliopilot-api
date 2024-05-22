import os
import datetime

from dotenv import load_dotenv


load_dotenv()

# Environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Other setting variables
MINIMUM_PASSWORD_LEN = 8
JWT_EXPIRY = datetime.timedelta(days=0, minutes=15) # 15 minute session validity