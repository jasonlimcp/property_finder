import requests
import streamlit as st

backend = "http://localhost:8000"

def main():
    
    st.set_page_config(
        page_title="Property Finder",
        page_icon="🏡",
        layout="wide"
    )

    st.title("Analyze Properties Here!")
    
    prop_list = requests.get(backend + '/propnames').json()
    #prop_list_json = prop_list
    
    propname = st.sidebar.selectbox(
        label='Select Property Project',
        options=prop_list["lister"]
        )

    with st.sidebar:
        postal_dist = st.selectbox(
            label = "Select Postal District",
            options=['All']+[str(n) for n in range(1,29)])

        prop_size = st.slider(
            label = "Select Property Size (SQFT)",
            min_value=100,
            max_value=8000,
            value=(100,8000),
            step = 100
        )

        min_year = st.selectbox(
            label = "Properties Bought After",
            options=['All']+[str(n) for n in range(2000,2022)])

        submit = st.button("Calculate")


        #if st.button("Calculate"):
        #    data = requests.get(backend, params={"data": propname})
        #    data_json = data.json()
        #    st.write(data_json["msg"])

    if submit == True:
        with st.container():
            st.write("**You've selected:**")
            st.write("Property Name: "+ propname)
            st.write("Postal District: "+postal_dist)
            st.write("Property Size: "+ str(prop_size[0]) + "sqft to " + str(prop_size[1])+"sqft")
            st.write("Year Built From: "+min_year)
    


    
if __name__ == "__main__":
    main()