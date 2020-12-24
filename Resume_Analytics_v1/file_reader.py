import re
import os
import docx2txt
from tika import parser
import pdfplumber

import logging


def convert_docx_to_txt(docx_file):
    """
        A utility function to convert a Microsoft docx files to raw text.

    """
    try:
        text = parser.from_file(docx_file, service='text')['content']
        
        # number of pages
        raw_xml = parser.from_file(docx_file, xmlContent=True)
        body = raw_xml['content'].split('<body>')[1].split('</body>')[0]
        body_without_tag = body.replace("<p>", "").replace("</p>", "").replace("<div>", "").replace("</div>","").replace("<p />","")
        text_pages = body_without_tag.split("""<div class="page">""")[1:]
        num_pages = len(text_pages)
        
    except RuntimeError as e:            
        logging.error('Error in tika installation:: ' + str(e))
        logging.error('--------------------------')
        logging.error('Install java for better result ')
        text = docx2txt.process(docx_file)
        num_pages = None
    except Exception as e:
        logging.error('Error in docx file:: ' + str(e))
        return [], " "
    try:
        clean_text = re.sub(r'\n+', '\n', text)
        clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
        resume_lines = clean_text.splitlines()  # Split text blob into individual lines
        resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if
                        line.strip()]  # Remove empty strings and whitespaces
        return resume_lines, text,num_pages
    except Exception as e:
        logging.error('Error in docx file:: ' + str(e))
        return [], " "

def convert_pdf_to_txt(pdf_file):
    """
    A utility function to convert a machine-readable PDF to raw text.

    """

    try:
        raw_text = parser.from_file(pdf_file, service='text')['content']
        pages_read = pdfplumber.open(pdf_file)
        num_pages = len(pages_read.pages)
        pages_read.close()
    except RuntimeError as e:            
        logging.error('Error in tika installation:: ' + str(e))
        logging.error('--------------------------')
        logging.error('Install java for better result ')
        pdf = pdfplumber.open(pdf_file)
        num_pages = len(pdf.pages)
        raw_text= ""
        for page in pdf.pages:
            raw_text += page.extract_text() + "\n"
        pdf.close()                
    except Exception as e:
        logging.error('Error in pdf file:: ' + str(e))
        return [], " "
    try:
        full_string = re.sub(r'\n+', '\n', raw_text)
        full_string = full_string.replace("\r", "\n")
        full_string = full_string.replace("\t", " ")

        # Remove awkward LaTeX bullet characters

        full_string = re.sub(r"\uf0b7", " ", full_string)
        full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
        full_string = re.sub(r'• ', " ", full_string)
        full_string = re.sub(r'● ', " ", full_string)
        # Split text blob into individual lines
        resume_lines = full_string.splitlines(True)

        # Remove empty strings and whitespaces
        resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]
        return resume_lines, raw_text,num_pages
    except Exception as e:
        logging.error('Error in docx file:: ' + str(e))
        return [], " "
    
def read_file(file):
      
        file = os.path.join(file)
        if file.endswith('docx') or file.endswith('doc'):
            resume_lines, raw_text,num_pages = convert_docx_to_txt(file)
        elif file.endswith('pdf'):
            resume_lines, raw_text,num_pages = convert_pdf_to_txt(file)
        elif file.endswith('txt'):
            with open(file, 'r', encoding='latin') as f:
                resume_lines = f.readlines()
            num_pages = None

        else:
            resume_lines = None
            num_pages = None
        # Cleaning text
        
        return resume_lines,num_pages