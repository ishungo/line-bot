import sys
import os
# sys.path.insert(0, '/home/is/MyTask/line-bot/test_app/app/')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app as application
