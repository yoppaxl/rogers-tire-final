
import streamlit as st
import pandas as pd

# Load inventory
df = pd.read_csv("rogers_tire_inventory.csv")

st.set_page_config(page_title="Rogers Tire Inventory", layout="centered")
st.title("Rogers Tire Inventory")

# --- Search Section ---
st.subheader("🔍 Search Tires")
search = st.text_input("Enter Tire Size (e.g., 235/65/17)").strip()
if search:
    result = df[df["Tire Size"].str.replace(" ", "").str.lower() == search.replace(" ", "").lower()]
    if not result.empty:
        for _, row in result.iterrows():
            st.success(f"{row['Tire Size']} ({row['Rim Size']}): {row['Quantity']} in stock")
    else:
        st.warning("Tire not found.")

# --- Full Inventory Section ---
st.subheader("📋 View All Tires")
rim_filter = st.selectbox("Filter by Rim Size", ["All"] + sorted(df["Rim Size"].unique()))
if rim_filter != "All":
    view_df = df[df["Rim Size"] == rim_filter]
else:
    view_df = df
st.dataframe(view_df)

# --- Add Tire Section ---
st.subheader("➕ Add Tire")
new_size = st.text_input("Tire Size (e.g., 225/65/17)", key="add_size")
new_rim = st.text_input("Rim Size (e.g., 17's)", key="add_rim")
new_qty = st.number_input("Quantity", min_value=1, step=1, key="add_qty")
if st.button("Add Tire"):
    mask = (df["Tire Size"].str.lower() == new_size.lower()) & (df["Rim Size"].str.lower() == new_rim.lower())
    if df[mask].empty:
        df = pd.concat([df, pd.DataFrame([{
            "Tire Size": new_size, "Rim Size": new_rim, "Quantity": new_qty
        }])], ignore_index=True)
        st.success(f"Added {new_size} ({new_rim}) x{new_qty}")
    else:
        df.loc[mask, "Quantity"] += new_qty
        st.success(f"Updated quantity for {new_size} ({new_rim})")

# --- Remove Tire Section ---
st.subheader("➖ Remove Tire")
rm_size = st.text_input("Tire Size to Remove", key="rm_size")
rm_rim = st.text_input("Rim Size", key="rm_rim")
rm_qty = st.number_input("Quantity to Remove", min_value=1, step=1, key="rm_qty")
if st.button("Remove Tire"):
    mask = (df["Tire Size"].str.lower() == rm_size.lower()) & (df["Rim Size"].str.lower() == rm_rim.lower())
    if df[mask].empty:
        st.error("Tire not found.")
    else:
        current = df.loc[mask, "Quantity"].values[0]
        if current <= rm_qty:
            df = df[~mask]
            st.success(f"Removed all of {rm_size} ({rm_rim})")
        else:
            df.loc[mask, "Quantity"] -= rm_qty
            st.success(f"Removed {rm_qty} of {rm_size} ({rm_rim})")

# --- Download Option ---
st.subheader("⬇️ Download Inventory")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "tire_inventory.csv", "text/csv")
