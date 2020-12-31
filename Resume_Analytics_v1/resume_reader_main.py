# from file_reader import read_file
from data_parser import resumeparse,base_path
from file_reader import read_file
import os
import json
import re
import sys
import job_posting
from job_data import job_data

def main(file,job_link):
      
        resume_lines,num_pages = read_file(file)
        num_of_words = len(resume_lines)
        resume_segments = resumeparse.segment(resume_lines)
        
        
        full_text = " ".join(resume_lines)
        
        email = resumeparse.extract_email(full_text)
        phone = resumeparse.find_phone(full_text)
        name = resumeparse.extract_name(" ".join(resume_segments['contact_info']))
        total_exp, text = resumeparse.get_experience(resume_segments)
        university = resumeparse.extract_university(full_text, os.path.join(base_path,'data_files','world-universities.csv'))

        designition = resumeparse.job_designition(full_text)
        designition = list(dict.fromkeys(designition).keys())

        degree = resumeparse.get_degree(full_text)
        degree2 = resumeparse.extract_degree(full_text)
        
        skills = ""
        
        if len(resume_segments['skills'].keys()):
            for key , values in resume_segments['skills'].items():
                mod_values = [val for val in values if len(val.split()) <10]
                add_skill = re.sub(key, '', ",".join(mod_values), flags=re.IGNORECASE)
                
                skills +=  add_skill  
                
            skills = skills.strip().strip(",").split(",")
        
        if len(skills) == 0:
            skills = resumeparse.extract_skills(full_text)
        skills = list(dict.fromkeys(skills).keys())
        skills1=[]
        for skill in skills:
#             skill2 = ''.join(e for e in skill if e.isalnum())
            skill2 = re.sub('[^A-Za-z0-9/ /]+', '', skill)
            skill1 = skill2.upper().strip()
            skills1.append(skill1)
        num_skills = len(skills1)
        
        final_degree = list(set(degree + degree2)) 
        
        extracted_job_data = job_data(job_link,skills1)

        output = {
            "num_pages" : num_pages,
            "num_of_words":num_of_words,
            "email": email,
            "phone": phone,
            "name": name,
            "total_exp": total_exp,
            "university": university,
            "designition": designition,
            "degree": final_degree,
            "skills": skills1,
            "number_of_skills":num_skills,
            "Job_Data": extracted_job_data            
        }
#         with open('output.json','w') as outfile:
#             json.dump(output,outfile)
        return output
    
    