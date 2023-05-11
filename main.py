import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("UpWork Data Analysis to find out the skills in Demand")
st.write("**About dataset:** \nThe dataset is curated by scraping publically available job listings on Upwork.com. The data is a sample of about ~9500 jobs listed on upwork.com which made up ~6.25% of total jobs available on upwork at the time of scraping. The dataset can be found at https://www.kaggle.com/datasets/hashiromer/upwork-jobs")

# LOADING DATASET
df1 = pd.read_csv("dataset/1_6_2023_general.csv")
df2 = pd.read_csv("dataset/1_3_2023_general.csv")
df3 = pd.read_csv("dataset/1_1_2023_general.csv")
upwork = pd.concat([df3,df2,df1])


## 1) In Demand services
st.subheader("1) Most in demand services on the platform")
st.write("refers to the services that are currently sought after the most by clients on the platform. This information can be useful for service providers who want to focus on offering the most in-demand services to increase their chances of getting hired.")

service = upwork.groupby('occupations_category_pref_label').size()
services = service.to_frame().reset_index()
services.columns.values[1]='total'

# plottting a bar graph to see the services in demands on upwork
fig, ax = plt.subplots()
ax.bar(services['occupations_category_pref_label'], services['total'], color="mediumseagreen")
ax.set_xticklabels(services['occupations_category_pref_label'], rotation=90)

# this is to add the label on top of the bars
for i in range(len(services['total'])):
    ax.text(i, services['total'][i], services['total'][i], ha='center', va='bottom')

with st.container():
    chart1, table1 = st.columns(2)
    with chart1:
        st.pyplot(fig)
    with table1:
        st.table(services)
        
## 2) In Demand subservices
st.write("##")
st.write("##")
st.subheader("2) Most in demand subservices of services on Upwork")

service_name = ('Web, Mobile & Software Dev','Accounting & Consulting','Admin Support','Customer Service','Data Science & Analytics','Design & Creative','Engineering & Architecture','IT & Networking','Legal','Sales & Marketing','Translation','Writing')

# Inserting a SELECTBOX for user to choose the subservices data
subservice = st.selectbox('Select the service to see the subservices graph:',(service_name))

def subservices(subservice):
    x1 = upwork.loc[upwork['occupations_category_pref_label']==f'{subservice}'].groupby('occupations_oservice_pref_label').size()
    x1 = x1.to_frame().reset_index()
    x1.columns.values[1] = 'total'
    return(x1)

x1 = subservices(subservice)

fig2, ax = plt.subplots()
ax.bar(x1['occupations_oservice_pref_label'], x1['total'], color="mediumseagreen")
ax.set_xticklabels(x1['occupations_oservice_pref_label'], rotation=90)
    
for i in range(len(x1['total'])):
    ax.text(i, x1['total'][i], x1['total'][i], ha='center', va='bottom')

with st.container():
    chart2, table2 = st.columns(2)
    with chart2:
        st.pyplot(fig2)
    with table2:
        st.table(x1)


    

## Q3) hourly vs fixbudget ratios
st.write("##")
st.write("##")
st.subheader("3) Fixed budget vs Hourly services ratios preferred by clients based on services")
st.write("This heading suggests that the analysis examines the preference of clients for fixed budget versus hourly services for different types of services. The ratios will give an idea of the distribution of the type of contracts preferred by clients for different services.")
st.write("##")

fixbudget = upwork.loc[upwork['type']=='fixed_budget'].groupby('occupations_category_pref_label').size().to_frame().reset_index()
hourly = upwork.loc[upwork['type']=='hourly'].groupby('occupations_category_pref_label').size().to_frame().reset_index()
fixbudget.columns.values[1] = 'total'
hourly.columns.values[1] = 'total'

fig3, ax = plt.subplots(figsize=(8,5))
ax.bar(fixbudget['occupations_category_pref_label'], fixbudget['total'], label='fixed budget',color='lightgreen')
ax.bar(hourly['occupations_category_pref_label'], hourly['total'], bottom=fixbudget['total'], label='hourly',color='mediumseagreen')
ax.legend()
ax.set_ylabel('total jobs')
ax.set_title('Stacked Bar Chart')
ax.set_xticklabels(fixbudget['occupations_category_pref_label'],rotation=90)

st.pyplot(fig3)

## 4) Average hourly vs fixed budget rates
st.write("##")
st.write("##")
st.subheader("4) Average hourly and fixed budget rates of services in $")
st.write("The given topic refers to the average rates charged by freelancers on Upwork for their services. Hourly rates are charged by freelancers for their services on an hourly basis, while fixed budget rates refer to the total cost for completing a specific project. This information can be useful for clients looking to hire freelancers on Upwork, as it provides an insight into the expected costs for their desired services.")
st.write("##")
fixbudget_avg = upwork.loc[upwork['type']=='fixed_budget'].groupby('occupations_category_pref_label').mean('amount_amount').reset_index()

hourly_avg = upwork.loc[upwork['type']=='hourly'].groupby('occupations_category_pref_label').mean('hourly_rate').reset_index()

fig4, axs = plt.subplots(1,2,figsize=(15,5))
axs[0].bar(hourly_avg['occupations_category_pref_label'],hourly_avg['hourly_rate'],color="mediumseagreen")
axs[1].bar(fixbudget_avg['occupations_category_pref_label'],fixbudget_avg['amount_amount'],color="mediumseagreen")

axs[0].set_title('hourly cost average of services')
axs[1].set_title('fixed budget cost average of services')

axs[0].set_xticklabels(hourly_avg['occupations_category_pref_label'],rotation=90)
axs[1].set_xticklabels(fixbudget_avg['occupations_category_pref_label'],rotation=90)


for i in range(len(hourly_avg['hourly_rate'])):
    axs[0].text(i,hourly_avg['hourly_rate'].round()[i],hourly_avg['hourly_rate'].round()[i],ha='center')

for i in range(len(hourly_avg['hourly_rate'])):
    axs[1].text(i,fixbudget_avg['amount_amount'].round()[i],fixbudget_avg['amount_amount'].round()[i],ha='center',va='bottom')
 
st.pyplot(fig4)


## 5) Clients & Country
st.write("##")
st.subheader("5) Representation of country with the most number of clients posting for freelancing work")
st.write("the given world map is an interactive representation of the number of clients who posted job in this 3 months period from every country.")

upwork_location = upwork.groupby('client_location_country').size().to_frame().reset_index()
upwork_location.columns.values[1] = 'total'

# Create a choropleth map
fig5 = px.choropleth(upwork_location, locations='client_location_country', locationmode='country names',color='total',projection='natural earth',color_continuous_scale=px.colors.sequential.Greens)

fig5.update_layout(
    width=700,
    height=600,
)

st.plotly_chart(fig5)
