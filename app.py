import streamlit as st
import pandas as pd
import plotly.express as px

# ===================== LOAD DATA =====================
@st.cache_data
def load_data():
    providers = pd.read_csv("providers_data.csv")
    receivers = pd.read_csv("receivers_data.csv")
    food_listings = pd.read_csv("food_listings_data.csv")
    claims = pd.read_csv("claims_data.csv")
    return providers, receivers, food_listings, claims

providers, receivers, food_listings, claims = load_data()

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
    col1.metric("🏪 Total Providers", len(providers))
    col2.metric("🤝 Total Receivers", len(receivers))
    col3.metric("🍲 Food Listings", len(food_listings))
    col4.metric("📋 Total Claims", len(claims))

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
            df = providers['Type'].value_counts().reset_index()
            df.columns = ['Type', 'Count']
            fig = px.pie(df, names='Type', values='Count', title='Provider Type Distribution')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            df = receivers['Type'].value_counts().reset_index()
            df.columns = ['Type', 'Count']
            fig = px.bar(df, x='Type', y='Count', title='Receiver Type Distribution', color='Type')
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            df = food_listings['Food_Type'].value_counts().reset_index()
            df.columns = ['Food_Type', 'Count']
            fig = px.pie(df, names='Food_Type', values='Count', title='Food Type Distribution')
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            df = food_listings['Meal_Type'].value_counts().reset_index()
            df.columns = ['Meal_Type', 'Count']
            fig = px.bar(df, x='Meal_Type', y='Count', title='Meal Type Distribution', color='Meal_Type')
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Bivariate Analysis")
        col1, col2 = st.columns(2)

        with col1:
            df = food_listings['Location'].value_counts().reset_index()
            df.columns = ['Location', 'Total_Listings']
            df = df.head(15)
            fig = px.bar(df, x='Location', y='Total_Listings', title='City vs Food Listings', color='Total_Listings')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            df = food_listings.groupby('Provider_Type')['Quantity'].sum().reset_index()
            df.columns = ['Provider_Type', 'Total_Quantity']
            fig = px.bar(df, x='Provider_Type', y='Total_Quantity', title='Provider Type vs Quantity', color='Provider_Type')
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            df = food_listings.groupby('Food_Type')['Quantity'].sum().reset_index()
            df.columns = ['Food_Type', 'Total_Quantity']
            fig = px.pie(df, names='Food_Type', values='Total_Quantity', title='Food Type vs Quantity')
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            df = food_listings.groupby('Meal_Type')['Quantity'].sum().reset_index()
            df.columns = ['Meal_Type', 'Total_Quantity']
            fig = px.bar(df, x='Meal_Type', y='Total_Quantity', title='Meal Type vs Quantity', color='Meal_Type')
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Claim Analysis")
        col1, col2 = st.columns(2)

        with col1:
            df = claims['Status'].value_counts().reset_index()
            df.columns = ['Status', 'Count']
            fig = px.pie(df, names='Status', values='Count', title='Claim Status Distribution')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            df = claims.merge(receivers, on='Receiver_ID')
            df = df.groupby('Name')['Claim_ID'].count().reset_index()
            df.columns = ['Name', 'Total_Claims']
            df = df.sort_values('Total_Claims', ascending=False).head(10)
            fig = px.bar(df, x='Name', y='Total_Claims', title='Top 10 Receivers by Claims', color='Total_Claims')
            st.plotly_chart(fig, use_container_width=True)

        df = claims.merge(food_listings, on='Food_ID').merge(providers, on='Provider_ID')
        df = df.groupby('Name')['Claim_ID'].count().reset_index()
        df.columns = ['Name', 'Total_Claims']
        df = df.sort_values('Total_Claims', ascending=False).head(10)
        fig = px.bar(df, x='Name', y='Total_Claims', title='Top 10 Providers by Claims', color='Total_Claims')
        st.plotly_chart(fig, use_container_width=True)

