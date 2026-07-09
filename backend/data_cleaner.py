import pandas as pd

def data_cleaner(data_file):
    """ This function takes the orders export and cleans and transform the data """
    data_file = pd.read_csv(data_file)

    #======================= Normalize admin earnings columns names =======================#
    data_file.columns = data_file.columns.str.strip()
    data_file.columns = data_file.columns.str.lower()
    data_file.columns = data_file.columns.str.replace(" ", "_")

    #======================= Transform admin earnings columns =======================#
    # Merge *order_day* and *order_time* columns to create *order_at* column as timestamp type
    order_day_idx = data_file.columns.get_loc('order_day')
    order_at = pd.to_datetime(data_file['order_day'].astype(str) + " " + data_file['order_time'].astype(str), errors="coerce")
    data_file.insert(order_day_idx, 'order_at', order_at)

    data_file = data_file.drop(columns=['order_day', 'order_time'])

    # Merge *delivered_day* and *delivered_at* columns to create *delivered_at* column as timestamp type
    delivered_day_idx = data_file.columns.get_loc('delivered_day')
    delivered_at_clean = pd.to_datetime(data_file['delivered_day'].astype(str) + " " + data_file['delivered_at'].astype(str), errors="coerce")
    data_file.insert(delivered_day_idx, 'delivered_at_clean', delivered_at_clean)

    data_file = data_file.drop(columns=['delivered_day', 'delivered_at'])
    data_file = data_file.rename(columns = {'delivered_at_clean': 'delivered_at'})


    # Format the columns into date time
    data_file["accepted_at"] = pd.to_datetime(data_file["accepted_at"], errors="coerce")
    data_file["cancelled_at"] = pd.to_datetime(data_file["cancelled_at"], errors="coerce")

    #======================= Remove irrelevant rows =======================#
    restaurant_name_exclusions = "Market|City center|uno|test|Forfait"
    data_file = data_file[
                        ~data_file['restaurant_name'].str.contains(
                        restaurant_name_exclusions,
                           case=False, na=False)
                    ]

    cancellation_reason_exclusion = "rembour|test"
    data_file = data_file[
                        ~data_file["cancellation_reason"].str.contains(
                        cancellation_reason_exclusion, 
                            case=False, na=False)
                    ]
    
    return data_file

file_location = r"C:\Users\user\Downloads\admin-earnings-orders-export_v1.3.1_countryCode=DZ&filters=s_1783292400000_e_1783465199999.csv"
cleaned_data = data_cleaner(file_location)
print(cleaned_data.head())
