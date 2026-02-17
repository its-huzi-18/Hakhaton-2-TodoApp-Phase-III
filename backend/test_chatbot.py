"""Test chatbot endpoint"""
import asyncio
import httpx

async def test_chat():
    base_url = "http://localhost:8000"
    
    # Step 1: Register a new user
    print("1. Registering new user...")
    async with httpx.AsyncClient() as client:
        reg_response = await client.post(
            f"{base_url}/api/auth/register",
            json={"email": "chatbot_test@example.com", "password": "testpassword123"}
        )
        print(f"   Register status: {reg_response.status_code}")
        
        if reg_response.status_code == 201:
            user_data = reg_response.json()
            print(f"   User ID: {user_data.get('id')}")
            print(f"   User email: {user_data.get('email')}")
            user_id = str(user_data.get('id'))
        else:
            # Try login if user exists
            print("   User exists, logging in...")
            login_response = await client.post(
                f"{base_url}/api/auth/login",
                json={"email": "chatbot_test@example.com", "password": "testpassword123"}
            )
            if login_response.status_code == 200:
                token_data = login_response.json()
                user_id = token_data['user']['id']
                print(f"   Logged in! User ID: {user_id}")
            else:
                print(f"   Login failed: {login_response.text}")
                return
    
    # Step 2: Test chat endpoint
    print("\n2. Testing chat endpoint...")
    print(f"   Sending message to: {base_url}/api/{user_id}/chat")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        chat_response = await client.post(
            f"{base_url}/api/{user_id}/chat",
            json={"content": "Add a task to test the chatbot"}
        )
        print(f"   Chat status: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"   Response: {response_data.get('content', response_data.get('response', 'N/A'))[:100]}")
            print("\n✅ Chatbot is working!")
        else:
            print(f"   Error: {chat_response.text}")
            print("\n❌ Chatbot returned an error")

if __name__ == "__main__":
    asyncio.run(test_chat())
