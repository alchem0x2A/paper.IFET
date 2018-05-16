import re
import os, os.path
import shutil
import glob
import subprocess
import warnings


# color definition
class TColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


tex_file = "paper.tex"
# tex_tmp = "tmp.tex"

# Delete the leading date and title
contents = []
with open(tex_file, "r") as fo:
    contents = fo.readlines()
    for i, line in enumerate(contents):
        if re.search("\\\\begin{document}", line) is not None:
            break               # find the main document
        if (re.search("title\\{\\}", line) is not None) \
           or (re.search("date\\{\\}", line) is not None) \
           or (re.search("minted", line) is not None):
            contents[i] = "%" + line

with open(tex_file, "w") as fw:
    fw.writelines(contents)

# Convert the pdfs

def convert_pdf(infile, outdir="./img"):
    base_name = os.path.basename(infile)
    outfile = os.path.join(outdir, base_name)
    program = "gs"
    params = ["-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
              "-dPDFSETTINGS=/ebook", "-dNOPAUSE",
              "-dQUIET", "-dBATCH"]
    io = ["-sOutputFile={}".format(outfile), infile]
    
    success = subprocess.call([program, *params, *io])
    if success != 0:
        warnings.warn(TColors.FAIL + "File {} cannot be converted!".format(infile) + TColors.ENDC)
    else:
        print(TColors.OKGREEN +
              "File {} converted successfully.".format(infile)
              +TColors.ENDC)

# Convert all the pdf files
RAW_PATH = "./raw_img"
for ifile in glob.glob(os.path.join(RAW_PATH, "*.pdf")):
    convert_pdf(ifile)
