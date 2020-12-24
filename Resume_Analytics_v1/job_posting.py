def job_posting(link,resume_skills):
    
    from data_parser import resumeparse,base_path
    from file_reader import read_file
    import os
    import re
    from selenium import webdriver
    from bs4 import BeautifulSoup as bs
    import time
    from urllib.request import urlopen
    import json
    from pandas.io.json import json_normalize
    import pandas as pd, numpy as np
    import requests
    import itertools
    from explicit import waiter, XPATH
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from time import sleep
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.select import Select
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import nltk
    import spacy
    from spacy.matcher import Matcher
    from spacy.matcher import PhraseMatcher
    nlp = spacy.load('en_core_web_sm')

    job_link = link

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument('window-size=2560,1440')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('chrome://settings/')
    driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.5);')

    driver.get(job_link)

    overall_details = driver.find_element_by_class_name("LeftJobHeaderWrapper").text.split("\n")

    md_skills = driver.find_element_by_id('md_skills').text.split("\n\n")

    industry = driver.find_element_by_id('md_industry').text

    print(overall_details)
    print(industry)

    file = ''
    base_path = os.path.dirname(file)
    file = os.path.join(base_path,"SKILLS.txt")
    file = open(file, "r", encoding='utf-8')    
    skill = [line.strip().lower() for line in file]
    skillsmatcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in skill if len(nlp.make_doc(text)) < 10]
    skillsmatcher.add("Job title", None, *patterns)

    matched_skills = []
    matched_requirements = []

    if len(md_skills)>1:
        for prim_skill in skill:
            for match_string in md_skills:
                for lookup_string in match_string.split('\n'):
                    for match in lookup_string.split():
                        if prim_skill.lower()==match.lower():
                            matched_requirements.append(lookup_string)
                            matched_skills.append(prim_skill)
    else:
        for prim_skill in skill:
            for match_string in md_skills[0].split('\n'):
                for match in match_string.split():
                    if prim_skill.lower() == match.lower():
                        matched_requirements.append(match_string)
                        matched_skills.append(prim_skill)

#     matched_skills

    job_dict = {'skill':matched_skills,'requirement':matched_requirements}

    job_data = pd.DataFrame(job_dict)

    job_data.drop_duplicates(inplace=True)

    common_skills= []
    counter=0

    for skill in resume_skills:
        if skill.lower().strip() in list(job_data['skill']):
            common_skills.append(skill)
            counter+=1
            
    return job_data,common_skills,counter