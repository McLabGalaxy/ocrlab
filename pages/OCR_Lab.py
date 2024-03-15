import os
import cv2
import time
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
import streamlit as st
from PIL import Image
import urllib.request, urllib.parse, urllib.error

import fpdf 

import asyncio
from pathlib import Path
from svgtrace import trace,asyncTrace    
import os


FONT = 'fonts/simfang.ttf'

st.set_page_config(
    page_title="eReceipt OCR-Image",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")

st.title("OCR Lab")
language = st.sidebar.selectbox("Select Language", ["English", "Japanese", "German", "Chinese","Korean"])
language_code="en"

if language == "Japan":
    language_code = "japan"
elif language == "French":
    language_code = "fr"
elif language == "Chinese":
    language_code = "ch"
elif language == "German":
    language_code = "german"    
elif language == "English":
    language_code = "en"
elif language =="Spanish":
    language_code = "es"

with st.sidebar.expander("printer receipt components"):
    st.sidebar.subheader("printer receipt components")    
    st.sidebar.markdown("""
        - <Printer>
        - <Text>
        - <Row>
        - <Br>
        - <Line>
        - <Barcode>
        - <QRCode>
        - <Image>(Vector image file formats)
        - <Cut>
        - <Raw>                    
    """)
st.sidebar.markdown("JPEG/PNG are raster formats, SVG is a vector format.")
st.sidebar.subheader("Random sample receipts")
st.sidebar.markdown("""
    - http://n.sinaimg.cn/ent/transform/w630h933/20171222/o111-fypvuqf1838418.jpg
    - https://mrcconsultancy.files.wordpress.com/2018/02/e-receipt-japan0003.jpg
    - https://ielanguages.com/real/German/images/receipt_jpg.jpg
    - https://user-images.githubusercontent.com/13250888/190206825-e54d2d4f-c4e7-45e0-ba8f-eff5cd2b06ff.png
    - https://rpower-marketing-assets.s3.amazonaws.com/Public/rpower-webpage-marketverticles-photos/rpower-pos-asian-restaurant-receipt.png
        """)


_ENABLE_USER_GPU = False
# require 
# !python -m pip install paddlepaddle-gpu==2.0.0 -i https://mirror.baidu.com/pypi/simple
#
# classification and detection
# det=False, cls=False

_SHOW_OCR_RESULT = False

uploadfile_path = None

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang=language_code,use_gpu=_ENABLE_USER_GPU)

def save_uploadedfile(uploadedfile):
    save_folder = 'result'
    save_path = Path(save_folder, uploadedfile.name)
    with open(save_path, mode='wb') as w:
        w.write(uploadedfile.getbuffer())
    if save_path.exists():
        st.success(f'File {uploadedfile.name} is successfully saved!')
    return save_path   
    
