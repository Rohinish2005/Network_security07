import hashlib
import os
import time

USER_DATABASE = {
    "rohinish_sharma": "my_super_secret_password"
}


class Server:
    def __init__(self):
        
        self.challenges = {}

    def generate_challenge(self, username):
        """Generates a unique, one-time challenge for a user."""
        if username not in USER_DATABASE:
            return None, "User not found."
        
        
        nonce = os.urandom(16).hex()
        timestamp = str(int(time.time()))
        
        
        user_salt = hashlib.sha256(username.encode()).hexdigest()
        challenge = f"{nonce}_{timestamp}_{user_salt}"
        
        
        self.challenges[username] = {
            "value": challenge,
            "expiry": time.time() + 60  
        }
        print(f"Server: Issued challenge for '{username}': {challenge[:10]}...")
        return challenge, None

    def verify_response(self, username, challenge, response):
        """Verifies the client's response against the expected hash."""
        if username not in self.challenges:
            return False, "No active challenge for this user."

        stored_challenge = self.challenges[username]
        
        
        if challenge != stored_challenge["value"] or time.time() > stored_challenge["expiry"]:
            
            return False, "Invalid or expired challenge. Possible replay attack detected."
            
        
        secret_key = USER_DATABASE.get(username)
        if not secret_key:
            return False, "User not found."
            
        
        expected_response = hashlib.sha256((challenge + secret_key).encode()).hexdigest()
        
        
        del self.challenges[username]
        
        if response == expected_response:
            return True, "Authentication successful."
        else:
            return False, "Authentication failed. Invalid response."


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_response(self, challenge):
        """Combines the challenge and the secret key (password) to create a hash response."""
        return hashlib.sha256((challenge + self.password).encode()).hexdigest()


if __name__ == "__main__":
    server = Server()
    print("--- 1. Simulating Successful User Authentication ---")
    
    
    client = Client("rohinish_sharma", "my_super_secret_password")
    
    
    challenge_1, msg = server.generate_challenge(client.username)
    if not challenge_1:
       print(f"Server Error: {msg}")
    else:
        
        response_1 = client.create_response(challenge_1)
        print(f"Client: Generated response for challenge {challenge_1[:10]}...: {response_1[:10]}...")

        
        is_authenticated, result_msg = server.verify_response(client.username, challenge_1, response_1)
        print(f"Server: {result_msg}")
        if is_authenticated:
            print(f"Authentication was successful. User '{client.username}' is logged in.")
            
    print("\n" + "="*50 + "\n")
    print("--- 2. Simulating a Replay Attack ---")
    
    
    intercepted_response = response_1
    print(f"Attacker: Intercepted a valid response: {intercepted_response[:10]}...")

    
    challenge_2, msg = server.generate_challenge("rohinish_sharma")
    
    
    print("Attacker: Replaying the old response to the new challenge...")
    is_authenticated, result_msg = server.verify_response("rohinish_sharma", challenge_2, intercepted_response)
    
    
    print(f"Server: {result_msg}")
    if not is_authenticated:
        print("Replay attack was successfully blocked! The old response is invalid for the new challenge.")
