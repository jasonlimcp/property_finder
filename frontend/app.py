import io
import requests
import streamlit as st

backend = "http://localhost:8000/test"


def main():
    st.set_page_config(
        page_title="Property Finder",
        page_icon="🏡",
        layout="wide"
    )

    st.title("Property Finder")

    year = st.radio("Year of Completion", ("2005", "2006"), key="year")

    if st.button("Press Here"):
        data = requests.get(backend, params={"data": year})
        data_json = data.json()
        st.write(data_json["msg"])

    
if __name__ == "__main__":
    main()