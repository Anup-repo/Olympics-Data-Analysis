import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")

df= preprocessor.preprocess(df, region_df)

st.sidebar.header("Olympics data Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio("Select an option",
("Medal Details","Overall Analysis","Country wise Analysis","Athlete details"))


if user_menu=="Medal Details":
    st.sidebar.header("Medal Details")

    year,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_details = helper.fetch_medal_detail(df,selected_year, selected_country)
    if selected_year =="Overall" and selected_country =="Overall":
        st.title("Overall Details")
    if selected_year !="Overall" and selected_country =="Overall":
        st.title("Medal Details in "+ str(selected_year))
    if selected_year =="Overall" and selected_country !="Overall":
        st.title("Overall performance by "+ selected_country)
    if selected_year !="Overall" and selected_country !="Overall":
        st.title(selected_country+" Performance in "+ str(selected_year))
    st.table(medal_details)

if user_menu == "Overall Analysis":
    edition = df["Year"].unique().shape[0]-1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nation = df["region"].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Edition")
        st.header(edition)
    with col2:
        st.header("Host")
        st.header(cities)
    with col3:
        st.header("Sports")
        st.header(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.header(events)
    with col2:
        st.header("Atheletes")
        st.header(athletes)
    with col3:
        st.header("Nation")
        st.header(nation)
    
    st.title("Participating nations over the year")
    nation_overtime = helper.data_overtime(df, "region")
    fig = px.line(nation_overtime,x="Edition",y="region")
    st.plotly_chart(fig)

    st.title("Events over the year")
    event_overtime = helper.data_overtime(df, "Event")
    fig = px.line(event_overtime,x="Edition",y="Event")
    st.plotly_chart(fig)

    st.title("Number of sports over time")
    fig,ax = plt.subplots(figsize=(20,20))
    x= df.drop_duplicates(["Year","Sport","Event"])
    ax = sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype("int"),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Atheletes")
    sport = df["Sport"].unique().tolist()
    sport.sort()
    sport.insert(0,"Overall")
    selected_sport = st.selectbox("Select sport",sport)
    most_successful=helper.most_successful(df,selected_sport)
    st.table(most_successful)

if user_menu == "Country wise Analysis":
    st.sidebar.header("Countrywise Info")
    country = df["region"].dropna().unique().tolist()
    country.sort()
    country.insert(0,"Overall")
    selected_country = st.sidebar.selectbox("Select country",country)
    new_df = helper.contry_medal_info(df, selected_country)
    st.title(selected_country +" Medal counts")
    fig = px.line(new_df,x="Year",y="Medal")
    st.plotly_chart(fig)

    st.title(selected_country +" excels in following sport")
    try:
        new_df = helper.country_heatmap(df, selected_country)
        fig,ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(new_df.pivot_table(index="Sport",columns="Year",values="Medal",aggfunc="count").fillna(0),annot=True)
        st.pyplot(fig)
    except:
        if(selected_country=="Overall"):
            st.title("Plz select country")
        else:
            st.title(selected_country +" has won no Medal tillnow")

    st.title("Top atheletes of "+selected_country)
    top_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top_df)

if user_menu=="Athlete details":
    st.title("Men vs Women")
    final = helper.men_vs_women(df)
    fig = px.line(final,x="Year",y=["Male","Female"])
    st.plotly_chart(fig)

    st.title("Weight vs Height")
    sport = df["Sport"].unique().tolist()
    sport.sort()
    sport.insert(0,"Overall")
    selected_sport = st.selectbox("Select sport",sport)
    temp_df = helper.weigth_vs_height(df, selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df["Weight"],temp_df["Height"],hue=temp_df["Medal"],style=temp_df["Sex"],s=60)
    st.pyplot(fig)