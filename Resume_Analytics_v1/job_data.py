def job_data(job_link,resume_skill):
    
    '''This function will extract job related data along with the matched skills from resume. As per requirement, we will also be capturing the skills not present in the resume but mentioned in the Job posting.
    The count of skills willbe ectracted too'''

    import os
    import re
    import time
    from urllib.request import urlopen
    import json
    from pandas.io.json import json_normalize
    import pandas as pd, numpy as np
    import requests
    import nltk
    import spacy
    from spacy.matcher import Matcher
    from spacy.matcher import PhraseMatcher
    nlp = spacy.load('en_core_web_sm')
    import itertools
    import collections
    from bs4 import BeautifulSoup
    from rake_nltk import Rake
    
    # Extracting job posting
    page = requests.get(job_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    jobtitle = soup.find(id='td_jobpositionnolink')
    jobtype = soup.find(id='td_job_type')
    jobpostedby = soup.find(id='td_posted_by')
    posteddate = soup.find(id='td_posted_date')
    
    #Job Data
    Job_Title = jobtitle.text
    Job_Type = jobtype.text
    Posted_By = jobpostedby.text.split(': ')[1]
    Posted_Date = posteddate.text.split(': ')[1]
#     print(Job_Title)
#     print(Job_Type)
#     print(Posted_By)
#     print(Posted_Date)

    # This will give us all the job details
    Job_Details = soup.find('div', {'class':'md_skills'})
    Job_Attributes = Job_Details.findAll('li')
    Job_Data = []
    for elem in Job_Attributes:
        elem1 = elem.text
        Job_Data.append(elem1)

    job_text= ' '.join(elem for elem in Job_Data)

    r = Rake()
    r.extract_keywords_from_text(job_text)

    skill_list = r.get_ranked_phrases()
    
    lookup = []
    for elem in Job_Data:
        temp_list= elem.split(',')
        for i in temp_list:
            lookup.append(i)
            
    lookup_master = []
    for elem in lookup:
        temp_list= elem.split(' ')
        for i in temp_list:
            lookup_master.append(i)
            
    # Importing our skill file
    file = ''
    base_path = os.path.dirname(file)
    file = os.path.join(base_path,"data_files/SKILLS_1.txt")
    file = open(file, "r", encoding='utf-8')    
    skill_file = [line.strip().lower() for line in file]   
    
    # Stage 1 Match
    match=[]
    for skill in skill_file:
        for job_skill in skill_list:
            if len(job_skill.split(' '))==1:
                if skill.upper() in job_skill.strip().upper():
                    match.append(skill)
            else:
                for s in job_skill.split(' '):
    #                 print(s)
                    if skill.upper() == s.strip().upper():
                        match.append(skill)
                
    final = []
    for item in match:
        for master_item in lookup_master:
            if item.lower()==master_item.lower().strip():
                final.append(item.upper())
                
    final_skills = list(set(final))   
    for skill in final_skills:
        if skill=='':
            final_skills.remove(skill)
    num_skills = len(final_skills)
    # Create counter
    word_count = collections.Counter(lookup_master)
    WordCount = {k.upper():v for k,v in word_count.items()}
    
    word_dict={}
    for item in final_skills:
        key = item

        value = WordCount[key]
        temp_dict = {key:value}
        word_dict.update(temp_dict)
        
    # Fetching skills not present in resume but mentioned in job posting
    matched_skill_count=0
    unmatched_skill_count=0
    matched_skills = []
    for skill in final_skills:
        for res_skill in resume_skill:
            if skill.upper()== res_skill.strip().upper():
                matched_skill_count+=1
                matched_skills.append(skill)
    tech_score = matched_skill_count/num_skills
    tech_det_dict = {}
    for i in range(0,len(matched_skills)):
        temp_dict = {i:{'title':matched_skills[i],'score':100}}
        tech_det_dict.update(temp_dict)
        
    technical_skill = {'score':tech_score,'details':tech_det_dict}
    
    key_score = round(matched_skill_count/num_skills)
    key_det_dict = {}
    for i in range(0,len(matched_skills)):
        temp_dict = {i:{'title':matched_skills[i],'score':100}}
        key_det_dict.update(temp_dict)
        
    keywords = {'score':key_score,'details':key_det_dict}
        

    unmatched_skill_count  =  num_skills-matched_skill_count
    output = {
        "jobRole" : Job_Title,
        "job_type":Job_Type,
        "companyName": Posted_By,
        "posted_date": Posted_Date,
        "job_skills": final_skills,
        "job_skill_count": word_dict,
        "num_of_job_skills": num_skills,
        "matched_skills":matched_skills,
        "matched_skill_count": matched_skill_count,
        "unmatched_skill_count":unmatched_skill_count,
        "technicalSkills": technical_skill,
        "keywords": keywords
        }
    
    return output