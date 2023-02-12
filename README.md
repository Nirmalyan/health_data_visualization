# Apple Health Data 

This repository contains code to extract fields from Apple's XML health data and showcases metrics in a dashboard.  

## Problem Statement 

The Health app in iOS allows the users to access all the health related data collected from other apps and devices. Although there are features to analyze data and identify trends in the app, Apple does not provide an alternative method to view on desktops or bigger screens. The goal of the project is to extract data from Health app, build a dashboard in PowerBI so that I can find some insights about my health and be better informed.

## Data 

I exported the data from the Apple's Health app (dated from March 21 - Oct 21) which when extracted is a XML file with 350K lines at 105 MB. The dataset is not uploaded owing to privacy concerns and large size. The subsequent updates were cumbersome, as it required manually uploading the data to the computer and running the xml parser every time. So I decided to build ETL pipeline to automate the entire process. 

## ETL Pipeline

![alt text](https://github.com/Nirmalyan/health_data_visualization/blob/main/screenshots/awsops.png?raw=True)

1) The health data is exported in JSON format automatically everyday through a REST API call made to the Lambda function
2) The Lambda function receives the JSON data and uploads to specified S3 bucket. 
3) An Airflow instance hosted on an EC2 listens for changes in the S3 bucket. 
4) Whenever there is a change on S3, the data is normalized and inserted into a RDS database. 
5) The updated data can be viewed on the PowerBI dashboard. 

## Screenshots 

![alt text](https://github.com/Nirmalyan/health_data_visualization/blob/main/screenshots/health_report.png?raw=True)


## Conclusion 

After analyzing the trends and metrics in the data, The following assumptions can be made, 

* The lockdown in India (April to June) had adverse effect on my physical activity. My daily walk count and time spent exercising are really low for the first few months. However my daily activity improved drastically during August right after moving to US. It is because walking is my primary mode of transport. The trendline also indicates the positive growth direction. 

* Analyzing the heart beat over the months indicates that there were two instances where the heart rate was abnormal. After looking at the data, it was calibration error from the device. 

* Other metrics like blood oxygen and headphone audio exposure levels were well in the healthy range. 

## Future Objectives 

* Host the dashboard.
* Add more metrics and overhaul the design.
* Find a way to refresh the data periodically.  