#!/usr/bin/env python3

# Connect to Telegram as user (Client API)
from telethon import TelegramClient, events, sync, connection, types

# Adding someone else to such chat or channel
from telethon.tl.functions.channels import InviteToChannelRequest

# Filter chat admins
from telethon.tl.types import ChannelParticipantsAdmins

# Filter chat bots
#from telethon.tl.types import ChannelParticipantsBots

from pathlib import Path
import logging

# Defaults
proxy_host = ''
proxy_port = 443
proxy_secret = '00000000000000000000000000000000'

# Load config
from config import *


# Setup Logger configuration (console output)
log = logging.getLogger()

log.setLevel(logging.getLevelName(log_level or 'DEBUG'))

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)-5s] %(message)s', '%d.%m.%Y %H:%M:%S'))
log.addHandler(consoleHandler)

if log_path:
    fileHandler = logging.FileHandler("{0}/{1}.log".format(log_path or Path(__file__).resolve().parent, Path(log_name).stem or Path(__file__).stem))
    fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-5s - %(message)s', '%d.%m.%Y %H:%M:%S'))
    log.addHandler(fileHandler)


def filter_users(users, exclude_hidden:bool=True, exclude_bots:bool=True, exclude_deleted:bool=True, exclude_offline:int=30, users_blacklist:list=[], phase:str='FILTER'):
    from datetime import date

    log.debug(f"✔ [{phase}] Exclude: hidden usernames = {exclude_hidden}, bots = {exclude_bots}, deleted users = {exclude_deleted}, offline users = {exclude_offline} day(s), blacklist = {users_blacklist}")
    usernames_hidden_ids = []
    usernames_bots = []    
    usernames_deleted = []
    usernames_offline = []
    usernames_blacklist = []
    usernames_collected = []

    try:
        for user in users:
            # Calculate when user was online
            if isinstance(user.status, types.UserStatusOffline):
                user_was_online = date.today() - date(user.status.was_online.year, user.status.was_online.month, user.status.was_online.day)

            # Exclude users with hidden username
            if user.username is None and exclude_hidden:
                usernames_hidden_ids.append(user.id)
                continue
            # Exclude deleted users
            elif user.deleted and exclude_deleted:
                usernames_deleted.append(user.username)
                continue
            # Exclude bots
            elif user.bot and exclude_bots:
                usernames_bots.append(user.username)
                continue
            # Exclude users, which was online a long time ago
            elif isinstance(user.status, types.UserStatusOffline) and exclude_offline > 0 and user_was_online.days > exclude_offline:
                usernames_offline.append(user.username)
                continue
            # Exclude users from blacklist
            elif user.username in users_blacklist:
                usernames_blacklist.append(user.username)
                continue
            # Perfect users
            else:
                usernames_collected.append(user.username)
            
        log.info (f"✔ [{phase}] Hidden usernames excluded total: {len(usernames_hidden_ids)}")
        log.debug(f"✔ [{phase}] Hidden usernames excluded id list: {usernames_hidden_ids}")
        log.info (f"✔ [{phase}] Deleted users excluded total: {len(usernames_deleted)}")
        log.debug(f"✔ [{phase}] Deleted users excluded list: {usernames_deleted}")
        log.info (f"✔ [{phase}] Bots excluded total: {len(usernames_bots)}")
        log.debug(f"✔ [{phase}] Bots excluded list: {usernames_bots}")
        if exclude_offline > 0:
            log.info (f"✔ [{phase}] Offline more than {exclude_offline} day(s) users excluded total: {len(usernames_offline)}")
            log.debug(f"✔ [{phase}] Offline users list: {usernames_offline}")
        log.info (f"✔ [{phase}] Blacklist excluded total: {len(usernames_blacklist)}")
        log.debug(f"✔ [{phase}] Blacklist excluded list: {usernames_blacklist}")
        log.info (f"✔ [{phase}] Total excluded: {len(usernames_hidden_ids) + len(usernames_deleted) + len(usernames_bots) + len(usernames_offline) + len(usernames_blacklist)}")
        log.info (f"✔ [{phase}] Total collected: {len(usernames_collected)}")
        log.debug(f"✔ [{phase}] Collected usernames list: {usernames_collected}")
        return usernames_collected
    except Exception as e:
        log.error(f"■ [{phase}] Problem while try to filter users")
        log.debug(f"■ [{phase}] Exception: \n{e}")



log.info("▶ Start script")

if proxy_host:
    client = TelegramClient(
        api_id, 
        api_id, api_hash, 
        proxy=(proxy_host, proxy_port, proxy_secret), 
        connection=connection.tcpmtproxy.ConnectionTcpMTProxyRandomizedIntermediate
    )
else:
    client = TelegramClient(
        api_id, 
        api_id, api_hash
    )
client.start()


usernames_import = []
for chat in export_chats:
    usernames_export = []

    log.info(f"✔ [EXPORT] Parse all users from chat @{chat} ...")
    users = client.get_participants(chat)

    log.info (f"✔ [EXPORT] Users parsed: {len(users)}")
    log.debug(f"✔ [EXPORT] Users: \n{users}")

    usernames_export = filter_users(
        users=users, 
        exclude_bots=exclude_bots, 
        exclude_deleted=exclude_deleted, 
        exclude_offline=exclude_offline_days, 
        users_blacklist=usernames_blacklist
    )
    
    # Exclude chat admins
    if exclude_admins:
        usernames_admins = []
        
        for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if user.username in usernames_export:
                usernames_export.remove(user.username)
                usernames_admins.append(user.username)
        
        log.info (f"✔ [FILTER] Admins usernames excluded total: {len(usernames_admins)}")
        log.debug(f"✔ [FILTER] Admins usernames excluded list: {usernames_admins}")
    
    usernames_import = usernames_import + usernames_export
    log.info(f"✔ [FILTER] After filter: {len(usernames_import)}")


if len(export_chats) > 1:
    log.info("✔ [DEDUP] Deduplicate users from all chats...")
    before_dedup = len(usernames_import)
    usernames_import = list(set(usernames_import))
    log.info(f"✔ [DEDUP] After deduplication: {len(usernames_import)} (duplicates: {before_dedup - len(usernames_import)})")

log.info(f"✔ [COMPARE] Parse all users from target chat @{target_chat} ...")
users = client.get_participants(target_chat)

usernames_target = []
if len(users) > 0:
    usernames_target = filter_users(
            users=users, 
            exclude_bots=exclude_deleted, 
            exclude_deleted=exclude_deleted, 
            exclude_offline=0, 
            phase='COMPARE'
    )

log.info("✔ [COMPARE] Exclude from import users, which already exist in target chat...")
usernames_import = list( set(usernames_import) - set(usernames_target) )

log.info(f"✔ [COMPARE] TOTAL: {len(usernames_import)}")

if import_limit > 0:
    log.info(f"✔ [IMPORT] Add {import_limit} user(s) to chat @{target_chat}")
    usernames_import = usernames_import[:import_limit]
else:
    log.info(f"✔ [IMPORT] Add all users to chat @{target_chat}")

log.info(f"☻ [IMPORT] Users: {usernames_import}")
client(InviteToChannelRequest(target_chat, usernames_import))

log.info("⚑ Finish script")