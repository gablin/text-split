texts.pdf: base.tex split.py texts.txt
	./split.py -i texts.txt -l base.tex -o tmp.tex --char-split
	pdflatex tmp
	mv tmp.pdf $@
	$(RM) tmp.tex

.PHONY: clean
clean:
	$(RM) *.aux *.log *.pdf
