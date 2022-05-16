import requests
import streamlit as st

backend = "http://localhost:8000"

def main():
    
    st.set_page_config(
        page_title="Property Finder",
        page_icon="🏡",
        layout="wide"
    )

    st.title("Magnifying Glass: Singapore Property Landscape")
    
    prop_list = requests.get(backend + '/propnames').json()
    
    form = st.sidebar.form("form", clear_on_submit=True)
    with form:
    
        st.subheader("What type of Property Transactions do you want to see?")

        propname = st.selectbox(
        label='Select Property Project',
        options=prop_list["lists"]
        )

        postal_dist = st.selectbox(
            label = "Select Postal District",
            options=['All']+[str(n) for n in range(1,29)]
            )

        prop_size = st.slider(
            label = "Select Property Size (SQFT)",
            min_value=100,
            max_value=8000,
            value=(100,8000),
            step = 100
        )

        min_year = st.selectbox(
            label = "Properties Bought After",
            options=['All']+[str(n) for n in range(2000,2016)]
            )

        submit = st.form_submit_button("See Results")

    if submit==False:
        st.image('data/hk2019r.jpg')
        st.caption("Image Credits: Jason Lim 2019")
        st.info("Select parameters on the left to get started, or simply click **See Results**!")

    if submit == True:
        
        st.info("**You've Selected:**")
        
        select_col1, select_col2, select_col3, select_col4 = st.columns(4)

        with select_col1:
            st.subheader("Property Name")
            st.write(propname)
        with select_col2:
            st.subheader("Postal District")
            st.write(postal_dist)
        with select_col3:
            st.subheader("Property Size")
            st.write(str(prop_size[0]) + "sqft to " + str(prop_size[1])+"sqft")
        with select_col4:
            st.subheader("Year of Purchase After")
            st.write(min_year)

        stats = requests.get(
            backend + '/stats', 
            params={"propname": propname,"postdist": postal_dist,"propsize_min": prop_size[0],"propsize_max": prop_size[1],"newsaleyear": min_year}).json()

        count_transactions = stats['stat_dict']['Price Differential (%)']['count']
        
        if count_transactions > 0:

            st.success("**Here's how your selection performed:**")
            st.subheader("Out of " + str(int(count_transactions)) + " transactions")

            result_col1, result_col2, result_col3, result_col4 = st.columns(4)

            with result_col1:
                st.metric(
                label="Average Profit/Loss",
                value = str(round(100*(stats['stat_dict']['Price Differential (%)']['mean']),1)) + "%"
                )
            with result_col2:
                st.metric(
                label="Median Profit/Loss",
                value = str(round(100*(stats['stat_dict']['Price Differential (%)']['50%']),1)) + "%"
                )
            with result_col3:
                st.metric(
                label="Average Annualized Gain/Loss",
                value = str(round(100*(stats['stat_dict']['Annualized Growth']['mean']),1)) + "%"
                )
            with result_col4:
                st.metric(
                label="Median Annualized Gain/Loss",
                value = str(round(100*(stats['stat_dict']['Annualized Growth']['50%']),1)) + "%"
                )

            chart1= requests.get(
                    backend + '/chartprice',
                    params={"propname": propname,"postdist": postal_dist,"propsize_min": prop_size[0],"propsize_max": prop_size[1],"newsaleyear": min_year}
                    ).content

            chart2= requests.get(
                    backend + '/chartgrowth',
                    params={"propname": propname,"postdist": postal_dist,"propsize_min": prop_size[0],"propsize_max": prop_size[1],"newsaleyear": min_year}
                    ).content

            st.image([chart1,chart2])
            
        else:
            st.warning("No transactions found.")
    
if __name__ == "__main__":
    main()