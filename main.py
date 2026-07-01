import pandas as pd


# Import admin earnings
admin_earnings = pd.read_csv(r"C:\Users\user\Downloads\admin-earnings-orders-export_v1.3.1_countryCode=DZ&filters=s_1782774000000_e_1782946799999.csv")
print("File imported successfuly!")

#======================= Normalize admin earnings columns names =======================#

# Remove white spaces from column names
admin_earnings.columns = admin_earnings.columns.str.strip()

# Replace upper cases in column names
admin_earnings.columns = admin_earnings.columns.str.lower()

# Turn column names to snake case
admin_earnings.columns = admin_earnings.columns.str.replace(" ", "_")

#======================= Transform admin earnings columns =======================#

# Merge *order_day* and *order_time* columns to create *order_at* column as timestamp type
order_day_idx = admin_earnings.columns.get_loc('order_day')
order_at = pd.to_datetime(admin_earnings['order_day'].astype(str) + " " + admin_earnings['order_time'].astype(str))
admin_earnings.insert(order_day_idx, 'order_at', order_at)

admin_earnings = admin_earnings.drop(columns=['order_day', 'order_time'])
print(admin_earnings.head(10))

# Merge *delivered_day* and *delivered_at* columns to create *delivered_at* column as timestamp type
delivered_day_idx = admin_earnings.columns.get_loc('delivered_day')
delivered_at_clean = pd.to_datetime(admin_earnings['delivered_day'].astype(str) + " " + admin_earnings['delivered_at'].astype(str))
admin_earnings.insert(delivered_day_idx, 'delivered_at_clean', delivered_at_clean)

admin_earnings = admin_earnings.drop(columns=['delivered_day', 'delivered_at'])
admin_earnings.rename({'delivered_at_clean': 'delivered_at'})
print(admin_earnings.head(10))



