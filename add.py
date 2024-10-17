# from telethon.sync import TelegramClient
# from telethon.tl.functions.messages import GetDialogsRequest
# from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
# from telethon.errors import (
#     PeerFloodError,
#     UserPrivacyRestrictedError,
#     FloodWaitError,
# )
# from telethon.tl.functions.channels import InviteToChannelRequest
# import sys
# import csv
# import time
# import random
# import traceback

# # Replace these with your API credentials
# api_id = 26935340  # Replace with your API ID
# api_hash = '5b00b55597cc61a30f7e05ae770836f1'  # Replace with your API Hash
# phone = '+212693360369'  # Replace with your phone number

# # Initialize Telegram client
# client = TelegramClient(phone, api_id, api_hash)

# # Main function to handle the logic
# async def main():
#     await client.connect()
#     if not await client.is_user_authorized():
#         await client.send_code_request(phone)
#         await client.sign_in(phone, input("Enter the code: "))

#     # Load user data from the CSV file
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
#                 'name': row[3],
#             }
#             users.append(user)

#     # Fetch the list of available groups
#     chats = []
#     last_date = None
#     chunk_size = 200
#     groups = []

#     result = await client(GetDialogsRequest(
#         offset_date=last_date,
#         offset_id=0,
#         offset_peer=InputPeerEmpty(),
#         limit=chunk_size,
#         hash=0,
#     ))
#     chats.extend(result.chats)

#     # Let the user choose a group to add members to
#     for i, group in enumerate(chats):
#         print(f"{i} - {group.title}")

#     g_index = int(input("Enter the number of the group: "))
#     target_group = chats[g_index]

#     # Check if the group is a supergroup
#     if hasattr(target_group, 'megagroup') and target_group.megagroup:
#         target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
#         print(f"Selected group: {target_group.title}")
#     else:
#         print("Cannot add members to regular groups. Exiting.")
#         sys.exit()

#     # Choose the mode of adding members
#     mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

#     n = 0  # Counter for tracking invites

#     # Adding members to the group with retry logic
#     for user in users:
#         n += 1
#         retry_attempts = 0  # Reset retry attempts for each user

#         while retry_attempts < 5:  # Limit to 5 retries
#             try:
#                 print(f"Adding {user['id']} ({user['username']}) to the group...")

#                 # Add the user by username or ID
#                 if mode == 1:
#                     if not user['username']:
#                         print(f"Skipping user {user['id']} due to missing username.")
#                         break
#                     user_to_add = await client.get_input_entity(user['username'])
#                 elif mode == 2:
#                     user_to_add = InputPeerUser(user['id'], user['access_hash'])
#                 else:
#                     print("Invalid mode selected. Exiting.")
#                     sys.exit()

#                 # Invite the user to the supergroup
#                 await client(InviteToChannelRequest(target_group_entity, [user_to_add]))

#                 # Random sleep to avoid hitting rate limits
#                 sleep_time = random.randint(60, 180)
#                 print(f"Sleeping for {sleep_time} seconds...")
#                 time.sleep(sleep_time)

#                 break  # Exit retry loop if the invitation is successful

#             except PeerFloodError:
#                 print("Telegram is limiting your actions. Retrying after 15 minutes...")
#                 time.sleep(900)  # Wait 15 minutes and retry

#             except FloodWaitError as e:
#                 if e.seconds > 3600:  # If wait time is more than 1 hour
#                     print(f"FloodWaitError: Must wait {e.seconds / 3600:.2f} hours.")
#                     print("Skipping this user to avoid excessive wait.")
#                     break  # Skip this user and move to the next

#                 print(f"FloodWaitError: Waiting for {e.seconds} seconds...")
#                 time.sleep(e.seconds)  # Wait for the specified time and retry

#             except UserPrivacyRestrictedError:
#                 print(f"User {user['id']} has privacy settings that block invites.")
#                 break  # Skip this user and move to the next

#             except Exception as e:
#                 print(f"Unexpected Error: {e}")
#                 traceback.print_exc()
#                 break  # Skip this user on unexpected errors

#             retry_attempts += 1  # Increment retry attempts

