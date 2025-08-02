import os 
import fitz
from openai import OpenAI

client=OpenAI()

def read_txt(path):
    with open(path,"r",encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    text=""
    with fitz.open(path) as doc:
        for page in doc:
            text+=page.get_text()
    return text

def split_text(text,max_words=500):
    words=text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0,len(words),max_words)]            

file_path="data/"+input("Enter file name:")

if file_path.endswith(".txt"):
    text=read_txt(file_path)
elif file_path.endswith(".pdf"):
    text=read_pdf(file_path)
else:
    raise ValueError("Unsupported file format. Use .txt or .pdf") 

chunks=split_text(text,max_words)

summaries=[]
for i,chunk in enumerate(chunks):
    response=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":"You are helpful assistant that summaries text."},
        "role":"user","content":f"Summarise:\n\n{chunk}]

    )
summaries.append(response.choices[0].message.content)

final_summary="\n\n".join(summaries)

os.makedirs("summaries",exist_ok=True)
with open("summaries/summary_output.txt","w",encoding="utf-8") as f:
    f.write(final_summary)