import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:mitu&b30#@localhost/food_wastage_db")

with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.commit()

providers = pd.read_csv(r"C:\Users\Dell\Downloads\food_wastage_project\providers_data.csv")
receivers = pd.read_csv(r"C:\Users\Dell\Downloads\food_wastage_project\receivers_data.csv")
food_listings = pd.read_csv(r"C:\Users\Dell\Downloads\food_wastage_project\food_listings_data.csv")
claims = pd.read_csv(r"C:\Users\Dell\Downloads\food_wastage_project\claims_data.csv")

providers.to_sql("providers", con=engine, if_exists="replace", index=False)
print("✅ Providers imported!")

receivers.to_sql("receivers", con=engine, if_exists="replace", index=False)
print("✅ Receivers imported!")

food_listings.to_sql("food_listings", con=engine, if_exists="replace", index=False)
print("✅ Food Listings imported!")

claims.to_sql("claims", con=engine, if_exists="replace", index=False)
print("✅ Claims imported!")

with engine.connect() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    conn.commit()

print("🎉 All data imported successfully!")