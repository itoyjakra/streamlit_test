import streamlit as st
import pandas as pd

PRICE_TABLE = "Chetana_Marketing_v3.0.csv"


def display_numbers(unit):
    if unit in ["KG", "PIECE"]:
        return 1, unit
    elif "GM" in unit:
        num, _ = unit.split()
        return int(num), "GM"


def make_app(df_input):
    """Toy app"""

    st.header("Available Items")
    consumer_name = st.text_input('your name')

    item_types = df_input.TYPE.unique()
    consumer_input = []
    for item_type in item_types:
        df_produce = df_input.loc[df_input.TYPE == item_type].copy()
        st.subheader(f"{item_type}")
        for name, unit, price in zip(df_produce.ITEM, df_produce.UNIT, df_produce.PRICE):
            with st.container():
                col1, col2 = st.columns(2)
                input_unit = col1.number_input(f'{name} (Rs. {price}/{unit})', 0, 10)
                total_price = input_unit * float(price)
                display_quantity, display_unit = display_numbers(unit)
                display_quantity *= input_unit
                col2.text(f"Rs. {total_price}  [{display_quantity} {display_unit}]")
                consumer_input.append({"name": name, "unit": input_unit, "unit_price": price})

    df_input = pd.DataFrame(consumer_input)
    df_input["unit"] = pd.to_numeric(df_input["unit"]).fillna(0)
    df_input["unit"] = pd.to_numeric(df_input["unit"], downcast="integer")
    df_input["unit_price"] = pd.to_numeric(df_input["unit_price"])
    df_input["price"] = df_input["unit"] * df_input["unit_price"]
    total_cost = df_input["price"].sum()

    st.subheader(f"Ordered by {consumer_name}")
    st.dataframe(df_input.loc[df_input.unit > 0])
    st.subheader(f"Total cost: Rs. {total_cost}")


def get_price_table():
    """Returns the weekly price table in a dataframe"""
    df_market = pd.read_csv(PRICE_TABLE)
    cols_select = ['CODE', 'সব্জি [VEGETABLES]', 'UNIT', 'PRICE']
    df_market = df_market.loc[:, cols_select]
    # df_market.columns = ['CODE', 'VEGETABLES', 'UNIT', 'PRICE']
    df_market.columns = ['CODE', 'ITEM', 'UNIT', 'PRICE']
    df_market = df_market.dropna(axis=0, subset=["PRICE"])

    df_codes = df_market[df_market.CODE == "CODE"].copy()
    type_indices = df_market[df_market.CODE == "CODE"].index

    df_market.loc[:, "TYPE"] = "VEGETABLES"
    for index in type_indices:
        df_market.loc[index:, "TYPE"] = df_codes.loc[index, "ITEM"]
    df_market = df_market.drop(type_indices)

    return df_market


def main():
    df_price = get_price_table()
    make_app(df_price)


if __name__ == "__main__":
    main()
