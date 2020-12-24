# from file_reader import read_file
from data_parser import resumeparse,base_path
from file_reader import read_file
from job_posting import job_posting
import os
import json
import re
import sys

def main(file,job_link):
      
        resume_lines,num_pages = read_file(file)
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
        
        final_degree = list(set(degree + degree2)) 
        
        
        job_data,common_skills,counter = job_posting(job_link,skills)
        c_skills = list(common_skills)
        if len(c_skills)==0:
            c_skills.append('None')
        requirement_phrase = list(job_data['requirement'])
        requirement_skills= list(job_data['skill'])
        if len(requirement_phrase)==0:
            requirement_skills.append('None')
            requirement_phrase.append('None')
                                 
                                     
        
        output = {
            "num_pages" : num_pages,
            "email": email,
            "phone": phone,
            "name": name,
            "total_exp": total_exp,
            "university": university,
            "designition": designition,
            "degree": final_degree,
            "skills": skills,
            "matched_skills": c_skills,
            "job_requirement_phrase": requirement_phrase,
            "Job_skills_requirement":requirement_skills
        }
        with open('output.json','w') as outfile:
            json.dump(output,outfile)
        return output
    
if __name__ == '__main__':
    path = ''.join(sys.argv[1:])
    print('here ',path)
    main(path)
    