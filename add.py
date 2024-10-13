# from telethon.sync import TelegramClient
# from telethon.tl.functions.messages import GetDialogsRequest
# from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, InputPeerChat
# from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
# from telethon.tl.functions.channels import InviteToChannelRequest
# import sys
# import csv
# import traceback
# import time
# import random
# from time import sleep  # Added import for sleep

# # Your API credentials
# api_id = 26935340
# api_hash = '5b00b55597cc61a30f7e05ae770836f1'
# phone = '+212693360369'
# client = TelegramClient(phone, api_id, api_hash)

# # Connect to Telegram
# client.connect()
# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     client.sign_in(phone, input('Enter the code: '))

# # Input CSV file with user details
# input_file = sys.argv[1]
# users = []
# with open(input_file, encoding='UTF-8') as f:
#     rows = csv.reader(f, delimiter=",", lineterminator="\n")
#     next(rows, None)  # Skip the header row
#     for row in rows:
#         user = {
#             'username': row[0],
#             'id': int(row[1]),
#             'access_hash': int(row[2]),
#             'name': row[3]
#         }
#         users.append(user)

# # Fetch the list of groups
# chats = []
# last_date = None
# chunk_size = 200
# groups = []

# result = client(GetDialogsRequest(
#     offset_date=last_date,
#     offset_id=0,
#     offset_peer=InputPeerEmpty(),
#     limit=chunk_size,
#     hash=0
# ))
# chats.extend(result.chats)

# # Append groups to the list
# for chat in chats:
#     try:
#         groups.append(chat)
#     except Exception as e:
#         print(f"Error appending group: {e}")
#         continue

# # Choose a group to add members to
# print('Choose a group to add members:')
# i = 0
# for group in groups:
#     print(f"{i} - {group.title}")
#     i += 1

# g_index = int(input("Enter a Number: "))
# target_group = groups[g_index]

# # Determine whether the group is a supergroup or regular group
# if hasattr(target_group, 'access_hash'):
#     target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)  # For supergroups
#     print(f"Selected group is a supergroup: {target_group.title}")
# else:
#     print(f"Selected group is a regular group: {target_group.title}")
#     print("Cannot add members to regular groups using this method.")
#     sys.exit()

# # Choose whether to add by username or ID
# mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

# n = 0

# # Adding members to the group
# for user in users:
#     n += 1
#     if n % 50 == 0:
#         sleep(900)  # Sleep after every 50 users for 15 minutes to avoid rate-limiting

#     try:
#         print(f"Adding {user['id']} to the group...")

#         # Add by username or ID
#         if mode == 1:
#             if user['username'] == "":
#                 continue
#             user_to_add = client.get_input_entity(user['username'])
#         elif mode == 2:
#             user_to_add = InputPeerUser(user['id'], user['access_hash'])
#         else:
#             print("Invalid mode selected. Exiting.")
#             sys.exit()

#         # Add the user to the supergroup
#         client(InviteToChannelRequest(target_group_entity, [user_to_add]))

#         # Random sleep to avoid hitting Telegram's rate limits
#         print("Waiting for 60-180 Seconds...")
#         time.sleep(random.randrange(60, 180))

#     except PeerFloodError:
#         print("Getting Flood Error from Telegram. Script is stopping now. Please try again later.")
#         break  # Stop the script if flood limit is reached
#     except UserPrivacyRestrictedError:
#         print(f"Privacy settings do not allow adding {user['id']}. Skipping this user.")
#         continue
#     except Exception as e:
#         print(f"Unexpected Error: {e}")
#         traceback.print_exc()
#         continue

# print("Script finished successfully.")


















# from telethon.sync import TelegramClient
# from telethon.tl.functions.channels import GetParticipantRequest
# from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
# from telethon.tl.functions.messages import GetDialogsRequest
# from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
# from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
# from telethon.tl.functions.channels import InviteToChannelRequest
# import sys
# import csv
# import traceback
# import time
# import random
# from time import sleep

# # Your API credentials
# api_id = 26935340
# api_hash = '5b00b55597cc61a30f7e05ae770836f1'
# phone = '+212693360369'

# # Create Telegram client
# client = TelegramClient(phone, api_id, api_hash)

# # Async function to check if the current user is an admin
# async def is_admin(group, user):
#     participant = await client(GetParticipantRequest(group, user))
#     if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
#         return True
#     return False

# # The main function to run the script
# async def main():
#     await client.connect()
#     if not await client.is_user_authorized():
#         await client.send_code_request(phone)
#         await client.sign_in(phone, input('Enter the code: '))

#     # Input CSV file with user details
#     input_file = sys.argv[1]
#     users = []
#     with open(input_file, encoding='UTF-8') as f:
#         rows = csv.reader(f, delimiter=",", lineterminator="\n")
#         next(rows, None)  # Skip the header row
#         for row in rows:
#             user = {
#                 'username': row[0],
#                 'id': int(row[1]),
#                 'access_hash': int(row[2]),
#                 'name': row[3]
#             }
#             users.append(user)

#     # Fetch the list of groups
#     chats = []
#     last_date = None
#     chunk_size = 200
#     groups = []