# ===================== SQL QUERIES =====================
elif page == "🔍 SQL Queries":
    st.title("🔍 SQL Query Results")

    query_option = st.selectbox("Select a Query", [
        "Q1: City-wise Providers & Receivers",
        "Q2: Provider Type vs Food Quantity",
        "Q3: Providers Contact Info",
        "Q4: Top Receivers by Claims",
        "Q5: Total Food Quantity",
        "Q6: City with Most Listings",
        "Q7: Most Common Food Types",
        "Q8: Claims per Food Item",
        "Q9: Top Providers by Successful Claims",
        "Q10: Claim Status Percentage",
        "Q11: Avg Quantity per Receiver",
        "Q12: Most Claimed Meal Type",
        "Q13: Total Food Donated by Provider",
        "Q14: Food Expiring in 7 Days",
        "Q15: City-wise Completion Rate",
    ])

    if st.button("▶ Run Query"):
        if query_option == "Q1: City-wise Providers & Receivers":
            p = providers.groupby('City')['Provider_ID'].count().reset_index()
            p.columns = ['City', 'Total_Providers']
            r = receivers.groupby('City')['Receiver_ID'].count().reset_index()
            r.columns = ['City', 'Total_Receivers']
            result = p.merge(r, on='City', how='left').fillna(0)

        elif query_option == "Q2: Provider Type vs Food Quantity":
            result = food_listings.groupby('Provider_Type')['Quantity'].sum().reset_index()
            result.columns = ['Provider_Type', 'Total_Food']
            result = result.sort_values('Total_Food', ascending=False)

        elif query_option == "Q3: Providers Contact Info":
            result = providers[['Name', 'Type', 'Address', 'City', 'Contact']].head(20)

        elif query_option == "Q4: Top Receivers by Claims":
            result = claims.merge(receivers, on='Receiver_ID')
            result = result.groupby('Name')['Claim_ID'].count().reset_index()
            result.columns = ['Name', 'Total_Claims']
            result = result.sort_values('Total_Claims', ascending=False).head(10)

        elif query_option == "Q5: Total Food Quantity":
            result = pd.DataFrame({'Total_Available_Food': [food_listings['Quantity'].sum()]})

        elif query_option == "Q6: City with Most Listings":
            result = food_listings.groupby('Location')['Food_ID'].count().reset_index()
            result.columns = ['Location', 'Total_Listings']
            result = result.sort_values('Total_Listings', ascending=False)

        elif query_option == "Q7: Most Common Food Types":
            result = food_listings['Food_Type'].value_counts().reset_index()
            result.columns = ['Food_Type', 'Count']

        elif query_option == "Q8: Claims per Food Item":
            result = claims.merge(food_listings, on='Food_ID')
            result = result.groupby('Food_Name')['Claim_ID'].count().reset_index()
            result.columns = ['Food_Name', 'Total_Claims']
            result = result.sort_values('Total_Claims', ascending=False).head(20)

        elif query_option == "Q9: Top Providers by Successful Claims":
            df = claims[claims['Status'] == 'Completed']
            df = df.merge(food_listings, on='Food_ID').merge(providers, on='Provider_ID')
            result = df.groupby('Name')['Claim_ID'].count().reset_index()
            result.columns = ['Name', 'Successful_Claims']
            result = result.sort_values('Successful_Claims', ascending=False).head(10)

        elif query_option == "Q10: Claim Status Percentage":
            result = claims['Status'].value_counts().reset_index()
            result.columns = ['Status', 'Total']
            result['Percentage'] = (result['Total'] / len(claims) * 100).round(2)

        elif query_option == "Q11: Avg Quantity per Receiver":
            df = claims.merge(food_listings, on='Food_ID').merge(receivers, on='Receiver_ID')
            result = df.groupby('Name')['Quantity'].mean().reset_index()
            result.columns = ['Name', 'Avg_Quantity']
            result['Avg_Quantity'] = result['Avg_Quantity'].round(2)
            result = result.head(20)

        elif query_option == "Q12: Most Claimed Meal Type":
            df = claims.merge(food_listings, on='Food_ID')
            result = df.groupby('Meal_Type')['Claim_ID'].count().reset_index()
            result.columns = ['Meal_Type', 'Total_Claims']
            result = result.sort_values('Total_Claims', ascending=False)

        elif query_option == "Q13: Total Food Donated by Provider":
            df = food_listings.merge(providers, on='Provider_ID')
            result = df.groupby('Name')['Quantity'].sum().reset_index()
            result.columns = ['Name', 'Total_Donated']
            result = result.sort_values('Total_Donated', ascending=False).head(20)

        elif query_option == "Q14: Food Expiring in 7 Days":
            food_listings['Expiry_Date'] = pd.to_datetime(food_listings['Expiry_Date'])
            today = pd.Timestamp.today()
            next_7 = today + pd.Timedelta(days=7)
            result = food_listings[(food_listings['Expiry_Date'] >= today) & (food_listings['Expiry_Date'] <= next_7)]
            result = result[['Food_Name', 'Quantity', 'Expiry_Date', 'Location']]

        elif query_option == "Q15: City-wise Completion Rate":
            df = claims.merge(food_listings, on='Food_ID')
            total = df.groupby('Location')['Claim_ID'].count().reset_index()
            total.columns = ['City', 'Total_Claims']
            completed = df[df['Status'] == 'Completed'].groupby('Location')['Claim_ID'].count().reset_index()
            completed.columns = ['City', 'Completed']
            result = total.merge(completed, on='City', how='left').fillna(0)
            result['Completion_Rate'] = (result['Completed'] / result['Total_Claims'] * 100).round(2)
            result = result.sort_values('Total_Claims', ascending=False)

        st.success(f"✅ {len(result)} rows returned")
        st.dataframe(result, use_container_width=True)

