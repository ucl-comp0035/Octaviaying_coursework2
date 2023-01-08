import streamlit as st
import pandas
import requests
import json

base_url = "http://127.0.0.1:5000"


def display_overall():
    url = base_url + '/data'
    res = requests.get(url)
    data = json.loads(res.text)

    df = pandas.DataFrame(data['data'],
                          columns=['Country Name', 'Indicator Name', 'Year', 'Value'])
    st.write("Overall Information")
    st.table(df)


def display_country():
    searchText = st.text_input("Country Name")
    url = base_url + '/country/' + searchText
    res = requests.get(url)
    if res.status_code == 200:
        data = json.loads(res.text)
    else:
        data = {'data': []}
    df = pandas.DataFrame(data['data'],
                          columns=['Country Name', 'Indicator Name', 'Year', 'Value'])
    st.table(df)


def display_indicator():
    searchText = st.text_input("Indicator Name")
    url = base_url + '/indicator/' + searchText
    res = requests.get(url)
    if res.status_code == 200:
        data = json.loads(res.text)
        df = pandas.DataFrame(data['data'],
                              columns=['Country Name', 'Indicator Name', 'Year', 'Value'])
        st.header(searchText)
        st.line_chart(df, x='Year', y='Value')


def display_year():
    searchText = st.text_input("Country")
    searchYear = st.date_input("Year").year
    url = base_url + '/bar/' + searchText + '/' + str(searchYear)
    res = requests.get(url)
    if res.status_code == 200:
        data = json.loads(res.text)
        df = pandas.DataFrame(data['data'],
                              columns=['Country Name', 'Indicator Name', 'Year', 'Value'])
        st.header(searchText + ' in ' + str(searchYear))
        st.bar_chart(df, x='Indicator Name', y='Value')


if __name__ == '__main__':
    st.title("Coursework2")

    tab1, tab2, tab3, tab4 = st.tabs(["All Data", "Country", "Indicator", "Year"])

    with tab1:
        display_overall()
    with tab2:
        display_country()
    with tab3:
        display_indicator()
    with tab4:
        display_year()
