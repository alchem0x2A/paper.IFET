import re
import os, os.path
import shutil
import glob
import subprocess
import multiprocessing
from multiprocessing import Pool
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


# tex_file = "paper.tex"
# tex_tmp = "tmp.tex"

# Delete the leading date and title
def tex_process(tex_file):
    contents = []
    with open(tex_file, "r") as fo:
        contents = fo.readlines()
        # Modify the title and date
        for i, line in enumerate(contents):
            if re.search("\\\\begin{document}", line) is not None:
                break               # find the main document
            if (re.search("title\\{\\}", line) is not None) \
               or (re.search("date\\{\\}", line) is not None) \
               or (re.search("minted", line) is not None):
                contents[i] = "%" + line
        # Modify abstract
        i = 0
        while i < len(contents):
            line = contents[i]
            if (re.search("\\\\section(\*?){Abstract}", line) is not None):
                j = i + 1
                while True:
                    if re.search("\\\\section", contents[j]) is not None:  # Another section
                        print(contents[i], contents[j])
                        contents[i + 1] += "\\begin{boldabstract}\n"
                        contents[j - 1] += "\\end{boldabstract}\n\n"
                        break
                    else:
                        j += 1
                break
            else:
                i += 1

    with open(tex_file, "w") as fw:
        fw.writelines(contents)

# Convert the pdfs

def convert_pdf(infile, outdir="./img"):
    base_name = os.path.basename(infile)
    outfile = os.path.join(outdir, base_name)
    program = "gs"
    params = ["-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
              "-dPDFSETTINGS=/prepress", "-dNOPAUSE",
              "-dQUIET", "-dBATCH"]
    io = ["-sOutputFile={}".format(outfile), infile]
    
    success = subprocess.call([program, *params, *io])
    if success != 0:
        warnings.warn(TColors.FAIL + "File {} cannot be converted!".format(infile) + TColors.ENDC)
    else:
        print(TColors.OKGREEN +
              "File {} converted successfully on thread {}.".format(infile, multiprocessing.current_process())
              +TColors.ENDC)

# Convert all the pdf files
RAW_PATH = "./raw_img"

if __name__ == "__main__":
    import sys
    try:
        img_path = sys.argv[1]
    except IndexError:
        img_path = None
    file_list = []
    # TeX process
    for ifile in glob.glob("*.tex"):
        tex_process(ifile)
        print(TColors.OKBLUE + "Converted TeX file: {}".format(ifile) + TColors.ENDC)

    # PDF Process 
    # for ifile in glob.glob(os.path.join(RAW_PATH, "*.pdf")):
    #     if img_path is None:
    #         file_list.append((ifile))
    #     else:
    #         file_list.append((ifile, img_path))
    # N_cores = multiprocessing.cpu_count()
    # # multicore
    # with Pool(N_cores) as p:
    #     p.map(convert_pdf, file_list)
