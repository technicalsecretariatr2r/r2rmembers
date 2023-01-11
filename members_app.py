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
st.subheader("Introduction")

tab1, tab2, tab3, tab4 = st.tabs(["¿Qué es esto?", "¿Qué información tiene?", "¿Hacia dónde va?","Proceso de análisis"])

with tab1:
   st.markdown('Un visualizador de los datos de miembros reportados por Partners R2R. Su función es facilitar la comprensión de los tipos de miembros que tienen los Partners de R2R y así idealmente reconocer caminos para asegurar que Partners puedan reportar metricas robustas a la campaña')
            
with tab2:
   st.markdown('Una base de datos de los miembros reportados por los Partners de R2R en General Information Survey. Todo clasificado por categorías y tipos de miembros, también los miembros se idenificaron como Operators y Agreggators.')
            
with tab3:
   st.markdown('Busca ser una plataforma interactiva para explorar las características de los miembros que están vinculados a los partners, y por ende vinculados a la campaña R2R. Todo esto para facilitar la toma de decisiones en el diseño de la futura encuesta Proceed.')
   
with tab4:
   st.markdown('Para el análisis de la lista de miembros se desarrollaron los siguientes pasos:\n- Se generó una nueva base de datos con toda la información que entregaron los Parners sobre sus miembros.\n- Cuando no existía información disponible para identificar y categorizar a un miembros, se googlearon aquellos miembros y se completó la información pendiente.\n- Se desarrolló una categorización de los miembros en diferentes niveles.\n- Se clasificó como Aggregators aquellos Members que engloban la relación entre varias otras organizaciones.\n- Se clasificó como Operators aquellos Members que ejecutan un plan de acción sobre algun sistema de impacto principalmente de una forma autónoma.\n Este análisis no categoriza a los Partners como Aggregators o Operators. Sólo lo hace con los miembros reportados.')

st.markdown("""----""")

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

total_partners      = df_bbdd_selection['ID_MASTER'].nunique()
total_members       = df_bbdd_selection['Member_Name'].nunique()
total_members_type  = df_bbdd_selection['Member_Type'].nunique()
total_members_Categories  = df_bbdd_selection['Member_Type_2'].nunique()
#total_members_aggregator = df_bbdd_selection['Aggregator_operator'].value_counts()['Aggregator']
#total_members_operator = df_bbdd_selection['Aggregator_operator'].value_counts()['Operator']

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
            st.markdown(' ⬅️ Check out the sidebar to select information. You can select multiples options.')
else:
            st.subheader('Results of members identification analysis')
            col1, col2, col3, col4 = st.columns((1.5,1,1,1))   #https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/
            col1.metric("Partners reporting members list",total_partners)
            col4.metric("Total Members",total_members)
            col3.metric("Members types",total_members_type)
            col2.metric("Members categories",total_members_Categories)
            #col1.metric("Nº Aggregators",total_members_aggregator)
            #col2.metric("Nº Operators",total_members_operator)
            st.caption('<div style="text-align: left">Source: General Information survey</h1></div>', unsafe_allow_html=True)
            st.text("")
            st.markdown('Explore the tree map by selecting any analitical category. It is possible to zoom in for getting into the details')
            st.plotly_chart(fig)
            st.markdown('Explore the sunburst map by selecting any analitical category. It is possible to zoom in for getting into the details')
            st.plotly_chart(fig1)
            st.markdown('Frecuency of members by level Aggregator & Operator')
            st.write(df_bbdd_selection_pie)
            with st.expander("Chek out the raw data"):
                        st.write(df_bbdd_selection) 
