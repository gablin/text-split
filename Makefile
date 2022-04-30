%.pdf: base.tex split.py %.txt
	./split.py -i $(@:.pdf=.txt) -l base.tex -o tmp.tex --char-split
	pdflatex tmp
	mv tmp.pdf $@
	$(RM) tmp.tex

.PHONY: clean
clean:
	$(RM) *.aux *.log *.pdf
