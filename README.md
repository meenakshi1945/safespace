# SafeSpace - Encrypted Chat Application

A peer-to-peer encrypted chat application that ensures confidentiality of user messages using AES encryption.

## Tech Stack
- Python
- Tkinter (GUI)
- PyCryptodome (AES Encryption)
- SQLite (Database)
- AES-128 Encryption

## Features
- Real-time encrypted messaging
- AES-128 bit encryption
- Message history storage
- User-friendly GUI
- Secure key management

## How It Works
1. Messages are encrypted using AES-128 before sending
2. Encrypted messages are stored in the database
3. Only users with the encryption key can decrypt and read messages
4. Real-time chat interface with encryption indicators

## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt