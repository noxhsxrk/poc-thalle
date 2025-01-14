import requests
import pandas as pd
from datetime import datetime
import os
import random
import dotenv

dotenv.load_dotenv()

def log_chat_interaction(user_message, system_message, response_data):
    excel_file = 'chat_logs.xlsx'
    
    cleaned_response = response_data['message']['content'].replace('\\n', '\n').strip()
    
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_prompt': user_message,
        'system_prompt': system_message,
        'response': cleaned_response,
        'response time (s)': response_data['total_duration'] / 1000000000
    }

    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([log_entry])
    
    df.style.set_properties(**{'background-color': '#f2f2f2'}, subset=pd.IndexSlice[1::2, :]).to_excel(excel_file, index=False)

def chat_with_thalle(user_message_file="user_message.txt", system_message_file="system_message.txt"):
    endpoint = os.getenv("ENDPOINT")
    url = endpoint+"/api/chat"
    
    print("\n📂 Reading system message...")
    try:
        with open(system_message_file, 'r', encoding='utf-8') as f:
            system_messages = f.read().strip().split('\n')
        print(f"✅ Loaded {len(system_messages)} system messages successfully")
    except FileNotFoundError:
        print(f"❌ System message file {system_message_file} not found")
        return None

    print("\n📂 Reading user messages...")
    try:
        with open(user_message_file, 'r', encoding='utf-8') as f:
            user_messages = [msg.strip() for msg in f.readlines() if msg.strip()]
        print(f"✅ Loaded {len(user_messages)} user messages")
    except FileNotFoundError:
        print(f"❌ User message file {user_message_file} not found")
        return None

    responses = []
    total_messages = len(user_messages)
    
    print("\n🚀 Starting API calls...")
    for idx, user_message in enumerate(user_messages, 1):
        print(f"\n[{idx}/{total_messages}] Processing: {user_message[:50]}{'...' if len(user_message) > 50 else ''}")
        
        system_prompt_number = random.randint(0, len(system_messages) - 1)
        selected_system_message = system_messages[system_prompt_number]
        
        use_empty_system = random.random() < 0.2
        if use_empty_system:
            selected_system_message = ""
            print(f"   🎲 Using empty system prompt")
        else:
            print(f"   🎲 Using system prompt #{selected_system_message[:50]}{'...' if len(selected_system_message) > 50 else ''}")
        
        payload = {
            "model": "hf.co/KBTG-Labs/THaLLE-0.1-7B-fa-GGUF:F16",
            "messages": [
                {
                    "role": "system",
                    "content": selected_system_message
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "stream": False
        }

        try:
            print(f"   ⏳ Calling API...")
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            print(f"   💾 Logging interaction...")
            log_chat_interaction(user_message, selected_system_message, response_data)
            responses.append(response_data)
            print(f"   ✅ Completed [{idx}/{total_messages}]")
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error making API call: {e}")
            error_entry = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'user_prompt': user_message,
                'system_prompt': selected_system_message,
                'response': f"ERROR: {str(e)}",
                'response time (s)': None
            }
            excel_file = 'chat_logs.xlsx'
            if os.path.exists(excel_file):
                df = pd.read_excel(excel_file)
                df = pd.concat([df, pd.DataFrame([error_entry])], ignore_index=True)
            else:
                df = pd.DataFrame([error_entry])
            df.style.set_properties(**{'background-color': '#f2f2f2'}, subset=pd.IndexSlice[1::2, :]).to_excel(excel_file, index=False)
            continue
    
    print(f"\n✨ All done! Processed {len(responses)}/{total_messages} messages successfully")
    return responses

if __name__ == "__main__":
    chat_with_thalle()
