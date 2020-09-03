import sys, os

from PyPDF2 import PdfFileMerger

from os import listdir
from os.path import isfile, join

current_path = current_path = os.getcwd()

pdfs = [f for f in listdir(current_path + "\\invoices") if isfile(join(current_path + "\\invoices", f))]

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(current_path + '\\invoices\\' + pdf)

merger.write("distribution_barcodes.pdf")
merger.close()
