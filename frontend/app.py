import requests
import streamlit as st

backend = "http://localhost:8000/propnames"
prop_list = requests.get(backend)

def main():
    
    st.set_page_config(
        page_title="Property Finder",
        page_icon="🏡",
        layout="wide"
    )

    st.title("View Property Stats here:")
        
    st.write(prop_list)
    
    propname = st.selectbox(
        label='Select Property:',
        options=prop_list
        )

    if st.button("Press Here"):
        data = requests.get(backend, params={"data": propname})
        data_json = data.json()
        st.write(data_json["msg"])

    
if __name__ == "__main__":
    main()