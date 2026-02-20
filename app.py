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

st.divider()
st.header("💥 Behaviour Simulator")

crash_button = st.button("Simulate Market Crash")
panic_button = st.button("😱 Panic Sell After Crash")
rebalance_toggle = st.toggle("Rebalance yearly", value=True)

# Base returns
st.divider()
st.header("Assumed Annual Returns (student inputs)")

st.write("Students can change return assumptions to see impact on outcomes.")

equity_return = st.slider(
    "Equity return (%)", 
    min_value=-20, max_value=20, value=12
) / 100

debt_return = st.slider(
    "Debt return (%)", 
    min_value=0, max_value=12, value=6
) / 100

gold_return = st.slider(
    "Gold return (%)", 
    min_value=0, max_value=15, value=7
) / 100

crypto_return = st.slider(
    "Crypto return (%)", 
    min_value=-50, max_value=40, value=15
) / 100

st.info("""
Discussion prompts:
• What happens if equity returns are lower than expected?  
• What if crypto returns are negative?  
• Are long-term assumptions realistic?
""")

# Apply crash
if crash_button:
    st.error("Market crash simulated: Equity -30%, Crypto -50%")
    equity_return = -0.30
    crypto_return = -0.50

# Initial values
eq = eq_amt
debt_v = debt_amt
gold_v = gold_amt
crypto_v = crypto_amt

initial_total = eq + debt_v + gold_v + crypto_v
values = []
recovery_year = None

for year in range(1, years+1):

    # Crash happens in year 1
    if year == 1 and crash_button:
        eq *= (1 + equity_return)
        crypto_v *= (1 + crypto_return)

        if panic_button:
            st.warning("Investor panics and shifts risky assets to debt!")
            debt_v += eq + crypto_v
            eq = 0
            crypto_v = 0

    # Normal growth thereafter
    eq *= 1.12
    debt_v *= 1.06
    gold_v *= 1.07
    crypto_v *= 1.15

    total = eq + debt_v + gold_v + crypto_v
    values.append(total)

    if total >= initial_total and recovery_year is None:
        recovery_year = year

    # Rebalancing
    if rebalance_toggle:
        eq = total * equity/100
        debt_v = total * debt/100
        gold_v = total * gold/100
        crypto_v = total * crypto/100

final_value = values[-1]

st.subheader("📈 Outcome After Simulation")
st.success(f"Final value after {years} years: ₹{final_value:,.0f}")

if recovery_year:
    st.info(f"Portfolio recovered to original value in {recovery_year} years")
else:
    st.warning("Portfolio did not recover within selected horizon")

# Chart
fig2, ax2 = plt.subplots()
ax2.plot(range(1, years+1), values)
ax2.set_xlabel("Years")
ax2.set_ylabel("Portfolio Value")
st.pyplot(fig2)

st.info("""
Class discussion prompts:
• What did panic selling do to recovery time?
• Did rebalancing help?
• Who survives a crash better?
""")
