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

# Replace the ref with bbl
def merge_bbl(tex_file):
    if tex_file is None:
        return False
    file_base, ext = os.path.splitext(tex_file)
    if ext not in (".tex", ".latex", ".xelatex", "xetex"):
        raise NameError("File is not a tex file!")
    
    bbl_file = file_base + ".bbl.bak"
    bbl_content = None
    with open(bbl_file, "r", encoding="utf-8") as fo:
        bbl_content = fo.read()
        
    contents = []
    with open(tex_file, "r", encoding="utf-8") as fo:
        contents = fo.readlines()
        # Modify the title and date
        for i, line in enumerate(contents):
            if re.search("\\\\bibliographystyle", line) is not None:
                contents[i] = "%" + line
            if (re.search("\\\\bibliography", line) is not None):
                contents[i] = "%" + line + bbl_content
                break
    out_file = file_base + ".tex"
    with open(out_file, "w", encoding="utf-8") as fw:
        fw.writelines(contents)


if __name__ == "__main__":
    import sys
    try:
        ifile = sys.argv[1]
    except IndexError:
        ifile = None
    file_list = []
    # TeX process
    if tex_process(ifile):
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
