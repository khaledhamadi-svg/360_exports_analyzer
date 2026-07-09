import pandas as pd

def data_cleaner(input_file):
    """
    input: admin dashboard export DataFramce
    output: cleaned DataFrame
    """
    data_file = pd.read_csv(input_file)

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

    #======================= Remove duplicate columns =======================#
    col_names = pd.Series(data_file.columns)
    for dup in col_names[col_names.duplicated()].unique(): 
        dup_indices = col_names[col_names == dup].index
        
        for i, idx in enumerate(dup_indices):
            if i > 0:
                col_names[idx] = f"{dup}_{i}"
    
    data_file.columns = col_names
    
    return data_file

# df = pd.read_csv(r"C:\Users\user\Downloads\admin-earnings-orders-export_v1.3.1_countryCode=DZ&filters=s_1783378800000_e_1783551599999.csv")
# test = data_cleaner(df)
# print(test.head(10))