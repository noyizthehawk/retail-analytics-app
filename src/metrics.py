from .schema import normalize_column_names


def calculate_total_sales(df):
    return df["sales"].sum()
def calculate_total_quantity(df):
    return df["quantity"].sum()
def calculate_total_orders(df):
    return df["order_id"].nunique()
def calculate_avg_order_value(df):
    return df["sales"].mean()
def calculate_total_profit(df):
    return df["profit"].sum()
def calculate_total_customers(df):
    return df["customer_id"].nunique()
def calculate_summary_metrics(df):
    if "customer_id" in df.columns:
        return {
            "total_sales": calculate_total_sales(df),
            "total_quantity": calculate_total_quantity(df),
            "total_orders": calculate_total_orders(df),
            "avg_order_value": calculate_avg_order_value(df),
            "customer_id": calculate_total_customers(df)
        }
    else:
         return {
            "total_sales": calculate_total_sales(df),
            "total_quantity": calculate_total_quantity(df),
            "total_orders": calculate_total_orders(df),
            "avg_order_value": calculate_avg_order_value(df),
        }







