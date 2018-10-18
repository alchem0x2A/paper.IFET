DOCX_REF= ./utils/my_reference.docx
BUILD_PATH = ./build
IMG_PATH = ./img
BIB_FILE = ./ref.bib
CSL_FILE = ./utils/aps.csl
DOCX_NAME = ./build/paper.docx
TEX_FILE = ./paper.tex
NAT_TEX_FILE = ./paper_nature_format.tex
ZIP_FILE = ./paper_tex_submission.zip
SUPPL_TEX_FILE = ./suppl.tex
PDF_M = paper.pdf
PDF_CHANG = paper_change.pdf
PDF_SI = suppl.pdf
VERBOSE = --verbose
LATEXMKFLAGS = -f -pdf -quiet
LATEXMKFLAGS += -pdflatex="pdflatex -interactive=nonstopmode"
DIFF_FLAGS= --exclude-textcmd="section,subsection,bibitem" --config="PICTUREENV=(?:figure|section|DIFnomarkup|mcitethebibliography)[*]*" --graphics-markup=0 --disable-citation-markup

all: build post-process latex-to-pdf SI-latex-to-pdf diff archive

build: | $(BUILD_PATH) $(IMG_PATH)

$(BUILD_PATH):
	mkdir -p $@

$(IMG_PATH):
	mkdir -p $@

post-process: post_process.py
	python post_process.py

convert-pdf: convert.py
	python convert.py	#manually run

pandoc-to-word:
	pandoc --from=latex --to=docx $(TEX_FILE) -o $(DOCX_NAME) \
		--reference-doc=$(DOCX_REF) \
		--bibliography=$(BIB_FILE) \
		--csl=$(CSL_FILE) \
		$(VERBOSE)

latex-to-pdf: $(TEX_FILE) $(BIB_FILE)
	latexmk $(LATEXMKFLAGS) $<
	latexmk -c

SI-latex-to-pdf: $(SUPPL_TEX_FILE) $(BIB_FILE)
	latexmk $(LATEXMKFLAGS) $<
	latexmk -c

diff:
	latexdiff $(DIFF_FLAGS) paper_old.tex paper.tex > paper_change.tex
	latexmk $(LATEXMKFLAGS) paper_change.tex 

archive: 
	rm -rf $(BUILD_PATH)/*
	mkdir -p $(BUILD_PATH)/img
	cp $(IMG_PATH)/scheme*.pdf $(BUILD_PATH)/img/
	cp $(PDF_M) $(PDF_SI) $(TEX_FILE) paper_change.pdf $(BUILD_PATH)
	cp $(IMG_PATH)/TOC.pdf paper.bbl.bak $(BUILD_PATH)
	cp -r ./videos $(BUILD_PATH)

clean:
	latexmk -C
	rm -rf 
	rm *~ *# *.bbl $(BUILD_PATH)/*

