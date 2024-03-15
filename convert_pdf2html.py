##
## sudo apt install -y wkhtmltopdf
## Install PyMuPDF: pip install pymupdf
##
import fitz
print(fitz.__doc__)
doc = fitz.open("result/ocr_result.pdf") 

# for page in doc: # iterate the document pages
#     text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
#     print(text)

for page in doc: # iterate the document pages
    for line in page.get_text("html").splitlines():
        print(line)
            
# 	text = page.get_text("html").encode("utf8") # get plain text (is in UTF-8)
# 	out.write(text) # write text of page
# 	out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
# out.close()


        

# def to_html(filepath: str):
#     doc = fitz.open(filepath)
#     for i, page in enumerate(doc):
#         text = page.getText("html")
#         with open(f"result/pymupdf-page-{i}.html", "w") as fp:
#             fp.write(text)
#     doc.close()


# to_html("result/ocr_result.pdf")


# import pdfkit

# # Set the path to wkhtmltopdf executable file
# path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'  # This may vary depending on your system
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# # Use the configuration when generating PDF
# #pdfkit.from_url('http://google.com', 'out.pdf', configuration=config)

# # Read the PDF file
# pdf_file = open('result/ocr_result.pdf', 'rb')
# # Convert the PDF to HTML
# html_file = pdfkit.from_file(pdf_file, "result/ocr_result.html")
# # Close the PDF file
# pdf_file.close()
