
import streamlit as st

def predict_uhi(impervious, tree_cover, bldg_height, svf, ucr, dist_industry_km, orientation):
    uhi_2am = (
        0.008 * impervious -
        0.007 * tree_cover +
        0.06 * bldg_height +
        0.9 * ucr +
        0.5 * svf -
        0.2 * dist_industry_km +
        (0.5 if orientation == "E-W" else 0.2)
    )
    uhi_4pm = (
        0.004 * impervious -
        0.0045 * tree_cover +
        0.02 * bldg_height +
        0.3 * ucr +
        0.6 * svf -
        0.4 * dist_industry_km +
        (0.4 if orientation == "E-W" else 0.1)
    )
    lcz_guess = "LCZ 1" if bldg_height > 15 else "LCZ 3" if bldg_height > 10 else "LCZ 6"
    mitigation = "Increase tree cover or reduce impervious surface" if uhi_4pm > 1.5 else "Urban form is moderately heat-resilient"
    return lcz_guess, round(uhi_2am, 2), round(uhi_4pm, 2), mitigation

st.title("🌆 LCZ-UHI Predictor Tool")
st.markdown("Simulate urban heat island intensity based on Local Climate Zone inputs")

impervious = st.slider("% Impervious Surface", 0, 100, 75)
tree_cover = st.slider("% Tree Canopy Cover", 0, 100, 20)
bldg_height = st.slider("Building Height (m)", 0, 50, 12)
svf = st.slider("Sky View Factor", 0.0, 1.0, 0.55)
ucr = st.slider("Urban Canyon Ratio", 0.1, 2.0, 0.8)
dist_industry_km = st.slider("Distance to Industry (km)", 0.0, 10.0, 2.0)
orientation = st.selectbox("Street Orientation", ["E-W", "N-S"])

if st.button("Run Simulation"):
    lcz, uhi2am, uhi4pm, tip = predict_uhi(impervious, tree_cover, bldg_height, svf, ucr, dist_industry_km, orientation)
    st.success(f"Predicted LCZ Type: {lcz}")
    st.metric("Predicted UHI at 2 AM", f"{uhi2am} °C")
    st.metric("Predicted UHI at 4 PM", f"{uhi4pm} °C")
    st.info(f"Mitigation Tip: {tip}")
