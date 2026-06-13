import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# ===================== DATABASE CONNECTION =====================
@st.cache_resource
def get_engine():
    return create_engine("mysql+mysqlconnector://root:mitu&b30#@localhost/food_wastage_db")

engine = get_engine()

def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="Food Wastage Management", page_icon="🍱", layout="wide")

# ===================== SIDEBAR =====================
st.sidebar.title("🍱 Food Wastage System")
page = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "📊 EDA & Charts",
    "🔍 SQL Queries",
    "🔎 Filters",
    "📞 Contact Info",
    "➕ CRUD Operations"
])

# ===================== HOME PAGE =====================
if page == "🏠 Home":
    st.title("🍱 Local Food Wastage Management System")
    st.markdown("### Reducing Food Waste by Connecting Providers & Receivers")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_providers = run_query("SELECT COUNT(*) as count FROM providers")['count'][0]
    total_receivers = run_query("SELECT COUNT(*) as count FROM receivers")['count'][0]
    total_listings = run_query("SELECT COUNT(*) as count FROM food_listings")['count'][0]
    total_claims = run_query("SELECT COUNT(*) as count FROM claims")['count'][0]
    
    col1.metric("🏪 Total Providers", total_providers)
    col2.metric("🤝 Total Receivers", total_receivers)
    col3.metric("🍲 Food Listings", total_listings)
    col4.metric("📋 Total Claims", total_claims)
    
    st.markdown("---")
    st.markdown("""
    ### 📌 About This System
    This system helps **reduce food wastage** by connecting:
    - 🏪 **Food Providers** (Restaurants, Grocery Stores, Supermarkets)
    - 🤝 **Receivers** (NGOs, Community Centers, Individuals)
    
    ### 🎯 Business Objective
    - Providers list surplus food
    - Receivers claim available food
    - Track and analyze food distribution
    - Reduce hunger and food waste
    """)

