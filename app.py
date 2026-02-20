import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Behavioural Finance Lab", layout="centered")

st.title("🧠 Behavioural Finance Simulator")
st.write("See how panic, crashes, and rebalancing affect long-term wealth.")

# -------- INPUTS ----------
corpus = st.number_input("Initial portfolio (₹)", value=500000, step=50000)
sip = st.number_input("Monthly SIP (₹)", value=10000, step=1000)
years = st.slider("Investment horizon (years)", 3, 25, 10)

strategy = st.radio(
    "Base allocation:",
    ["Balanced", "All Equity", "All Crypto"]
)

rebalance = st.toggle("Rebalance annually", True)
continue_sip = st.toggle("Continue SIP during crash", True)

# -------- ALLOCATION ----------
if strategy == "Balanced":
    equity, debt, gold, crypto = 60, 25, 8, 7
elif strategy == "All Equity":
    equity, debt, gold, crypto = 100, 0, 0, 0
else:
    equity, debt, gold, crypto = 0, 0, 0, 100

# -------- INITIAL ----------
eq0 = corpus * equity/100
debt0 = corpus * debt/100
gold0 = corpus * gold/100
crypto0 = corpus * crypto/100

# -------- BUTTONS ----------
st.divider()
st.header("Market Event")

crash = st.button("💥 Simulate Crash (Year 1)")
panic = st.button("😱 Panic Sell After Crash")

# -------- RETURNS ----------
eq_r = 0.12
debt_r = 0.06
gold_r = 0.07
crypto_r = 0.15

if crash:
    eq_r = -0.30
    crypto_r = -0.55

# -------- FUNCTION ----------
def simulate(panic_sell=False):
    eq = eq0
    debt = debt0
    gold = gold0
    crypto = crypto0

    values = []
    recovered = None

    for y in range(1, years+1):

        # crash in year 1
        if y == 1 and crash:
            eq *= (1 + eq_r)
            crypto *= (1 + crypto_r)

            if panic_sell:
                debt += eq + crypto
                eq = 0
                crypto = 0

        # normal growth
        eq *= 1.12
        debt *= 1.06
        gold *= 1.07
        crypto *= 1.15

        # SIP
        if continue_sip:
            eq += sip * 0.6 * 12
            debt += sip * 0.25 * 12
            gold += sip * 0.08 * 12
            crypto += sip * 0.07 * 12

        total = eq + debt + gold + crypto
        values.append(total)

        if total >= corpus and recovered is None:
            recovered = y

        if rebalance:
            eq = total * equity/100
            debt = total * debt/100
            gold = total * gold/100
            crypto = total * crypto/100

    return values, recovered

# -------- RUN TWO SCENARIOS ----------
values_calm, rec_calm = simulate(False)
values_panic, rec_panic = simulate(True)

# -------- RESULTS ----------
st.divider()
st.header("Outcome Comparison")

final_calm = values_calm[-1]
final_panic = values_panic[-1]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stayed Invested")
    st.metric("Final Value", f"₹{final_calm:,.0f}")
    if rec_calm:
        st.write(f"Recovery: {rec_calm} yrs")

with col2:
    st.subheader("Panic Sold")
    st.metric("Final Value", f"₹{final_panic:,.0f}")
    if rec_panic:
        st.write(f"Recovery: {rec_panic} yrs")

# -------- GRAPH ----------
st.subheader("Wealth Path")

fig, ax = plt.subplots()
ax.plot(values_calm, label="Stayed Invested")
ax.plot(values_panic, label="Panic Sold")
ax.legend()
ax.set_xlabel("Years")
ax.set_ylabel("Portfolio Value")
st.pyplot(fig)

# -------- TEACHING BOX ----------
st.info("""
Class discussion:
• Who recovered faster?
• Did panic selling lock losses?
• Does rebalancing help recovery?
• Should SIP stop during crashes?
""")
