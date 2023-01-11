import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import re


#__________________________________________________________________________________________________________________________________________________________________
# Dashboard structure
#__________________________________________________________________________________________________________________________________________________________________
st.set_page_config(page_title="R2R Members", page_icon="🔦", layout="wide", initial_sidebar_state="expanded")

# Hide index when showing a table. CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# data
df_bbdd =         pd.read_csv('Members_DDBB.csv',sep=';').dropna(how = 'all')             # Base de da
df_bbdd = df_bbdd.sort_values(by=['ID_MASTER', 'Member_Type_2'])


#__________________________________________________________________________________________________________________________________________________________________
# MAIN PAGE
#__________________________________________________________________________________________________________________________________________________________________
with st.expander("Introducción"):
            st.markdown('<div style="text-align: justify;">**¿Qué es esto?**</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align: justify;">Un visualizador de los datos de Miembros reportados por Partners R2R. Su función es facilitar la comprensión de los tipos de miembros que tienen los Partners de R2R y así idealmente reconocer caminos para asegurar que Partners puedan reportar metricas robustas a la campaña.</div>', unsafe_allow_html=True)

            st.markdown('<div style="text-align: justify;">**¿Qué información tiene?**</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True)

            st.markdown('<div style="text-align: justify;">**¿Hacia dónde va?**</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True)

            st.markdown('<div style="text-align: justify;">**Proceso de análisis**</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True)





#__________________________________________________________________________________________________________________________________________________________________
# SIDEBAR
#__________________________________________________________________________________________________________________________________________________________________
st.sidebar.image("R2R_RGB_PINK.png", width=150)
st.sidebar.subheader("R2R partner's members analysis.\n Experimental phase")

#Multiselector for partner selection
partner_selection = st.sidebar.multiselect("Select partners", options=df_bbdd["Official_Name"].unique(),)
all_options = st.sidebar.checkbox("All Partners")
if all_options:
    partner_selection = df_bbdd["Official_Name"].unique().tolist()
df_bbdd_partner = df_bbdd.query('Official_Name == @partner_selection')  #Filter by source of information

#Multiselector for level of partners

aggregator_index = st.sidebar.multiselect("Select levels of members", options=df_bbdd_partner["Aggregator_operator"].unique(),default=df_bbdd_partner["Aggregator_operator"].unique())
all_options = st.sidebar.checkbox("All options")
if all_options:
    aggregator_index = df_bbdd_partner["Aggregator_operator"].unique().tolist()
df_bbdd_selection = df_bbdd_partner.query('Aggregator_operator == @aggregator_index')  #Filter by source of information

#______________________________
st.subheader('Results of members identification analysis')

#______________________________

total_partners      = df_bbdd_selection['ID_MASTER'].nunique()
total_members       = df_bbdd_selection['Member_Name'].nunique()
total_members_type  = df_bbdd_selection['Member_Type'].nunique()
total_members_Categories  = df_bbdd_selection['Member_Type_2'].nunique()
#total_members_aggregator = df_bbdd_selection['Aggregator_operator'].value_counts()['Aggregator']
#total_members_operator = df_bbdd_selection['Aggregator_operator'].value_counts()['Operator']

col1, col2, col3, col4 = st.columns((1.5,1,1,1))   #https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/

col1.metric("Partners reporting members list",total_partners)
col4.metric("Total Members",total_members)
col3.metric("Members types",total_members_type)
col2.metric("Members categories",total_members_Categories)
#col1.metric("Nº Aggregators",total_members_aggregator)
#col2.metric("Nº Operators",total_members_operator)
st.caption('<div style="text-align: left">Source: General Information survey</h1></div>', unsafe_allow_html=True)
st.text("")


#___________________________________________________________________________________________________________________________________________________________
# TREEAMAP AND SUNBURST
#___________________________________________________________________________________________________________________________________________________________

#tree map

df_tree = pd.DataFrame(df_bbdd_selection,columns=['Member_Type_2','Member_Type','Member_Name','Official_Name'])
df_tree = df_tree.groupby(['Member_Type_2','Member_Type'])['Member_Name'].count()              # aggregating by number of persons
df_tree = df_tree.groupby(['Member_Type_2','Member_Type']).size().reset_index(name='Member_Name')   # adding count agg as column

fig = px.treemap(df_tree, path=[px.Constant("Members"),'Member_Type_2','Member_Type'], values = 'Member_Name')
fig.update_traces(root_color="lightgray")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

#sunburst

fig1 = px.sunburst(data_frame = df_bbdd_selection, path = ['Member_Type_2','Member_Type','Member_Name'],values = None)

#pie
df_bbdd_selection_pie = pd.DataFrame(df_bbdd_selection,columns=['Aggregator_operator','Member_Name'])
df_bbdd_selection_pie = df_bbdd_selection_pie.groupby(['Aggregator_operator'])['Member_Name'].count()              # aggregating by number of persons


if  len(partner_selection)+len(aggregator_index) == 0:
    st.caption('')
else:
    st.caption('Explore the tree map by selecting any analitical category')
    st.plotly_chart(fig)
    st.caption('Explore the sunburst map by selecting any analitical category')
    st.plotly_chart(fig1)
    st.caption('Frecuency of members by level Aggregator & Operator')
    st.write(df_bbdd_selection_pie)
