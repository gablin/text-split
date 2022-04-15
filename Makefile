texts.pdf: base.tex split.py texts.txt
	./split.py -i texts.txt -l base.tex -o tmp.tex
	pdflatex tmp
	mv tmp.pdf $@
	$(RM) tmp.tex

.PHONY: clean
clean:
	$(RM) *.aux *.log *.pdf
