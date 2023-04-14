import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np
import seaborn as sns
import plotly.express as px
import datetime
from PIL import Image
from sklearn import model_selection

st.set_page_config(
        page_title="SalaryPredictor",
        page_icon="chart_with_upwards_trend",
        layout="wide",
)

df = pd.read_csv("data//sal.csv")
st.title("Salary Predictor")

image = Image.open('data//sal.jpeg')
col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    st.image(image,width=400)
with col3:
    st.write("")

nav = st.sidebar.radio("Navigation",["Home","Prediction","Contribute"])
if nav == "Home":
         if st.checkbox("Show Table"):
                     st.table(df)
         graph = st.selectbox("What kind of Graph ? ",["NumberOfJobs Vs Company","NumberOfJobs Vs Title","TotalCompensationDistribution","NoOfEmployeesBasedOnLocation Vs Location","GenderDistribution","RaceDistribution","EducationBackgroundDistribution","EmployeesInTop5","Experience Vs Salary"])
         if graph == "NumberOfJobs Vs Company":
            top_companies = df["company"].value_counts().head(10)
            company=np.array(top_companies.index)
            fig = px.bar(df,x = top_companies.index, y = top_companies.values,hover_name = top_companies.values,template = "ggplot2",
            labels = {"x" : "Company" , "y" : "Number of Jobs" },color=company)
            st.plotly_chart(fig)

         if graph == "NumberOfJobs Vs Title":
            top_comp = df["title"].value_counts()
            color=np.array(top_comp.index)
            fig = px.bar(x = top_comp.index, y= top_comp.values,labels = {"x" : "Title","y" : "Number of Current Jobs"},
             title = "Number of Workers in Each Job Title",template = "ggplot2",color=color)
            #fig.show()
            st.plotly_chart(fig)

         if graph=='TotalCompensationDistribution':
            fig=px.box(df, x = "totalyearlycompensation",title = "Total Compensation Distribution", template = "ggplot2",labels = { "totalyearlycompensation" : "Compensation"})
            st.plotly_chart(fig)

         if graph=='NoOfEmployeesBasedOnLocation Vs Location':
            loctn = df["location"].value_counts()
            color=loctn.index
            fig=px.bar(x= loctn.index, y = loctn.values, template = "plotly_dark",labels = {"x" : "Locations","y" : "Number of Employee based on location"},title = "Jobs based on Locations",color=color)
            st.plotly_chart(fig)
         
         if graph=='GenderDistribution':
            fig=px.pie(df, names = df["gender"].value_counts().index, values = df["gender"].value_counts().values,title = "Gender Distribution",template = "presentation")
            st.plotly_chart(fig)

         if graph=='EducationBackgroundDistribution':
            fig=px.pie(df, names = df["Education"].value_counts().index, values = df["Education"].value_counts().values,title = "Education Background Distribution Of Employee",template = "presentation")
            st.plotly_chart(fig)

         if graph=='RaceDistribution':
            fig=px.pie(df, names = df["Race"].value_counts().index, values = df["Race"].value_counts().values,title = "Race Distribution",template = "presentation")
            st.plotly_chart(fig)
         if graph=='EmployeesInTop5':
            top_5_com = ["Amazon" ,"Microsoft" ,"Google","Facebook","Apple"]
            com_edu = df[df["company"].apply(lambda x: x in top_5_com )]
            com_edu = com_edu[["company", "Education"]]
            fig=px.histogram(com_edu, x = "company", barmode = 'group',color = "Education", 
                template = "ggplot2",
                labels ={"company":"Company","count":"Number of Employees"},)
            st.plotly_chart(fig)
         if graph=='Experience Vs Salary':
            fig = px.scatter(df, x="yearsofexperience", y="totalyearlycompensation", color="title",
                 size='yearsatcompany', hover_data=['title','company'])
            st.plotly_chart(fig)
            

if nav == "Contribute":
    st.header("Contribute to our dataset")
    ct=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ct=ct.replace ("-", "/")
    company=st.text_input('Enter the Company')
    location=st.text_input('Enter the Location')
    ex = st.number_input("Enter your Experience",0.0,20.0)
    sal = st.number_input("Enter your Salary",0.00,1000000.00,step = 1000.0)
    ywfc = st.number_input("Enter the years you worked for company",0.00,1000000.00,step = 1000.0)
    profession=st.selectbox("What is Your Profession ",['Software Engineer','Software Engineering Manager','Product Manager'])
    gender=st.selectbox("Gender?",['male','Female'])
    Race=st.selectbox("Race?",['White','Black','Hispanic','Asian','Indian'])
    Education=st.selectbox("Education?",['Some College','PhD','Masters Degree','Bachelors Degree'])
    if st.button("submit"):
        to_add= {"timestamp":[ct],"company":[company],"title":[profession],"totalyearlycompensation":[sal],"location":[location],
        "yearsofexperience":[ex],"yearsatcompany":[ywfc],"gender":[gender],"Race":[Race],"Education":[Education]}
        to_add = pd.DataFrame(to_add)
        to_add.to_csv("data//sal.csv",mode='a',header = False,index=False)
        st.success("Submitted")

if nav == "Prediction":
    st.header("Know your Salary")
    profession=st.selectbox("What is Your Profession ",['Software Engineer','Software Engineering Manager','Product Manager'])
    sdf=None
    if profession=='Software Engineer':
        sdf=df[df['title']=='Software Engineer']
    elif profession=='Software Engineering Manager':
        sdf=df[df['title']=='Software Engineering Manager']
    else:
        sdf=df[df['title']=='Product Manager']
    sdf=sdf[['yearsofexperience','totalyearlycompensation']]
    x = np.array(df['yearsofexperience']).reshape(-1,1)
    y = np.array(df['totalyearlycompensation']).reshape(-1,1)
    alg1=LinearRegression()
    alg1.fit(x,y)
    val = st.number_input("Enter you exp",0.00,20.00,step = 0.25)
    val = np.array(val).reshape(-1,1)
    pred =alg1.predict(val)[0]
    if st.button("Predict"):
        st.success(f"Your predicted salary is {round(pred[0])}")









    
         
         

        



