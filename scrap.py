# from telethon.sync import TelegramClient
# from telethon.tl.functions.messages import GetDialogsRequest
# from telethon.tl.types import InputPeerEmpty
# import csv

# api_id =  26935340  
# api_hash = '5b00b55597cc61a30f7e05ae770836f1'  
# phone = '+212693360369' 

# # Initialize Telegram client
# client = TelegramClient(phone, api_id, api_hash)

# client.connect()
# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     client.sign_in(phone, input('Enter the code: '))

# # Fetch available groups
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

# # Filter groups to list only megagroups (supergroups)
# for chat in chats:
#     try:
#         groups.append(chat)
#     except:
#         continue

# print('Choose a group to scrape members from:')
# for i, group in enumerate(groups):
#     print(f"{i} - {group.title}")

# g_index = int(input("Enter a Number: "))
# target_group = groups[g_index]

# print(f'Fetching members from {target_group.title}...')

# all_participants = client.get_participants(target_group, aggressive=True)

# # Save the members' data in a CSV file
# output_file = "members.csv"
# with open(output_file, "w", encoding='UTF-8', newline='') as f:
#     writer = csv.writer(f, delimiter=",")
#     writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])

#     # Process each participant and write to the CSV
#     for user in all_participants:
#         username = user.username if user.username else ""
#         first_name = user.first_name if user.first_name else ""
#         last_name = user.last_name if user.last_name else ""
#         name = f"{first_name} {last_name}".strip()

#         # Ensure user.id and user.access_hash are valid before writing to the CSV
#         if user.id and user.access_hash:
#             writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])

# print(f'Members scraped successfully and saved to {output_file}.')


from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

# Replace these with your API credentials
api_id = 26935340  # Replace with your API ID
api_hash = '5b00b55597cc61a30f7e05ae770836f1'  # Replace with your API Hash
phone = '+212693360369'  # Replace with your phone number

# Initialize the Telegram client
client = TelegramClient(phone, api_id, api_hash)

# Connect to Telegram
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

# Fetch available groups
chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

# Filter only megagroups (supergroups)
for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except Exception as e:
        print(f"Error processing chat: {e}")
        continue

# Let the user choose the group to scrape members from
print('Choose a group to scrape members from:')
for i, group in enumerate(groups):
    print(f"{i} - {group.title}")

g_index = int(input("Enter the number of the group: "))
target_group = groups[g_index]

print(f'Fetching members from {target_group.title}...')

# Fetch all participants from the selected group
all_participants = client.get_participants(target_group, aggressive=True)

# Save the scraped members into a CSV file
output_file = 'members.csv'
with open(output_file, 'w', encoding='UTF-8', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    # Write the CSV header
    writer.writerow(['username', 'user id', 'access hash', 'name'])

    # Write each participant's data into the CSV
    for user in all_participants:
        username = user.username if user.username else ""
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        name = f"{first_name} {last_name}".strip()

        # Ensure that both user id and access hash are valid
        if user.id and user.access_hash:
            writer.writerow([username, user.id, user.access_hash, name])

print(f'Members scraped successfully and saved to {output_file}.')