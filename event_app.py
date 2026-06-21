import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="GridlockPulse Event Optimizer", layout="wide")
st.title("🔀 GridlockPulse: Predictive Event-Driven Traffic Optimization Engine")
st.markdown("### Flipkart Gridlock Hackathon 2.0 - Resource Allocation Prototype")
st.write("---")

# 1. Load and Profile the Astram Dataset inside the App
@st.cache_data
def load_and_profile_data():
    file_path = "Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv"
    df = pd.read_csv(file_path)
    
    # Pure Python Geohash Encoder
    def encode_geohash(latitude, longitude, precision=5):
        base32 = "0123456789bcdefghjkmnpqrstuvwxyz"
        lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
        geohash_chars = []
        bits, ch, even = 0, 0, True
        while len(geohash_chars) < precision:
            if even:
                mid = (lon_interval[0] + lon_interval[1]) / 2.0
                if longitude > mid: ch |= (1 << (4 - bits)); lon_interval = (mid, lon_interval[1])
                else: lon_interval = (lon_interval[0], mid)
            else:
                mid = (lat_interval[0] + lat_interval[1]) / 2.0
                if latitude > mid: ch |= (1 << (4 - bits)); lat_interval = (mid, lat_interval[1])
                else: lat_interval = (lat_interval[0], mid)
            even = not even
            if bits < 4: bits += 1
            else: geohash_chars.append(base32[ch]); bits, ch = 0, 0
        return "".join(geohash_chars)

    df['geohash_sector'] = df.apply(lambda r: encode_geohash(r['latitude'], r['longitude'], 5), axis=1)
    
    # Pre-calculate data frameworks
    cause_profiles = df.groupby('event_cause').agg(
        closure_rate=('requires_road_closure', 'mean')
    ).reset_index()
    
    zone_profiles = df.groupby('geohash_sector').size().to_dict()
    return df, cause_profiles, zone_profiles

df, historical_causes, historical_zones = load_and_profile_data()

# Initialize Session State Memory for continuous post-event learning logs
if 'learning_logs' not in st.session_state:
    st.session_state.learning_logs = []

# 2. Sidebar Configuration Setup
st.sidebar.header("🕹️ Scheduled Event Parameter Configurator")
selected_cause = st.sidebar.selectbox("Select Scheduled Event/Incident Cause", options=historical_causes['event_cause'].unique(), index=9)
input_lat = st.sidebar.number_input("Event Target Latitude", value=13.0400, format="%.4f")
input_lon = st.sidebar.number_input("Event Target Longitude", value=77.5181, format="%.4f")
expected_attendance = st.sidebar.slider("Expected Traffic / Attendance Volume", 500, 30000, 8000)
scheduled_hour = st.sidebar.slider("Scheduled Activation Peak Hour", 0, 23, 17)

