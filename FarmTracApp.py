import pandas as pd
import streamlit as st
from datetime import datetime as dt
from csv import writer

st.set_page_config(layout='wide')
st.title("FarmTrac")
st.subheader("Welcome to FarmTrac!")
st.write("FarmTrac app helps to keep track of farm work activities. Please select from following options:")
AddFarmActivity,SearchFarmActivity,AddWorker,AddFarm = st.tabs(["Add Farm Activity","Search Farm Activity","Add Farm Worker","Add Farm"])

with AddFarmActivity:
    WorkerData = pd.read_csv("datasets\WorkerDim.csv")
    WorkerList = WorkerData["WorkerName"]
    FarmData = pd.read_csv("datasets\FarmDim.csv")
    FarmList = FarmData["FarmName"]
    AddFarmActivityForm = st.form("Add Farm Activity")
    WorkDate = AddFarmActivityForm.date_input(label="Work Date", max_value=dt.today(), value="today")
    FarmName = AddFarmActivityForm.selectbox(label="Farm",options=FarmList)
    WorkerName = AddFarmActivityForm.multiselect(label="Farm Workers",options=WorkerList)
    AddFarmActivityBtn = AddFarmActivityForm.form_submit_button("Add Activity")

with AddFarm:
    AddFarmForm = st.form("Add Farm")
    FarmName = AddFarmForm.text_input("Enter Farm Name:")
    AddFarmBtn = AddFarmForm.form_submit_button("Add Farm")
    if AddFarmBtn:
        if FarmName == '':
            st.error(f"Error: Please enter the farm name!")
        else:
            
            FarmData = pd.read_csv("datasets\FarmDim.csv")
            FarmList = list(FarmData["FarmName"])
            if FarmName in FarmList:
                st.error(f"Error: {FarmName} is already added!")
            else:
                if FarmData.empty:
                    NewFarmId = 1
                else:
                    NewFarmId = FarmData["FarmId"].max() + 1

                NewFarm = [NewFarmId,FarmName,dt.today()]
                #FarmData = FarmData.append(NewFarmData,ignore_index=True)
                with open("datasets\FarmDim.csv",'a',newline='') as f:
                    writerObj = writer(f)
                    writerObj.writerow(NewFarm)
                st.success(f"Success: {FarmName} added!")

with AddWorker:
    AddWorkerForm = st.form("Add Worker")
    WorkerName = AddWorkerForm.text_input("Enter Worker Name:")
    AddWorkerBtn = AddWorkerForm.form_submit_button("Add Worker")
    if AddWorkerBtn:
        if WorkerName == '':
            st.error(f"Error: Please enter the worker name!")
        else:
            WorkerData = pd.read_csv("datasets\WorkerDim.csv")
            WorkerList = list(WorkerData["WorkerName"])
            if WorkerName in WorkerList:
                st.error(f"Error: {WorkerName} is already added!")
            else:
                if WorkerData.empty:
                    NewWorkerId = 1
                else:
                    NewWorkerId = WorkerData["WorkerId"].max() + 1

                NewWorker = [NewWorkerId,WorkerName,dt.today()]
                #FarmData = FarmData.append(NewFarmData,ignore_index=True)
                with open("datasets\WorkerDim.csv",'a',newline='') as f:
                    writerObj = writer(f)
                    writerObj.writerow(NewWorker)
                st.success(f"Success: {WorkerName} added!")