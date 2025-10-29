from environs import Env

env = Env()
env.read_env()

DB_USERNAME = env("DB_USERNAME")
DB_PASSWORD = env("DB_PASSWORD")
DB_IP = env("DB_IP")
DB_PORT = env("DB_PORT")
DB_NAME = env("DB_NAME")

JWT_TOKEN = env("JWT_TOKEN")
OWNER_PASSWORD = env("OWNER_PASSWORD")
