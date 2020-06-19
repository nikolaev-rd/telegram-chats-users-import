# App title: Telethon
# Short name: teleth0n

# You must get your own api_id and api_hash 
# from https://my.telegram.org under API Development.
api_id = '0000000'
api_hash = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


# Group chat(s) for export users (without '@')
export_chats = [
]

# Target group for import users (without '@')
target_chat = ''


# MTProxy settings
proxy_host = 'proxy.digitalresistance.dog'
proxy_port = 443
proxy_secret = 'd41d8cd98f00b204e9800998ecf8427e'


# Log level
# It can be: DEBUG | INFO | WARNING | ERROR | CRITICAL
log_level = 'INFO'

# Log file path without leading slash. 
# Example: /var/log
# Default: empty (no file logging).
log_path = '.'

# Log file name, '.log' extension will be added anyway. 
# Default: empty (used format: this_script_name.log)
log_name = ''


# List of usernames to exclude from import anyway (without '@')
usernames_blacklist = [
]

# Exclude admins of group(s) from import?
exclude_admins = True

# Exclude bots from import?
exclude_bots = True

# Exclude users marked as deleted from import?
exclude_deleted = True

# Filter users, which was online a long time ago - in days:
#   = 0 — only recently users will be imported
# Default: 30 days.
exclude_offline_days = 30

# Limit number of users for import
#   = 0 — all users will be imported
import_limit = 10