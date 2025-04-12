from spire.pdf.common import *
from spire.pdf import *

# Create an object of the PdfDocument class
doc = PdfDocument()
# Load a PDF document
doc.LoadFromFile("EGE_2025_Informatika_20var_variant-01_s_otv.pdf")

# Convert the PDF document to a Word DOCX file
doc.SaveToFile("ToDocx.docx", FileFormat.DOCX)
# Close the PdfDocument object
doc.Close()
