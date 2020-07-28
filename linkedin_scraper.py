# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:38:33 2020

@author: Luiz Otavio
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import pandas as pd
import os


def get_jobs_linkedin(email, password, num_jobs, search_job, search_location, statusLabel):

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    driver.get('https://www.linkedin.com/')
    
    statusLabel.setText('Status: Entering Login Info')
    time.sleep(2)
    #Login and Password
    try:
        username = driver.find_element_by_name('session_key')
        username.send_keys(email)
        credential = driver.find_element_by_name('session_password')
        credential.send_keys(password)       
    except:
        try:
            driver.find_element_by_class_name('nav__button-secondary').click()
            time.sleep(4)
            username = driver.find_element_by_name('session_key')
            username.send_keys(email)
            credential = driver.find_element_by_name('session_password')
            credential.send_keys(password)
        except:
            username = driver.find_element_by_xpath('/html/body/nav/section[2]/form/div[1]/div[1]/input')
            username.send_keys(email)
            credential = driver.find_element_by_xpath('/html/body/nav/section[2]/form/div[1]/div[2]/input')
            credential.send_keys(password)
    
    
    username.send_keys(Keys.ENTER)
    statusLabel.setText('Status: User Logged in with Success')

    time.sleep(2)
    if driver.current_url == 'https://www.linkedin.com/check/manage-account':
        driver.find_element_by_css_selector('#ember512 > button.primary-action-new').click()
    
    driver.maximize_window()
    
    #Go to Jobs Tab
    try: 
        driver.find_element_by_xpath('//*[@data-test-global-nav-link="jobs"]').click()
    except:
        print('Cannot Access Jobs Window')
    #driver.find_element_by_css_selector('#jobs-tab-icon').click()
    
    statusLabel.setText('Status: Entering Job and Location info')
    time.sleep(4)    
    #Job title and location
    job_search_field = driver.find_element_by_class_name('jobs-search-box__text-input')
    job_search_field.send_keys(search_job)
    
    try:
        job_location_field = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[1]/section/div[1]/div/div/div[3]/div/div/input')
    except NoSuchElementException:
        job_search_field.send_keys(Keys.TAB)
        job_location_field = driver.switch_to_active_element()
        job_location_field.send_keys(search_location)
   
    job_search_field.send_keys(Keys.ENTER)
    
    
    time.sleep(4)
    page = 1
    first_check = True
    
    jobs = []
    while len(jobs) < num_jobs:
        
        time.sleep(4)
        
        if first_check:
            job_titles_found = driver.find_element_by_class_name('job-card-list__title')
            for i in range(0,4):
                job_titles_found.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            job_titles_found = driver.find_elements_by_class_name('job-card-list__title')
            jobs_per_page = len(job_titles_found)
            first_check = False
     
        for button in job_titles_found:
            try:
                button.click()
            except ElementNotInteractableException:
                print('element nor interactable')
            
            statusLabel.setText("Status: Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
           
            try: 
               company_name = driver.find_element_by_class_name('jobs-details-top-card__company-url').text
            except NoSuchElementException:
                company_name = -1
    
            try: 
                location = driver.find_element_by_class_name('jobs-details-top-card__bullet').text
            except NoSuchElementException:
                location = -1
    
            try: 
                job_description = driver.find_element_by_class_name('jobs-description-content__text').text
            except NoSuchElementException:
                job_description = -1
                
            try: 
               job_title = driver.find_element_by_class_name('jobs-details-top-card__job-title').text 
            except NoSuchElementException:
                job_title = -1
      
            try:
                seniority = driver.find_element_by_class_name('js-formatted-exp-body').text
            except NoSuchElementException:  
                seniority = -1 #You need to set a "not found value. It's important."
      
            try:
                industry = driver.find_element_by_class_name('js-formatted-industries-list').text
            except NoSuchElementException:
                industry = -1 #You need to set a "not found value. It's important."
      
            try:
                job_type = driver.find_element_by_class_name('js-formatted-employment-status-body').text
            except NoSuchElementException:
                job_type= -1 #You need to set a "not found value. It's important."
    
            try:
                job_functions = driver.find_element_by_class_name('js-formatted-job-functions-list').text.replace(' ',', ')
            except NoSuchElementException:
                job_functions= -1 #You need to set a "not found value. It's important."
     
            try:
                size = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/ul/li[1]/span').text
            except NoSuchElementException:
                size = -1            
             
            jobs.append({"Job Title" : job_title,
                         "Job Description" : job_description,
                         "Company Name" : company_name,
                         "Location" : location,
                         "Size" : size,
                         "Job Functions" : job_functions,
                         "Job Type" : job_type,
                         "Industry" : industry,
                         "Seniority" : seniority})
      
            #Clicking on the "next page" button
        if len(jobs) >= page*25:
            try:
                page_complement = ''
                if '&start=' not in driver.current_url:
                    page_complement = '&start=25'
                    driver.get(driver.current_url + page_complement)
                else:              
                    
                    page = page + 1
                    page_complement = '&start=' + str(page * 25)    
                    driver.get(driver.current_url.split('&')[0] + page_complement)
                    
                first_check = True
            except NoSuchElementException:
                
                statusLabel.setText("Status: Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
                break
    
    #This line converts the dictionary object into a pandas DataFrame.
    
    save_path = os.getcwd() + '\\Scraped_Jobs.xlsx'  
    df = pd.DataFrame(jobs)
    df.to_excel(save_path, index=False)
    
    statusLabel.setText('Status: LinkedIn Scraping Ended')

    driver.quit()
    return  save_path 