# 3. Analytics Execution Engine Block
if st.sidebar.button("Run Data-Driven Impact Assessment"):
    # Re-calculate specific geohash zone coordinate
    def quick_encode(lat, lon):
        base32 = "0123456789bcdefghjkmnpqrstuvwxyz"
        lat_int, lon_int = (-90.0, 90.0), (-180.0, 180.0)
        gh = []
        bits, ch, even = 0, 0, True
        for _ in range(25):
            if even:
                mid = (lon_int[0] + lon_int[1]) / 2.0
                if lon > mid: ch |= (1 << (4 - bits)); lon_int = (mid, lon_int[1])
                else: lon_int = (lon_int[0], mid)
            else:
                mid = (lat_int[0] + lat_int[1]) / 2.0
                if lat > mid: ch |= (1 << (4 - bits)); lat_int = (mid, lat_int[1])
                else: lat_int = (lat_int[0], mid)
            even = not even
            if bits < 4: bits += 1
            else: gh.append(base32[ch]); bits, ch = 0, 0
        return "".join(gh)
        
    target_gh = quick_encode(input_lat, input_lon)
    
    st.subheader(f"📊 Historical Traffic Forecast Analysis | Target Sector Grid: `{target_gh}`")
    
    # Extract structural constraints from our analytical profiling steps
    cause_data = historical_causes[historical_causes['event_cause'] == selected_cause].iloc[0]
    closure_rate = cause_data['closure_rate']
    regional_incidents = historical_zones.get(target_gh, 0)
    
    # Multi-factor Disruption Score calculation formulas
    volume_factor = min(1.0, expected_attendance / 30000.0)
    regional_hazard = min(1.0, regional_incidents / 1000.0)
    disruption_score = (volume_factor * 0.4) + (closure_rate * 0.4) + (regional_hazard * 0.2)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Disruption Complexity Score", f"{disruption_score:.4f}")
    m2.metric("Historical Road Closure Rate", f"{closure_rate * 100:.1f}%")
    m3.metric("Prior Incidents in this Sector", f"{regional_incidents} records")
    st.write("---")
    
    # 4. Resource Allocation Recommender
    st.subheader("👮 Automated Strategic Tactical Deployment Plan")
    officers = int(np.ceil(disruption_score * (expected_attendance / 250) + 2))
    barricades = int(np.ceil(closure_rate * 40 + (disruption_score * 25)))
    detours = 1 if disruption_score < 0.4 else 2 if disruption_score < 0.7 else 4
    
    r1, r2, r3 = st.columns(3)
    r1.info(f"**Traffic Manpower Deployment:**\n\n**{officers} Personnel** mapped across approach junctions.")
    r2.warning(f"**Physical Barricading Units:**\n\n**{barricades} Barriers** required for outer filtration.")
    r3.error(f"**Diversion Detour Configurations:**\n\nActivate **{detours} Detours** to reroute traffic.")
    st.write("---")
    
    # 5. Hourly Forecast Projection Graphs 
    st.subheader("📈 Spatiotemporal Congestion Surge Ripple Forecast Curve")
    hours = list(range(24))
    normal_baseline = []
    predicted_surge = []
    
    for h in hours:
        # Standard background city rush hour signature modeling
        base_demand = 0.3 + 0.3 * np.exp(-((h - 9)/3.0)**2) + 0.4 * np.exp(-((h - 18)/3.0)**2)
        normal_baseline.append(min(1.0, base_demand))
        
        # Inject the active structural event anomaly spike window
        surge_demand = base_demand
        if scheduled_hour <= h <= (scheduled_hour + 4) % 24:
            surge_demand += (disruption_score * 0.4)
        predicted_surge.append(min(1.0, surge_demand))
        
    # Combine into a clean long-form DataFrame with safe bracketed list concatenation
    trend_df = pd.DataFrame({
        "Hour of the Day": hours * 2,
        "Breakdown Probability": normal_baseline + predicted_surge,
        "Scenario Pipeline": (["Normal City Baseline"] * 24) + (["Event-Driven Impact Surge"] * 24)
    })
    
    # Generate multi-line visualization with color mapping
    fig = px.line(
        trend_df, 
        x="Hour of the Day", 
        y="Breakdown Probability", 
        color="Scenario Pipeline",
        color_discrete_map={"Normal City Baseline": "#00FFCC", "Event-Driven Impact Surge": "#FF3366"},
        markers=True,
        title="Comparative Spatiotemporal Breakdown Ripple Forecast Analysis"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 6. Post-Event Learning Interface
st.write("---")
st.subheader("🔄 Post-Event Learning & Continuous Strategy Evaluation Registry")
with st.form("learning_registry"):
    event_ref = st.text_input("Conducted Event Operation Name", "Public Assembly Gathering")
    outcome_rating = st.selectbox("Observed Resource Management Rating", ["Optimal Deployment", "Understaffed - Intersections Congested", "Overstaffed - Low Asset Utilization"])
    field_notes = st.text_area("Provide Field Feedback Constraints Logged")
    
    if st.form_submit_button("Commit Evaluation to memory"):
        st.session_state.learning_logs.append({
            "Event Reference": event_ref,
            "Evaluation Metric": outcome_rating,
            "Field Notes": field_notes
        })
        st.success("Record committed successfully!")

if st.session_state.learning_logs:
    st.write("#### Active Local Continuous Learning Database Logs:")
    st.dataframe(pd.DataFrame(st.session_state.learning_logs), use_container_width=True)
