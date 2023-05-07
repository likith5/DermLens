import streamlit as st
# from pptx import Presentation
# from pptx.util import Inches,Pt
from datetime import date
from PIL import Image
import io
from io import BytesIO
from datetime import datetime
from PIL import Image
import numpy as np
from ultralytics import YOLO
import cv2
from fpdf import FPDF
import os
import shutil
# from reportlab.lib.pagesizes import letter, inch
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
# from reportlab.lib.styles import getSampleStyleSheet

input_folder = "./predicted"
output_folder = "./output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def load_model(model_name):
    model = YOLO(model_name)
    return model

def pred_img(curfile):
    curimg =Image.open(curfile)
    # print(type(model))
    res = model(curimg)
    res_plotted = res[0].plot()
    # output_file = os.path.join(output_folder,curfile)
    # shutil.copy2(res_plotted,output_file)
    # img = Image()
    # basepath = os.path.dirname(__file__)
    # filepath = os.path.join(basepath,"uploads",)
    # res_plotted.save(os.path.join(),)
    # allPred.append(res_plotted)
    with col2:
        st.image(res_plotted, caption = "Predicted Image", width =400)

def generate_pdf():
    pdf = Report()
    buffer = io.BytesIO()
    pdf.output(buffer)
    st.sidebar.write("Download your REPORT here!! :gear:")
    st.sidebar.download_button(label='Click to download PDF',
                        data=buffer.getvalue(),
                        file_name="Report "+str(datetime.now())+" "+".pdf")


class Report(FPDF):
    def __init__(self):
        super().__init__()

        # Set up the page size and margins
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'My Report', 0, 1, 'C')
        self.ln(20)

        # Add patient details
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Patient Details', 0, 1)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, "Patient Name:" + pname, 0, 1)
        self.cell(0, 10, "Age:"+ str(page), 0, 1)
        self.cell(0, 10, "Gender:"+ pgen, 0, 1)
        self.cell(0, 10, "Region where Vitiligo is present:"+ region, 0, 1)
        self.cell(0, 10, "Is there a presence of scales in depigmented area:"+ scales, 0, 1)
        self.cell(0, 10, "Have you done a Uveitis Test:"+ utest, 0, 1)
        print(allPred)
        # Add patient image
        for i in allPred:
            self.image(i, x=10, y=100, w=100, h=100)

# def generate_pdf():
#     patient_data = [
#     ["Patient Name:", pname],
#     ["Age:", page],
#     ["Gender:", pgen],
#     ["Region where Vitiligo is present:", region],
#     ["Is there a presence of scales in depigmented area:", scales],
#     ["Have you done a Uveitis Test:", utest]
#     ]

#     patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
#     patient_table.setStyle(TableStyle([
#         ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
#         ("FONTSIZE", (0, 0), (-1, -1), 12),
#         ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
#         ("ALIGN", (0, 0), (0, -1), "RIGHT"),
#     ]))

#     spacer = Spacer(1, 0.25*inch)

#     pdf_file = "my_report.pdf"
#     doc = SimpleDocTemplate(pdf_file, pagesize=letter)

#     styles = getSampleStyleSheet()
#     style_normal = styles["Normal"]

#     story = []
#     story.append(Paragraph("Patient Details:", style_normal))
#     story.append(patient_table)
#     story.append(spacer)
#     story.append(patient_image)

#     doc.build(story)

#     st.sidebar.write("Download your REPORT here!! :gear:")
#     st.sidebar.download_button(label='Click to download PDF',
#                         data=doc,
#                         file_name="Report "+str(datetime.now())+" "+".pdf")


     

# def enable_download(ppt_file):

#     filename = prompt +" "+str(datetime.now())+" "+".pptx"
#     st.sidebar.write("Download your REPORT here!! :gear:")
#     st.sidebar.download_button(label='Click to download PDF',
#                         data=ppt_file.getvalue(),
#                         file_name=filename)



# def generate_pdf(ppt_prompt):
#     st.caption("Your PPT is being generated!")
#     ppt_out = ppt_generation()
#     enable_download(ppt_out)


st.set_page_config(layout="wide")

# st.title("DermLens")
# st.header("prompt")


st.image("logo.jpeg",width =200)
# st.title("DermLens")

st.write("## Wood Lamp Images")
st.sidebar.write("## Patient Details")

# st.write(
#     " Write a prompt into the textbox below and watch the magic happen"
# )

files = st.file_uploader('Upload Image', type = ['jpg','png','jpeg'],accept_multiple_files=True)

model = load_model("dermv8n.pt")
allPred = []

col1, col2 = st.columns(2)

if files != []:
    
    if st.button("Predict"):
        for file in files:
            img1 = Image.open(file)
            img2 = np.array(img1)
            with col1:  
                st.image(img1, caption = "Uploaded Image", width =400)

            pred_img(file)


pname = st.sidebar.text_input("Name")
page = st.sidebar.number_input('Age', min_value=0, max_value=100, value=18)
pgen = st.sidebar.radio("Gender",("Male","Female","Others"))
region = st.sidebar.text_input("Region where Vitiligo is present")
scales = st.sidebar.radio("Presence of scales in depigmented area",("No","Yes"))
utest = "NA"
if scales == "Yes":
     utest = st.sidebar.radio("Have you done a Uveitis Test",("No","Yes"))
# print(utest)
if st.sidebar.button("Generate PDF"):
        generate_pdf()