#         # Pause every 50 users to avoid hitting rate limits
#         if n % 50 == 0:
#             print("Pausing for 15 minutes to avoid hitting rate limits...")
#             time.sleep(900)  # Pause for 15 minutes

# # Run the script asynchronously
# with client:
#     client.loop.run_until_complete(main())














import csv
import json
import asyncio
import traceback
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError, UserPrivacyRestrictedError, UserIdInvalidError, ChannelInvalidError
)
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon.tl.functions.channels import InviteToChannelRequest

# Your Telegram account credentials
accounts = [
    {'api_id': 123456, 'api_hash': 'your_api_hash1', 'phone': '+212700737262'},
    {'api_id': 654321, 'api_hash': 'your_api_hash2', 'phone': '+212693360369'}
]

# Load users from CSV
def load_users_from_csv(filename='members.csv'):
    users = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if row['user id'] and row['access hash']:
                    users.append({
                        'id': int(row['user id']),
                        'access_hash': int(row['access hash']),
                        'username': row.get('username', ''),
                        'name': row.get('name', '')
                    })
            except ValueError as e:
                print(f"Skipping invalid row: {row}. Error: {e}")
    return users

# Load or initialize progress tracking
def load_progress(filename='progress.json'):
    try:
        with open(filename, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

# Save progress to a file
def save_progress(processed_users, filename='progress.json'):
    with open(filename, 'w') as f:
        json.dump(list(processed_users), f)

# Login to all accounts
async def login_accounts():
    clients = []
    for account in accounts:
        client = TelegramClient(account['phone'], account['api_id'], account['api_hash'])
        await client.connect()
        if not await client.is_user_authorized():
            print(f"Login required for {account['phone']}")
            await client.send_code_request(account['phone'])
            code = input(f"Enter the code for {account['phone']}: ")
            await client.sign_in(account['phone'], code)
        clients.append(client)
    return clients

# Get group entity by name
async def get_group_entity(client, group_name):
    async for dialog in client.iter_dialogs():
        if dialog.name == group_name:
            return InputPeerChannel(dialog.entity.id, dialog.entity.access_hash)
    raise ValueError(f"Group '{group_name}' not found.")

# Invite users to a group
async def invite_users(client, group, users, processed_users):
    for user in users:
        if user['id'] in processed_users:
            print(f"Skipping {user['id']} (already processed).")
            continue

        try:
            print(f"Adding {user['id']} ({user.get('username', None)}) to the group...")
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
            await client(InviteToChannelRequest(group, [user_to_add]))
            print("User added successfully.")
            processed_users.add(user['id'])
            save_progress(processed_users)
            await asyncio.sleep(30)  # Avoid rate limits

        except UserIdInvalidError:
            print(f"Invalid user ID or access hash for user {user['id']}. Skipping...")
            processed_users.add(user['id'])
            save_progress(processed_users)

        except FloodWaitError as e:
            print(f"Flood wait error: Must wait {e.seconds} seconds. Switching accounts...")
            return False  # Indicate flood limit hit

        except UserPrivacyRestrictedError:
            print(f"Privacy settings prevent adding user {user['id']}. Skipping...")
            processed_users.add(user['id'])
            save_progress(processed_users)

        except ChannelInvalidError:
            print("Invalid channel. Re-fetching the group...")
            return False  # Indicate channel issue

        except Exception as e:
            print(f"Unexpected error: {e}")
            traceback.print_exc()

    return True  # All users processed

# Main function
async def main():
    users = load_users_from_csv()
    processed_users = load_progress()
    clients = await login_accounts()
    group_name = input("Enter the exact group name: ")

    while True:
        for i, client in enumerate(clients):
            print(f"Using account {i + 1}/{len(clients)}")
            try:
                group = await get_group_entity(client, group_name)
                success = await invite_users(client, group, users, processed_users)
                if success:
                    print("All users added successfully.")
                    return  # Exit if all users are added

            except Exception as e:
                print(f"Error with account {accounts[i]['phone']}: {e}")

            finally:
                await client.disconnect()

        print("All accounts hit limits. Sleeping for 1 hour...")
        await asyncio.sleep(3600)  # Sleep before retrying

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