# ===================== EDA & CHARTS =====================
elif page == "📊 EDA & Charts":
    st.title("📊 Exploratory Data Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Univariate", "Bivariate", "Claim Analysis"])
    
    with tab1:
        st.subheader("Univariate Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            df = run_query("SELECT Type, COUNT(*) as Count FROM providers GROUP BY Type")
            fig = px.pie(df, names='Type', values='Count', title='Provider Type Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            df = run_query("SELECT Type, COUNT(*) as Count FROM receivers GROUP BY Type")
            fig = px.bar(df, x='Type', y='Count', title='Receiver Type Distribution', color='Type')
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            df = run_query("SELECT Food_Type, COUNT(*) as Count FROM food_listings GROUP BY Food_Type")
            fig = px.pie(df, names='Food_Type', values='Count', title='Food Type Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            df = run_query("SELECT Meal_Type, COUNT(*) as Count FROM food_listings GROUP BY Meal_Type")
            fig = px.bar(df, x='Meal_Type', y='Count', title='Meal Type Distribution', color='Meal_Type')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Bivariate Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            df = run_query("SELECT Location, COUNT(*) as Total_Listings FROM food_listings GROUP BY Location ORDER BY Total_Listings DESC LIMIT 15")
            fig = px.bar(df, x='Location', y='Total_Listings', title='City vs Food Listings', color='Total_Listings')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            df = run_query("SELECT Provider_Type, SUM(Quantity) as Total_Quantity FROM food_listings GROUP BY Provider_Type")
            fig = px.bar(df, x='Provider_Type', y='Total_Quantity', title='Provider Type vs Quantity', color='Provider_Type')
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            df = run_query("SELECT Food_Type, SUM(Quantity) as Total_Quantity FROM food_listings GROUP BY Food_Type")
            fig = px.pie(df, names='Food_Type', values='Total_Quantity', title='Food Type vs Quantity')
            st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            df = run_query("SELECT Meal_Type, SUM(Quantity) as Total_Quantity FROM food_listings GROUP BY Meal_Type")
            fig = px.bar(df, x='Meal_Type', y='Total_Quantity', title='Meal Type vs Quantity', color='Meal_Type')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Claim Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            df = run_query("SELECT Status, COUNT(*) as Count FROM claims GROUP BY Status")
            fig = px.pie(df, names='Status', values='Count', title='Claim Status Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            df = run_query("""SELECT r.Name, COUNT(c.Claim_ID) as Total_Claims 
                FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID 
                GROUP BY r.Name ORDER BY Total_Claims DESC LIMIT 10""")
            fig = px.bar(df, x='Name', y='Total_Claims', title='Top 10 Receivers by Claims', color='Total_Claims')
            st.plotly_chart(fig, use_container_width=True)
        
        df = run_query("""SELECT p.Name, COUNT(c.Claim_ID) as Total_Claims 
            FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY p.Name ORDER BY Total_Claims DESC LIMIT 10""")
        fig = px.bar(df, x='Name', y='Total_Claims', title='Top 10 Providers by Claims', color='Total_Claims')
        st.plotly_chart(fig, use_container_width=True)

# ===================== SQL QUERIES =====================
elif page == "🔍 SQL Queries":
    st.title("🔍 SQL Query Results")
    
    queries = {
        "Q1: City-wise Providers & Receivers": """SELECT p.City, COUNT(DISTINCT p.Provider_ID) AS Total_Providers, COUNT(DISTINCT r.Receiver_ID) AS Total_Receivers FROM providers p LEFT JOIN receivers r ON p.City = r.City GROUP BY p.City""",
        "Q2: Provider Type vs Food Quantity": """SELECT Provider_Type, SUM(Quantity) AS Total_Food FROM food_listings GROUP BY Provider_Type ORDER BY Total_Food DESC""",
        "Q3: Providers Contact Info": """SELECT Name, Type, Address, Contact FROM providers LIMIT 20""",
        "Q4: Top Receivers by Claims": """SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Name ORDER BY Total_Claims DESC LIMIT 10""",
        "Q5: Total Food Quantity": """SELECT SUM(Quantity) AS Total_Available_Food FROM food_listings""",
        "Q6: City with Most Listings": """SELECT Location, COUNT(Food_ID) AS Total_Listings FROM food_listings GROUP BY Location ORDER BY Total_Listings DESC""",
        "Q7: Most Common Food Types": """SELECT Food_Type, COUNT(*) AS Count FROM food_listings GROUP BY Food_Type ORDER BY Count DESC""",
        "Q8: Claims per Food Item": """SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims FROM food_listings f LEFT JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Food_Name ORDER BY Total_Claims DESC LIMIT 20""",
        "Q9: Top Providers by Successful Claims": """SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID JOIN claims c ON f.Food_ID = c.Food_ID WHERE c.Status = 'Completed' GROUP BY p.Name ORDER BY Successful_Claims DESC LIMIT 10""",
        "Q10: Claim Status Percentage": """SELECT Status, COUNT(*) AS Total, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage FROM claims GROUP BY Status""",
        "Q11: Avg Quantity per Receiver": """SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS Avg_Quantity FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY r.Name LIMIT 20""",
        "Q12: Most Claimed Meal Type": """SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims FROM food_listings f JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Meal_Type ORDER BY Total_Claims DESC""",
        "Q13: Total Food Donated by Provider": """SELECT p.Name, SUM(f.Quantity) AS Total_Donated FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Name ORDER BY Total_Donated DESC LIMIT 20""",
        "Q14: Food Expiring in 7 Days": """SELECT Food_Name, Quantity, Expiry_Date, Location FROM food_listings WHERE Expiry_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY) ORDER BY Expiry_Date ASC""",
        "Q15: City-wise Completion Rate": """SELECT f.Location AS City, COUNT(c.Claim_ID) AS Total_Claims, ROUND(SUM(CASE WHEN c.Status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Completion_Rate FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID GROUP BY f.Location ORDER BY Total_Claims DESC""",
    }
    
    selected_query = st.selectbox("Select a Query", list(queries.keys()))
    
    if st.button("▶ Run Query"):
        df = run_query(queries[selected_query])
        st.success(f"✅ {len(df)} rows returned")
        st.dataframe(df, use_container_width=True)

# ===================== FILTERS =====================
elif page == "🔎 Filters":
    st.title("🔎 Filter Food Listings")
    
    cities = run_query("SELECT DISTINCT Location FROM food_listings ORDER BY Location")['Location'].tolist()
    food_types = run_query("SELECT DISTINCT Food_Type FROM food_listings ORDER BY Food_Type")['Food_Type'].tolist()
    meal_types = run_query("SELECT DISTINCT Meal_Type FROM food_listings ORDER BY Meal_Type")['Meal_Type'].tolist()
    provider_types = run_query("SELECT DISTINCT Provider_Type FROM food_listings ORDER BY Provider_Type")['Provider_Type'].tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Select City", ["All"] + cities)
        selected_food_type = st.selectbox("Select Food Type", ["All"] + food_types)
    with col2:
        selected_meal_type = st.selectbox("Select Meal Type", ["All"] + meal_types)
        selected_provider_type = st.selectbox("Select Provider Type", ["All"] + provider_types)
    
    query = "SELECT * FROM food_listings WHERE 1=1"
    if selected_city != "All":
        query += f" AND Location = '{selected_city}'"
    if selected_food_type != "All":
        query += f" AND Food_Type = '{selected_food_type}'"
    if selected_meal_type != "All":
        query += f" AND Meal_Type = '{selected_meal_type}'"
    if selected_provider_type != "All":
        query += f" AND Provider_Type = '{selected_provider_type}'"
    
    df = run_query(query)
    st.success(f"✅ {len(df)} records found")
    st.dataframe(df, use_container_width=True)

# ===================== CONTACT INFO =====================
elif page == "📞 Contact Info":
    st.title("📞 Contact Information")
    
    tab1, tab2 = st.tabs(["🏪 Providers", "🤝 Receivers"])
    
    with tab1:
        st.subheader("Provider Contact Details")
        cities = run_query("SELECT DISTINCT City FROM providers ORDER BY City")['City'].tolist()
        selected_city = st.selectbox("Filter by City", ["All"] + cities)
        
        if selected_city == "All":
            df = run_query("SELECT Name, Type, City, Address, Contact FROM providers")
        else:
            df = run_query(f"SELECT Name, Type, City, Address, Contact FROM providers WHERE City = '{selected_city}'")
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Receiver Contact Details")
        cities2 = run_query("SELECT DISTINCT City FROM receivers ORDER BY City")['City'].tolist()
        selected_city2 = st.selectbox("Filter by City", ["All"] + cities2, key="rec_city")
        
        if selected_city2 == "All":
            df = run_query("SELECT Name, Type, City, Contact FROM receivers")
        else:
            df = run_query(f"SELECT Name, Type, City, Contact FROM receivers WHERE City = '{selected_city2}'")
        st.dataframe(df, use_container_width=True)

# ===================== CRUD =====================
elif page == "➕ CRUD Operations":
    st.title("➕ CRUD Operations")
    
    operation = st.radio("Select Operation", ["➕ Add Food Listing", "📋 View All Listings", "✏️ Update Listing", "🗑️ Delete Listing"])
    
    if operation == "➕ Add Food Listing":
        st.subheader("Add New Food Listing")
        col1, col2 = st.columns(2)
        with col1:
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry_date = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1)
        with col2:
            provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket", "Catering"])
            location = st.text_input("Location/City")
            food_type = st.selectbox("Food Type", ["Veg", "Non-Veg", "Vegan"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        
        if st.button("➕ Add Listing"):
            try:
                with engine.connect() as conn:
                    conn.execute(text(f"""INSERT INTO food_listings 
                        (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                        VALUES ('{food_name}', {quantity}, '{expiry_date}', {provider_id}, '{provider_type}', '{location}', '{food_type}', '{meal_type}')"""))
                    conn.commit()
                st.success("✅ Food listing added successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif operation == "📋 View All Listings":
        st.subheader("All Food Listings")
        df = run_query("SELECT * FROM food_listings LIMIT 100")
        st.dataframe(df, use_container_width=True)
    
    elif operation == "✏️ Update Listing":
        st.subheader("Update Food Listing")
        food_id = st.number_input("Enter Food ID to Update", min_value=1)
        new_quantity = st.number_input("New Quantity", min_value=1)
        
        if st.button("✏️ Update"):
            try:
                with engine.connect() as conn:
                    conn.execute(text(f"UPDATE food_listings SET Quantity = {new_quantity} WHERE Food_ID = {food_id}"))
                    conn.commit()
                st.success("✅ Updated successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif operation == "🗑️ Delete Listing":
        st.subheader("Delete Food Listing")
        food_id = st.number_input("Enter Food ID to Delete", min_value=1)
        
        if st.button("🗑️ Delete"):
            try:
                with engine.connect() as conn:
                    conn.execute(text(f"DELETE FROM food_listings WHERE Food_ID = {food_id}"))
                    conn.commit()
                st.success("✅ Deleted successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")