DOCX_REF= ./utils/my_reference.docx
BUILD_PATH = ./build
IMG_PATH = ./img
BIB_FILE = ./ref.bib
CSL_FILE = ./utils/aps.csl
DOCX_NAME = ./build/paper.docx
TEX_FILE = ./paper.tex
SUPPL_TEX_FILE = ./suppl.tex
PDF_M = paper.pdf
PDF_CHANG = paper_change.pdf
PDF_SI = suppl.pdf
VERBOSE = --verbose
LATEXMKFLAGS = -f -pdf -quiet
LATEXMKFLAGS += -pdflatex="pdflatex -interaction=nonstopmode"

all: build post-process pandoc-to-word latex-to-pdf SI-latex-to-pdf

build: | $(BUILD_PATH) $(IMG_PATH)

$(BUILD_PATH):
	mkdir -p $@

$(IMG_PATH):
	mkdir -p $@

post-process: post_process.py
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

SI-latex-to-pdf: $(SUPPL_TEX_FILE) $(BIB_FILE)
	latexmk $(LATEXMKFLAGS) $<
	mv $(PDF_SI) $(BUILD_PATH)
	latexmk -c

clean:
	latexmk -C
	rm -rf 
	rm *~ *# *.bbl $(BUILD_PATH)/*

