import asyncio 
from info import *
from pyrogram import enums
from pymongo.errors import DuplicateKeyError
from pyrogram.errors import UserNotParticipant
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

dbclient = AsyncIOMotorClient(DATABASE_URI)
db       = dbclient["File-Searcher"]
grp_col  = db["GROUPS"]

async def add_group(group_id, group_name, user_id, verified):
    data = {"_id": group_id, "name":group_name, 
            "user_id":user_id, "verified":verified}
    try:
       await grp_col.insert_one(data)
    except DuplicateKeyError:
       pass

async def get_group(id):
    data = {'_id':id}
    group = await grp_col.find_one(data)
    return dict(group)

async def update_group(id, new_data):
    data = {"_id":id}
    new_value = {"$set": new_data}
    await grp_col.update_one(data, new_value)

async def delete_group(id):
    data = {"_id":id}
    await grp_col.delete_one(data)

async def get_groups():
    count  = await grp_col.count_documents({})
    cursor = grp_col.find({})
    list   = await cursor.to_list(length=int(count))
    return count, list
