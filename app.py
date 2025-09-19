import streamlit as st
from planner import generate_itinerary, export_itinerary_text, save_itinerary, load_saved_itineraries
import json



page_bg = """
<style>
/* Background image */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
    background-size: cover;
    background-attachment: fixed;
}


/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
}

/* Card-style box for itinerary days */
.day-card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    
}

/* Headers */
h1, h2, h3 {
    font-family: 'Trebuchet MS', sans-serif;
    color: #333;
    text-shadow: 1px 1px 2px #fff;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
st.title("✈️Ease My Trip - Your AI Trip Planner 🌍")
st.markdown("Plan your dream trip with AI-powered suggestions, fun vibes & travel magic! 🏖️🏔️🕌")

# Sidebar inputs
with st.sidebar:
    st.header('🛠️ Trip Preferences')
    destination = st.selectbox(
        '🌍 Destination',
        ['Goa', 'Manali', 'Jaipur', 'Tokyo', 'Paris', 'Kerala', 'New York', 'Dubai']
    )
    days = st.number_input('📅 Number of Days', min_value=1, max_value=14, value=3)
    budget = st.number_input('💰 Total Budget (₹)', min_value=1000, step=500, value=20000)
    interests = st.multiselect(
        '🎯 Interests',
        ['beaches','nightlife','adventure','culture','relax', 'food', 'shopping', 'photoshoot', 'wellness', 'snow'], default=['beaches']
    )
    st.markdown('---')
    st.caption('⚡ Prototype: Demo data only.')

if st.button('Generate Itinerary'):
    itinerary = generate_itinerary(destination, days, budget, interests)
    st.subheader(f'Trip Plan for {destination}')
    total = 0
    for day in itinerary:
        st.markdown(f"**Day {day['day']}**")
        st.write('Activities:', ', '.join(day['activities']))
        st.write('Weather:', day['weather'])
        st.write('Estimated Cost: ₹', day['estimated_cost'])
        total += day['estimated_cost']
        st.markdown('---')
    st.success(f'Estimated Total Cost: ₹{total}')

    # Show Hotels
    st.subheader("🏨 Recommended Hotels")
    def get_hotels(destination):
        # Dummy hotel data for demonstration
        hotels_data = {
            'Goa': [
                {'name': 'Goa Beach Resort', 'price': 3500},
                {'name': 'Sunshine Inn', 'price': 2500}
            ],
            'Manali': [
                {'name': 'Himalayan Heights', 'price': 4000},
                {'name': 'Snow Valley', 'price': 2800}
            ],
            'Jaipur': [
                {'name': 'Pink Palace', 'price': 3200},
                {'name': 'Heritage Stay', 'price': 2700}
            ],
            'Tokyo': [
                {'name': 'Tokyo Central Hotel', 'price': 8000},
                {'name': 'Sakura Inn', 'price': 6500}
            ],
            'Paris': [
                {'name': 'Paris Luxury Suites', 'price': 9000},
                {'name': 'Eiffel View', 'price': 7000}
            ],
            'Kerala': [
                {'name': 'Backwater Retreat', 'price': 3000},
                {'name': 'Coconut Grove', 'price': 2200}
            ],
            'New York': [
                {'name': 'NYC Grand', 'price': 12000},
                {'name': 'Central Park Stay', 'price': 9500}
            ],
            'Dubai': [
                {'name': 'Desert Pearl', 'price': 10000},
                {'name': 'Palm Resort', 'price': 8500}
            ]
        }
        return hotels_data.get(destination, [])
    hotels = get_hotels(destination)
    for h in hotels:
        st.write(f"**{h['name']}** - ₹{h['price']}/night")

    # Payment
    st.subheader("💳 Payment")
    payment_method = st.radio("Choose Payment Method:", ["UPI", "Credit/Debit Card", "NetBanking"])
    if st.button("Proceed to Pay"):
        st.success(f"✅ Payment of ₹{total} via {payment_method} completed successfully!")

    # Save itinerary in local file
    save_itinerary(destination, itinerary, total, budget)
    st.info("✅ Itinerary saved successfully!")

    # Export text
    txt = export_itinerary_text(destination, itinerary, total, budget)
    st.download_button('📥 Download Itinerary (TXT)', data=txt, file_name='itinerary.txt')


# Sidebar: saved trips
st.sidebar.header("📂 Saved Itineraries")
saved = load_saved_itineraries()
if saved:
    for idx, trip in enumerate(saved, start=1):
        st.sidebar.write(f"{idx}. {trip['destination']} ({trip['total_cost']} ₹)")
else:
    st.sidebar.write("❌ No saved itineraries yet.")
