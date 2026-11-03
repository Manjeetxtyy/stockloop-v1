import streamlit as st
import pandas as pd
from stockloop.data import SITES, inventory
from stockloop.logic import match_inventory, predict
from stockloop.workflow import Approval, decide

st.set_page_config(page_title="StockLoop V1", page_icon="🏥", layout="wide")
st.title("StockLoop")
st.caption("V1 prototype · simulated data and simulated AI-style predictions only")
st.warning("Not NHS-endorsed. No validated model accuracy or real savings are claimed. Do not use for clinical or operational authorisation.")

if "inventory" not in st.session_state: st.session_state.inventory = inventory()
if "approvals" not in st.session_state: st.session_state.approvals = []
df = st.session_state.inventory

page = st.sidebar.radio("Go to", ["Dashboard", "Inventory", "AI prediction", "Smart matching", "Approvals"])
st.sidebar.info("All sites, stock records, recommendations and outcomes are fictional simulations.")

if page == "Dashboard":
    st.header("Dashboard")
    cols = st.columns(3)
    for col, site in zip(cols, SITES):
        subset = df[df.site_id == site["id"]]
        with col:
            st.subheader(site["name"]); st.metric("Stock lines", len(subset)); st.metric("Units", int(subset.quantity.sum())); st.caption(f"Region: {site['region']} · capacity: {site['capacity']} (simulated)")
    st.subheader("Simulated network snapshot")
    st.dataframe(df.groupby(["site", "category"], as_index=False).agg(items=("item", "count"), units=("quantity", "sum")), use_container_width=True, hide_index=True)

elif page == "Inventory":
    st.header("Searchable inventory")
    category = st.selectbox("Category", ["All", "Medicine", "Consumable"]); query = st.text_input("Search item or site")
    view = df if category == "All" else df[df.category == category]
    if query: view = view[view.item.str.contains(query, case=False) | view.site.str.contains(query, case=False)]
    st.caption(f"Showing {len(view)} simulated records · medicine and consumable stock checks are kept separate.")
    st.dataframe(view[["site", "item", "category", "quantity", "weekly_demand", "expiry", "storage", "batch", "traceability"]], use_container_width=True, hide_index=True)

elif page == "AI prediction":
    st.header("AI-style expiry and demand prediction")
    st.caption("Transparent rules-based simulation for demonstration; this is not a validated predictive model.")
    item = st.selectbox("Item", sorted(df.item.unique())); site = st.selectbox("Site", [s["name"] for s in SITES])
    row = df[(df.item == item) & (df.site == site)].iloc[0]; result = predict(row)
    st.metric("Simulated risk", result["risk"]); st.metric("Estimated cover", f"{result['cover_weeks']} week(s)"); st.write(result["explanation"])
    st.dataframe(pd.DataFrame([{"Input": k, "Value": str(row[k])} for k in ["category", "quantity", "weekly_demand", "expiry", "storage"]]), hide_index=True)

elif page == "Smart matching":
    st.header("Smart matching")
    item = st.selectbox("Item", sorted(df.item.unique())); source = st.selectbox("Source site", [s["name"] for s in SITES]); target = st.selectbox("Destination site", [s["name"] for s in SITES if s["name"] != source])
    recommendations = match_inventory(df, item, source, target)
    if recommendations:
        rec = recommendations[0]; st.write(rec["reason"]); st.metric("Suggested quantity", rec["suggested_quantity"])
        if rec["checks"]:
            st.write("Medicine transfer eligibility checks"); st.dataframe(pd.DataFrame([{"Check": k.title(), "Passed": v} for k, v in rec["checks"].items()]), hide_index=True)
            st.info("Medicine transfers are never automatically authorised. Use Request review in Approvals.")
        if st.button("Create approval request"):
            st.session_state.approvals.append(Approval(item, source, target, rec["suggested_quantity"], df[df.item == item].iloc[0].category)); st.success("Approval request created.")
    else: st.info("No simulated match found for this combination.")

else:
    st.header("Approval workflow")
    if not st.session_state.approvals: st.info("No requests yet. Create one from Smart matching.")
    for i, approval in enumerate(st.session_state.approvals):
        with st.container(border=True):
            st.write(f"**{approval.item}** · {approval.source} → {approval.target} · {approval.quantity} units · {approval.category} · **{approval.status}**")
            note = st.text_input("Decision note", key=f"note-{i}")
            c1, c2, c3 = st.columns(3)
            for col, action in zip((c1, c2, c3), ("Approve", "Reject", "Request review")):
                if col.button(action, key=f"{action}-{i}"):
                    try: decide(approval, action, note); st.rerun()
                    except ValueError as exc: st.error(str(exc))

