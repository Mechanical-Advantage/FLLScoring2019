"""Configuration settings for FLL Pit Display."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))
dbdir = 'D:\mascout\FLLScoring2019\fllipit'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbdir, 'fllipit.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\mascout\FLLScoring2019\\fllipit\\fllipit.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
EVENT_NAME = 'Littleton FLL Qualifier'
TEST_DB = True
DB_FILE = 'D:\\mascout\\FLLScoring2019\\fllipit\\fllipit.db'

# The number of qualifying rounds, minimum is
USE_5_QUAL_ROUNDS = True

print(SQLALCHEMY_DATABASE_URI)