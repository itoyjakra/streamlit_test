import streamlit as st
import pandas as pd
from inventory import produce


def make_app():
    """Toy app"""
    prod = pd.DataFrame(produce)

    st.header("Available Items")
    cols_show = ["name", "unit", "price"]
    st.dataframe(prod.loc[:, cols_show])

    consumer_name = st.text_input('your name')
    st.subheader("Select your items")

    consumer_input = []
    for name, unit, price in zip(prod.name, prod.unit, prod.price):
        input_unit = st.text_input(f'{name} (Rs. {price}/{unit})')
        consumer_input.append({"name": name, "unit": input_unit, "unit_price": price})

    df_input = pd.DataFrame(consumer_input)
    df_input["unit"] = pd.to_numeric(df_input["unit"]).fillna(0)
    df_input["unit_price"] = pd.to_numeric(df_input["unit_price"])
    df_input["price"] = df_input["unit"] * df_input["unit_price"]
    total_cost = df_input["price"].sum()

    st.subheader(f"Ordered by {consumer_name}")
    st.dataframe(df_input)
    st.subheader(f"Total cost: Rs. {total_cost}")

    print(consumer_name)
    print(consumer_input)


def main():
    make_app()


if __name__ == "__main__":
    main()
