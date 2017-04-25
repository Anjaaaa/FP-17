NAME=Protokoll

all:  Aufbau_Ablauf.tex Auswertung.tex Diskussion.tex Theorie.tex $(NAME).tex
	pdflatex $(NAME).tex
	biber $(NAME)
	pdflatex $(NAME).tex
	pdflatex $(NAME).tex
	rm -rf *.aux
	rm -rf *.log
	rm -rf *.idx
	rm -rf *.synctex.gz
	rm -rf *.toc
	rm -rf *.tdo
	rm -rf *.bbl
	rm -rf *.bcf
	rm -rf *.blg
	rm -rf *.run.xml
	rm -rf *.lof
	rm -rf *.lot


clean:
	rm -rf *.aux
	rm -rf *.log
	rm -rf *.idx
	rm -rf *.synctex.gz
	rm -rf *.toc
	rm -rf *.tdo
	rm -rf *.bbl
	rm -rf *.bcf
	rm -rf *.blg
	rm -rf *.run.xml
	rm -rf *.lof
	rm -rf *.lot


clean-all:
	rm -rf *.aux
	rm -rf *.log
	rm -rf *.idx
	rm -rf *.synctex.gz
	rm -rf *.toc
	rm -rf *.tdo
	rm -rf *.bbl
	rm -rf *.bcf
	rm -rf *.blg
	rm -rf *.run.xml
	rm -rf *.lof
	rm -rf *.lot
	rm -rf $(NAME).pdf