def preprocess_ocr_image(upload_file:str=None, image_url:str=None):
    if upload_file is None and image_url is None:
        raise ValueError("preprocess image missing input file or url")    
    # Load the image
    if upload_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    elif image_url:
        file_bytes = np.asarray(bytearray(urllib.request.urlopen(input_img_url).read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB color space        
    return image

def ocr_image(image=None,image_url:str=None):
    if image is None and image_url is None:
        raise ValueError("ocr image missing input file or url")
    if image is not None:
        results = ocr.ocr(image, cls=True)  
    elif image_url:
        results = ocr.ocr(image_url, cls=True)                
    return results

def convert_svg_to_pdf(svf_file:str="result/ocr_result.svg", output_file:str="result/ocr_result.pdf"):
    svg = fpdf.svg.SVGObject.from_file(svf_file)
    pdf = fpdf.FPDF(unit="pt", format=(svg.width, svg.height))
    pdf.add_page()
    svg.draw_to_page(pdf)
    pdf.output(output_file)
    return output_file

### Main UI###
# st.image('ocr_logo.png', caption='OCR Receipt Image to Text and SVG')

#st.divider()    
st.subheader("A. Enter Receipt Link")
# input image url
input_img_url = ''

input_img_url = st.text_input("Input receipt Image Url 👇",key="placeholder",)
#st.write('you entered url:', title)
if input_img_url:
    #st.write("You entered: ", input_img_url)
    retrived_image=st.image(input_img_url, caption="Web Receipt Image", use_column_width=True)                
    input_image=preprocess_ocr_image(image_url=input_img_url)
    # Perform OCR on the image
    with st.spinner("Working on OCR...one moment, please!"):
        results = ocr_image(input_img_url)
        _SHOW_OCR_RESULT=True
    
st.subheader("B. Upload Receipt Image")
# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

st.divider()

if uploaded_file is not None:
    # Load the image
    input_image=preprocess_ocr_image(upload_file=uploaded_file)
    
    uploadfile_path=save_uploadedfile(uploaded_file)
    print("saved upload file:",uploadfile_path)
    #save_uploadedfile(uploaded_file)
    print(uploadfile_path)    
    file_stats = os.stat(uploadfile_path)
    #st.write(f'Image file size:{file_stats.st_size / (1024):.2f} KB')    
    st.metric(label="Image File", value=f"{file_stats.st_size / (1024):.2f} KB")           
        
    # Display the uploaded image
    st.image(input_image, caption="Uploaded Receipt Image", use_column_width=True)
    # Perform OCR on the image
    t0 = time.perf_counter()    
    with st.spinner("Working on OCR...one moment, please!"):
        results = ocr_image(input_image)
        _SHOW_OCR_RESULT=True

st.divider()
if _SHOW_OCR_RESULT:
    # Display the OCR result image    
    t0 = time.perf_counter()        
    st.write('OCR Result (Detection, Classification and Recognition)')
    result = results[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result] 

    im_show = draw_ocr(input_image, boxes, txts, scores, font_path=FONT)
    st.image(im_show)       

    ## save annotated-image to file
    im_filename = "result/ocr_result.png"
    im_show = Image.fromarray(im_show)
    im_show.save(im_filename)
    ## show image download button
    with open(im_filename, "rb") as file:
        st.download_button(label="Download annotated image",data=file,file_name=im_filename,mime='image/png')    

    # show OCR result text
    st.image("static/text_file.png", width=110)           
    result_text=[]
    for idx in range(len(results)):
        res = results[idx]
        for line in res:
            result_text.append(str(line))
    ocr_txt = st.text_area("OCR Result Text",result_text)
    st.write(f'total {len(ocr_txt)} characters.')
    #print(ocr_txt)

    ## save OCR result to file 
    im_text_file = "result/ocr_result.txt"
    with open(im_text_file, "w", encoding="utf-8") as file:
        file.write(ocr_txt)
    ## show text file download button
    with open(im_text_file, "rb") as file:
        st.download_button(label="Download result text",data=file,file_name=im_text_file,mime='text/txt')     

    #print(im_text_file)    
    file_stats = os.stat(im_text_file)
    #st.write(f'OCR Text file size:{file_stats.st_size / (1024):.4f} KB')    
    st.metric(label="OCR Text File", value=f"{file_stats.st_size / (1024):.2f} KB")           

    t1 = time.perf_counter() - t0
    st.success(f"image ocr success. it took {t1:.2f} seconds")    

    ## convert image to SVG
    if uploadfile_path:
        st.image("static/svg_file.png", width=110)               
        t0 = time.perf_counter()        
        uploadfile_path=os.path.abspath(uploadfile_path)            
        st.write(f"uploaded: {uploadfile_path}")               
        output_file="result/ocr_result.svg"
        t0 = time.perf_counter()
        svg_output1=asyncio.run(asyncTrace(uploadfile_path, True))
        Path(output_file).write_text(svg_output1, encoding="utf-8")
        t1 = time.perf_counter() - t0
        #print("test-2 took ", t1)                
        svg_txt = st.text_area("Result SVG",svg_output1)
        st.write(f'total {len(svg_txt)} characters.')
        #print(svg_txt)
        with open(output_file, "rb") as file:
            st.download_button(label="Download result SVG",data=file,file_name="ocr_result.svg",mime='image/svg+xml')         
        file_stats = os.stat(output_file)
        #st.write(f'SVG file size:{file_stats.st_size / (1024):.4f} KB')    
        st.metric(label="SVG File", value=f"{file_stats.st_size / (1024):.2f} KB")                   
        st.success(f"converted to svg. it took {t1:.2f} seconds")            
        
        ## convert SVG to PDF
        st.image("static/pdf_file.png", width=110)               
        t0 = time.perf_counter()                
        pdf_file=convert_svg_to_pdf(svf_file=output_file, output_file="result/ocr_result.pdf")
        #st.success(f"converted svg to PDF. it took {t1:.2f} seconds")    
        t1 = time.perf_counter() - t0
        with open(pdf_file, "rb") as file:
            st.download_button(label="Download result PDF",data=file,file_name="receipt_svg_converted.PDF",mime='application/pdf') 
        file_stats = os.stat(pdf_file)
        #st.write(f'PDF file size:{file_stats.st_size / (1024):.4f} KB')    
        st.metric(label="PDF File", value=f"{file_stats.st_size / (1024):.2f} KB")                  
        st.success(f"converted to svg. it took {t1:.2f} seconds")            
