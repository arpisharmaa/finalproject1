"""
Name: Arpi Sharma
CS230 Section 5
Data: Fast Food Restaurants Across America
URL: https://share.streamlit.io/arpisharmaa/finalproject1/main/finalproject.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from matplotlib import pyplot as plt
MAPKEY = "pk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DApk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DA"

# returns the list of states sorted
def stateslist(dataframe):
    x = dataframe
    states = x['province'].values.tolist()
    final = []
    for y in states:
        if y not in final:
            final.append(y)
    return sorted(final)

def map(state):
    x = pd.read_csv('Fast_Food_Restaurants_8000_sample (1).csv')
    y = x.loc[x['province'] == state]
    st.dataframe(y)
    view_state = pdk.ViewState(latitude=y["latitude"].mean(),longitude=y["longitude"].mean(),zoom=25,pitch=0)
    layer = pdk.Layer('ScatterplotLayer',data=y,get_position='[longitude, latitude]',get_radius=25,get_color=[0,0,255],pickable=True)
    tool_tip = {"html": "Chain:<br/> <b>{name}</b> ","style": { "backgroundColor": "steelblue","color": "white"}}
    map1 = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',initial_view_state= view_state,layers=[layer],tooltip=tool_tip)
    st.pydeck_chart(map1)



st.title("Fast Food in America")
page = st.selectbox("Choose your page", ["Homepage", "Fast Food Restaurants by State", "Map", "Bar Chart", "Amount of Fast Food Restaurants in each State"])
if page == "Homepage":
    from PIL import Image
    image = Image.open('fastfood.jpeg')
    st.image(image)
    st.caption('Fast food restaurants is a growing industry in the United States today. '
               'Especially since the pandemic the industry has grown more and more. '
               'In 2019 there were approximately 194,395 fast food restaurants in the U.S. '
               'and the number is just rising ')
    st.subheader("This website will present data provided by Datafiniti's "
                 "Business Database of a list of over 10,000 fast food restaurants in different graphs and models")
    st.caption('By: Arpi Sharma')
elif page == "Fast Food Restaurants by State":
    def pie(state, dataframe):
        freq = {}

        for entry in dataframe.values:
            if entry[12] == state:
                something = str(entry[10])
                something1 = something.replace("'", "").lower()
                if something1 not in freq:
                    freq[something1] = 1
                else:
                    freq[something1] += 1
        sortedfreq = sorted(freq.values())
        sorted_dict = {}
        x = []
        y = []
        for i in sortedfreq:
            for k in freq.keys():
                if freq[k] == i:
                    sorted_dict[k] = freq[k]

        if len(sortedfreq) <= 10:
            x = freq.keys()
            y = freq.values()
        else:
            for name in sorted_dict:
                if len(x) < 10:
                    x.append(name)
                    y.append(sorted_dict[name])

        plt.pie(y, labels=x, autopct='%.1f%%')
        plt.legend.loc = 'lower left'
        return plt


    # main function that runs the code without returning a value
    def main():
        st.subheader("Select a State to see the top 10 fast food restaurants in that state")
        df = pd.read_csv('Fast_Food_Restaurants_8000_sample (1).csv')
        states_list = stateslist(df)
        x = st.sidebar.selectbox('Select U.S. State for pi chart', states_list)
        st.pyplot(pie(x, df))


    main()
elif page == "Map":
    mapstate = st.sidebar.selectbox('Select U.S. State for Map', stateslist(pd.read_csv('Fast_Food_Restaurants_8000_sample (1).csv')))
    map(mapstate)
elif page == "Bar Chart":
    def horizontalbarchart():
        data = {'AR':13, 'CT':8, 'IL':63, 'NM':18, 'TX':112}
        states = list(data.keys())
        values = list(data.values())
        fig = plt.figure(figsize=(10,5))
        plt.barh(states, values)
        plt.xlabel("Number of McDonalds")
        plt.ylabel("States")
        plt.title("McDonalds Around the Country")
        st.pyplot(fig)
    def main():
        horizontalbarchart()
        st.subheader("The most popular fast food chain in America is McDonalds, but in this graph I will be comparing 5 different states from different regions and the popularity of McDonalds there.")
    main()


elif page == "Amount of Fast Food Restaurants in each State":
    def barchart():
        data = {'MA':161, 'CA':985, 'TX':641, 'MI':300, 'TN':242}
        states = list(data.keys())
        values = list(data.values())
        fig = plt.figure(figsize =(10,5))
        plt.bar(states, values)
        plt.xlabel('States')
        plt.ylabel('# of Restaurants')
        plt.title("Number of Fast Food Restaurants in Each State")
        st.pyplot(fig)
    def main():
        choice = st.radio("Would you like to see a representation of fast food restaurants in different territories?", ("Yes", "No"))
        if choice == "Yes":
            barchart()
            st.subheader("This chart is representative of the amount of fast food restaurants found in different areas of the US.")
        else:
            st.warning("Nothing is displayed because you chose to not view the data")
    main()

