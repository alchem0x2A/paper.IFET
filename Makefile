DOCX_REF= ./utils/my_reference.docx
BUILD_PATH = ./build
IMG_PATH = ./img
BIB_FILE = ./ref.bib
CSL_FILE = ./utils/aps.csl
DOCX_NAME = ./build/paper.docx
TEX_FILE = ./paper.tex
PDF_M = paper.pdf
VERBOSE = --verbose
LATEXMKFLAGS = -f -pdf -quiet
LATEXMKFLAGS += -pdflatex="pdflatex -interaction=nonstopmode"

all: post-process pandoc-to-word latex-to-pdf

post-process: post_process.py
	test ! -d $(BUILD_PATH) && mkdir $(BUILD_PATH)
	test ! -d $(IMG_PATH) && mkdir $(IMG_PATH)
	python post_process.py

pandoc-to-word:
	pandoc --from=latex --to=docx $(TEX_FILE) -o $(DOCX_NAME) \
		--reference-doc=$(DOCX_REF) \
		--bibliography=$(BIB_FILE) \
		--csl=$(CSL_FILE) \
		$(VERBOSE)

latex-to-pdf: $(TEX_FILE) $(BIB_FILE)
	latexmk $(LATEXMKFLAGS) $<
	mv $(PDF_M) $(BUILD_PATH)
	latexmk -c

clean:
	latexmk -C
	rm -rf 
	rm *~ *# *.bbl $(BUILD_PATH)/*