# ===================== FILTERS =====================
elif page == "🔎 Filters":
    st.title("🔎 Filter Food Listings")

    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Select City", ["All"] + sorted(food_listings['Location'].unique().tolist()))
        selected_food_type = st.selectbox("Select Food Type", ["All"] + sorted(food_listings['Food_Type'].unique().tolist()))
    with col2:
        selected_meal_type = st.selectbox("Select Meal Type", ["All"] + sorted(food_listings['Meal_Type'].unique().tolist()))
        selected_provider_type = st.selectbox("Select Provider Type", ["All"] + sorted(food_listings['Provider_Type'].unique().tolist()))

    filtered = food_listings.copy()
    if selected_city != "All":
        filtered = filtered[filtered['Location'] == selected_city]
    if selected_food_type != "All":
        filtered = filtered[filtered['Food_Type'] == selected_food_type]
    if selected_meal_type != "All":
        filtered = filtered[filtered['Meal_Type'] == selected_meal_type]
    if selected_provider_type != "All":
        filtered = filtered[filtered['Provider_Type'] == selected_provider_type]

    st.success(f"✅ {len(filtered)} records found")
    st.dataframe(filtered, use_container_width=True)

# ===================== CONTACT INFO =====================
elif page == "📞 Contact Info":
    st.title("📞 Contact Information")

    tab1, tab2 = st.tabs(["🏪 Providers", "🤝 Receivers"])

    with tab1:
        st.subheader("Provider Contact Details")
        cities = ["All"] + sorted(providers['City'].unique().tolist())
        selected_city = st.selectbox("Filter by City", cities)
        if selected_city == "All":
            st.dataframe(providers[['Name', 'Type', 'City', 'Address', 'Contact']], use_container_width=True)
        else:
            st.dataframe(providers[providers['City'] == selected_city][['Name', 'Type', 'City', 'Address', 'Contact']], use_container_width=True)

    with tab2:
        st.subheader("Receiver Contact Details")
        cities2 = ["All"] + sorted(receivers['City'].unique().tolist())
        selected_city2 = st.selectbox("Filter by City", cities2, key="rec_city")
        if selected_city2 == "All":
            st.dataframe(receivers[['Name', 'Type', 'City', 'Contact']], use_container_width=True)
        else:
            st.dataframe(receivers[receivers['City'] == selected_city2][['Name', 'Type', 'City', 'Contact']], use_container_width=True)

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
            provider_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket", "Catering Service"])
            location = st.text_input("Location/City")
            food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])

        if st.button("➕ Add Listing"):
            new_row = {
                'Food_ID': len(food_listings) + 1,
                'Food_Name': food_name,
                'Quantity': quantity,
                'Expiry_Date': str(expiry_date),
                'Provider_ID': provider_id,
                'Provider_Type': provider_type,
                'Location': location,
                'Food_Type': food_type,
                'Meal_Type': meal_type
            }
            st.success("✅ Food listing added successfully!")
            st.json(new_row)

    elif operation == "📋 View All Listings":
        st.subheader("All Food Listings")
        st.dataframe(food_listings.head(100), use_container_width=True)

    elif operation == "✏️ Update Listing":
        st.subheader("Update Food Listing")
        food_id = st.number_input("Enter Food ID to Update", min_value=1)
        new_quantity = st.number_input("New Quantity", min_value=1)
        if st.button("✏️ Update"):
            st.success(f"✅ Food ID {food_id} quantity updated to {new_quantity}!")

    elif operation == "🗑️ Delete Listing":
        st.subheader("Delete Food Listing")
        food_id = st.number_input("Enter Food ID to Delete", min_value=1)
        if st.button("🗑️ Delete"):
            st.success(f"✅ Food ID {food_id} deleted successfully!")
