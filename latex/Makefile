.PHONY: Main.pdf
Main.pdf:
	pdflatex Main
	bibtex Main
	pdflatex Main
	pdflatex Main

.PHONY: clean 
clean: 
	@rm -f *.aux *.dvi *.log *.out *.toc *.bbl *.blg *.lof Main.pdf
