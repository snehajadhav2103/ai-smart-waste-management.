import pandas as pd
import streamlit as st

st.set_page_config(page_title="Smart Waste Management", page_icon="♻️", layout="wide")
st.title("Smart Waste Management Dashboard")
st.caption("Explore waste collection data and review simple sorting guidance.")

SAMPLE = pd.DataFrame({
    "Date": pd.to_datetime(["2026-01-05","2026-01-12","2026-01-19","2026-01-26","2026-02-02","2026-02-09","2026-02-16","2026-02-23"]),
    "Area": ["North","South","East","West","North","South","East","West"],
    "Waste Type": ["Organic","Plastic","Paper","Metal","Plastic","Organic","Metal","Paper"],
    "Weight (kg)": [120, 75, 48, 32, 82, 135, 38, 52],
    "Recycled (kg)": [25, 50, 38, 28, 56, 30, 34, 43],
})
with st.sidebar:
    st.header("Dashboard filters")
    uploaded = st.file_uploader("Upload CSV (optional)", type=["csv"])
    if uploaded:
        try:
            data = pd.read_csv(uploaded)
            required = {"Date", "Area", "Waste Type", "Weight (kg)", "Recycled (kg)"}
            missing = required - set(data.columns)
            if missing:
                st.error("CSV is missing columns: " + ", ".join(sorted(missing)))
                data = SAMPLE.copy()
            else:
                data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
                data["Weight (kg)"] = pd.to_numeric(data["Weight (kg)"], errors="coerce")
                data["Recycled (kg)"] = pd.to_numeric(data["Recycled (kg)"], errors="coerce")
                data = data.dropna(subset=["Date", "Weight (kg)", "Recycled (kg)"])
        except Exception as exc:
            st.error(f"Could not read the CSV: {exc}")
            data = SAMPLE.copy()
    else:
        data = SAMPLE.copy()
    areas = st.multiselect("Area", sorted(data["Area"].dropna().unique()), default=sorted(data["Area"].dropna().unique()))
    waste_types = st.multiselect("Waste type", sorted(data["Waste Type"].dropna().unique()), default=sorted(data["Waste Type"].dropna().unique()))

filtered = data[data["Area"].isin(areas) & data["Waste Type"].isin(waste_types)].copy()
total = filtered["Weight (kg)"].sum()
recycled = filtered["Recycled (kg)"].sum()
rate = (recycled / total * 100) if total else 0
c1, c2, c3 = st.columns(3)
c1.metric("Total waste", f"{total:,.0f} kg")
c2.metric("Recorded recycled", f"{recycled:,.0f} kg")
c3.metric("Recycling share", f"{rate:.1f}%")

left, right = st.columns(2)
with left:
    st.subheader("Waste by type")
    by_type = filtered.groupby("Waste Type")["Weight (kg)"].sum().sort_values(ascending=False)
    st.bar_chart(by_type)
with right:
    st.subheader("Waste by area")
    by_area = filtered.groupby("Area")["Weight (kg)"].sum().sort_values(ascending=False)
    st.bar_chart(by_area)

st.subheader("Collection records")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_waste_data.csv", "text/csv")

st.divider()
st.subheader("Waste sorting guide")
guide = {
    "Organic": "Food scraps and garden waste: use an appropriate compost or organic-waste stream.",
    "Plastic": "Empty and rinse recyclable containers; check local recycling rules.",
    "Paper": "Keep clean and dry; greasy or food-soiled paper may not be recyclable.",
    "Metal": "Empty cans and containers; follow local collection instructions.",
}
for kind, tip in guide.items():
    st.markdown(f"**{kind}:** {tip}")

st.info("This portfolio demo uses sample records by default. Its dashboard analyzes uploaded or sample data; it does not connect to live bins or train a machine-learning model.")
