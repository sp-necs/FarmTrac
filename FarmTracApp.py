import pandas as pd
import streamlit as st
from datetime import datetime as dt
from csv import writer

st.set_page_config(layout='wide')
st.title("FarmTrac")
st.subheader("Welcome to FarmTrac!")
st.write("FarmTrac app helps to keep track of farm work activities. Please select from following options:")
AddFarmActivity,SearchFarmActivity,AddWorker,AddFarm = st.tabs(["Add Farm Activity","Search Farm Activity","Add Farm Worker","Add Farm"])

with AddFarm:
    AddFarmForm = st.form("Add Farm",clear_on_submit=True)
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
    AddWorkerForm = st.form("Add Worker",clear_on_submit=True)
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

with AddFarmActivity:
    WorkerData = pd.read_csv("datasets\WorkerDim.csv")
    WorkerList = WorkerData["WorkerName"]
    FarmData = pd.read_csv("datasets\FarmDim.csv")
    FarmList = FarmData["FarmName"]
    AddFarmActivityForm = st.form("Add Farm Activity",clear_on_submit=True)
    WorkDate = AddFarmActivityForm.date_input(label="Work Date", max_value=dt.today(), value="today")
    FarmName = AddFarmActivityForm.selectbox(label="Farm",options=FarmList,index=None)
    WorkerName = AddFarmActivityForm.multiselect(label="Farm Workers",options=WorkerList)
    Description = AddFarmActivityForm.text_input("Work Description")
    AddFarmActivityBtn = AddFarmActivityForm.form_submit_button("Add Activity")
    if AddFarmActivityBtn:
        if FarmName == None or WorkerName == '':
            st.error("Error: Please enter the Farm and Worker details!")
        else:
            NewFarmWorkId = 0
            FarmWorkData = pd.read_csv("datasets\FarmWork.csv")
            if FarmWorkData.empty:
                NewFarmWorkId = 1
            else:
                NewFarmWorkId = FarmWorkData["FarmWorkId"].max() + 1
            for worker in WorkerName:
                NewFarmWork = [NewFarmWorkId, WorkDate, FarmName, worker, Description]
                with open("datasets\FarmWork.csv",'a',newline='') as f:
                    writerObj = writer(f)
                    writerObj.writerow(NewFarmWork)
                NewFarmWorkId = NewFarmWorkId + 1
            st.success("Success: Farm Activity added!")

with SearchFarmActivity:
    FarmActivityData = pd.read_csv("datasets\FarmWork.csv")
    FarmData = pd.read_csv("datasets\FarmDim.csv")
    FarmActivityData["FarmWorkDate"] = pd.to_datetime(FarmActivityData["FarmWorkDate"]).dt.date
    SearchFarmActivityForm = st.form("Search Farm Activity")
    StartDate = SearchFarmActivityForm.date_input(label="From Date", max_value=dt.today(),value="today")
    EndDate = SearchFarmActivityForm.date_input(label="To Date", max_value=dt.today(),value="today")
    SearchFarmName = SearchFarmActivityForm.selectbox(label="Farm Name",options=FarmData["FarmName"],index=None)
    SearchFarmActivityBtn = SearchFarmActivityForm.form_submit_button("Search Activity")
    if SearchFarmActivityBtn:
        if StartDate>EndDate:
            st.error("Error: Please enter correct dates!")
        else:
            if FarmActivityData.empty:
                st.error("Error: There is no farm activity data!")
            else:
                if SearchFarmName == None:
                    SearchResult = FarmActivityData[(FarmActivityData["FarmWorkDate"]>=StartDate) & (FarmActivityData["FarmWorkDate"]<=EndDate)]
                    SearchFarmActivity.write(SearchResult)