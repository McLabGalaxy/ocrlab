
#from fpdf import FPDF
import fpdf 

def convert_svg_to_pdf(svf_file:str="result/ocr_result.svg", output_file:str="result/ocr_result.pdf"):
    svg = fpdf.svg.SVGObject.from_file(svf_file)
    pdf = fpdf.FPDF(unit="pt", format=(svg.width, svg.height))
    pdf.add_page()
    svg.draw_to_page(pdf)
    pdf.output(output_file)
    return output_file


print(convert_svg_to_pdf())
print("done")