#     result = await client(GetDialogsRequest(
#         offset_date=last_date,
#         offset_id=0,
#         offset_peer=InputPeerEmpty(),
#         limit=chunk_size,
#         hash=0
#     ))
#     chats.extend(result.chats)

#     # Append groups to the list
#     for chat in chats:
#         try:
#             groups.append(chat)
#         except Exception as e:
#             print(f"Error appending group: {e}")
#             continue

#     # Choose a group to add members to
#     print('Choose a group to add members:')
#     i = 0
#     for group in groups:
#         print(f"{i} - {group.title}")
#         i += 1

#     g_index = int(input("Enter a Number: "))
#     target_group = groups[g_index]

#     # Determine whether the group is a supergroup or regular group
#     if hasattr(target_group, 'access_hash'):
#         target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)  # For supergroups
#         print(f"Selected group is a supergroup: {target_group.title}")
#     else:
#         print(f"Selected group is a regular group: {target_group.title}")
#         print("Cannot add members to regular groups using this method.")
#         sys.exit()

#     # Perform the admin check
#     if not await is_admin(target_group_entity, await client.get_me()):
#         print("You are not an admin in this group. Admin privileges are required to add members.")
#         sys.exit()

#     # Choose whether to add by username or ID
#     mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

#     n = 0

#     # Adding members to the group
#     for user in users:
#         n += 1
#         if n % 50 == 0:
#             sleep(900)  # Sleep after every 50 users for 15 minutes to avoid rate-limiting

#         try:
#             print(f"Adding {user['id']} to the group...")

#             # Add by username or ID
#             if mode == 1:
#                 if user['username'] == "":
#                     continue
#                 user_to_add = await client.get_input_entity(user['username'])
#             elif mode == 2:
#                 user_to_add = InputPeerUser(user['id'], user['access_hash'])
#             else:
#                 print("Invalid mode selected. Exiting.")
#                 sys.exit()

#             # Add the user to the supergroup
#             await client(InviteToChannelRequest(target_group_entity, [user_to_add]))

#             # Random sleep to avoid hitting Telegram's rate limits
#             print("Waiting for 60-180 Seconds...")
#             time.sleep(random.randrange(60, 180))

#         except PeerFloodError:
#             print("Getting Flood Error from Telegram. Script is stopping now. Please try again later.")
#             break  # Stop the script if flood limit is reached
#         except UserPrivacyRestrictedError:
#             print(f"Privacy settings do not allow adding {user['id']}. Skipping this user.")
#             continue
#         except Exception as e:
#             print(f"Unexpected Error: {e}")
#             traceback.print_exc()
#             continue

# # Run the script asynchronously
# with client:
#     client.loop.run_until_complete(main())




from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
from time import sleep

# Your API credentials
api_id = 24477946
api_hash = '5a56a2f0150c524cc355fb2086653868'
phone = '212700737262'

# Create Telegram client
client = TelegramClient(phone, api_id, api_hash)

# The main function to run the script
async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: '))

    # Input CSV file with user details
    input_file = sys.argv[1]
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)  # Skip the header row
        for row in rows:
            user = {
                'username': row[0],
                'id': int(row[1]),
                'access_hash': int(row[2]),
                'name': row[3]
            }
            users.append(user)

    # Fetch the list of groups
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = await client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    # Append groups to the list
    for chat in chats:
        try:
            groups.append(chat)
        except Exception as e:
            print(f"Error appending group: {e}")
            continue

    # Choose a group to add members to
    print('Choose a group to add members:')
    i = 0
    for group in groups:
        print(f"{i} - {group.title}")
        i += 1

    g_index = int(input("Enter a Number: "))
    target_group = groups[g_index]

    # Determine whether the group is a supergroup or regular group
    if hasattr(target_group, 'megagroup') and target_group.megagroup:
        target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)  # For supergroups
        print(f"Selected group is a supergroup: {target_group.title}")
    else:
        print(f"Selected group is a regular group: {target_group.title}")
        print("Cannot add members to regular groups using this method.")
        sys.exit()

    # Choose whether to add by username or ID
    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

    n = 0

    # Adding members to the group
    for user in users:
        n += 1
        if n % 50 == 0:
            sleep(900)  # Sleep after every 50 users for 15 minutes to avoid rate-limiting

        try:
            print(f"Adding {user['id']} to the group...")

            # Add by username or ID
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = await client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                print("Invalid mode selected. Exiting.")
                sys.exit()

            # Add the user to the supergroup
            await client(InviteToChannelRequest(target_group_entity, [user_to_add]))

            # Random sleep to avoid hitting Telegram's rate limits
            print("Waiting for 60-180 Seconds...")
            time.sleep(random.randrange(60, 180))

        except PeerFloodError:
            print("Getting Flood Error from Telegram. Script is stopping now. Please try again later.")
            break  # Stop the script if flood limit is reached
        except UserPrivacyRestrictedError:
            print(f"Privacy settings do not allow adding {user['id']}. Skipping this user.")
            continue
        except Exception as e:
            print(f"Unexpected Error: {e}")
            traceback.print_exc()
            continue

# Run the script asynchronously
with client:
    client.loop.run_until_complete(main())
