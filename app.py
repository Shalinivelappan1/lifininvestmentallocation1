import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Portfolio Simulator", layout="centered")

st.title("📊 How Should You Allocate Your Money?")
st.write("This simulator helps you understand diversification, risk, and crypto allocation.")

st.divider()

st.header("Step 1: Enter Investor Profile")

age = st.slider("Age", 20, 60, 30)
corpus = st.number_input("Total current investments (₹)", value=300000, step=50000)
sip = st.number_input("Monthly investment/SIP (₹)", value=10000, step=1000)
risk = st.selectbox("Risk appetite", ["Low", "Moderate", "High"])
years = st.slider("Investment horizon (years)", 3, 25, 10)

st.info(
"""
💡 **Discussion prompt for class:**  
- Younger investors can take more risk. Why?  
- What happens if someone needs money in 3 years?  
"""
)

st.divider()

st.header("Step 2: Recommended Allocation")

# Allocation logic
if risk == "Low":
    equity = 45
    debt = 45
    gold = 7
    crypto = 3

elif risk == "Moderate":
    equity = 60
    debt = 25
    gold = 8
    crypto = 7

else:
    equity = 70
    debt = 15
    gold = 5
    crypto = 10

eq_amt = corpus * equity/100
debt_amt = corpus * debt/100
gold_amt = corpus * gold/100
crypto_amt = corpus * crypto/100

col1, col2 = st.columns(2)

with col1:
    st.metric("Equity (growth engine)", f"₹{eq_amt:,.0f}", f"{equity}%")
    st.metric("Debt (stability)", f"₹{debt_amt:,.0f}", f"{debt}%")

with col2:
    st.metric("Gold (hedge)", f"₹{gold_amt:,.0f}", f"{gold}%")
    st.metric("Crypto (high risk)", f"₹{crypto_amt:,.0f}", f"{crypto}%")

st.info(
"""
📚 **Concept:**  
- Equity = long-term growth  
- Debt = stability  
- Gold = hedge against uncertainty  
- Crypto = highly volatile satellite asset  

Most portfolios keep crypto below 10%.
"""
)

st.divider()

st.header("Visual Allocation")

labels = ['Equity','Debt','Gold','Crypto']
sizes = [equity, debt, gold, crypto]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.0f%%')
ax.axis('equal')
st.pyplot(fig)

st.divider()

st.header("Step 3: Monthly SIP Split")

st.write(f"Equity SIP: ₹{sip*0.6:,.0f}")
st.write(f"Debt SIP: ₹{sip*0.25:,.0f}")
st.write(f"Gold SIP: ₹{sip*0.08:,.0f}")
st.write(f"Crypto SIP: ₹{sip*0.07:,.0f}")

st.info(
"""
💡 **Class question:**  
If markets crash, which SIP should you pause first?  
Why is crypto usually the smallest allocation?
"""
)

st.divider()

st.header("Step 4: Long-Term Projection")

equity_return = 0.12
debt_return = 0.06
gold_return = 0.07
crypto_return = 0.15

future_value = (
    eq_amt*(1+equity_return)**years +
    debt_amt*(1+debt_return)**years +
    gold_amt*(1+gold_return)**years +
    crypto_amt*(1+crypto_return)**years
)

st.success(f"Estimated portfolio value in {years} years: ₹{future_value:,.0f}")

st.warning(
"""
⚠️ **Important teaching point:**  
Crypto returns are uncertain and highly volatile.  
This projection assumes average returns — real outcomes can vary widely.
"""
)

st.divider()

st.header("Step 5: Rebalancing")

st.write(
"""
Once a year:
- If crypto becomes >10% → reduce  
- Move profits to equity or debt  
- Rebalancing controls risk  

**Key lesson:** Asset allocation matters more than stock picking.
"""
)
