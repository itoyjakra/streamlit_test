import streamlit as st
import pandas as pd
from inventory import produce


def make_app(df_produce):
    """Toy app"""
    # prod = pd.DataFrame(produce)

    st.header("Available Items")
    # cols_show = ["name", "unit", "price"]
    # st.dataframe(df_produce.loc[:, cols_show])

    consumer_name = st.text_input('your name')
    st.subheader("Select your items")

    consumer_input = []
    for name, unit, price in zip(df_produce.ITEM, df_produce.UNIT, df_produce.PRICE):
        with st.container():
            col1, col2 = st.columns([2, 1])
            input_unit = col1.text_input(f'{name} (Rs. {price}/{unit})')
            if input_unit == "":
                continue
            total_price = int(input_unit) * float(price)
            col2.text(f"Rs. {total_price}")
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
    df_market = pd.read_csv("Chetana_Marketing_v2.0.csv")
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
