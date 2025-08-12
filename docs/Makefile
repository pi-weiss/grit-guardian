# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= poetry run sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean livehtml apidoc linkcheck

# Clean build directory
clean:
	rm -rf "$(BUILDDIR)"
	rm -rf "$(SOURCEDIR)/api/generated"

# Live reload development server
livehtml:
	poetry run sphinx-autobuild -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" \
		--host 0.0.0.0 \
		--port 8000 \
		--open-browser \
		--watch ../grit_guardian \
		--ignore "*.pyc" \
		--ignore "**/__pycache__/**"

# Generate API documentation from source code
apidoc:
	poetry run sphinx-apidoc -f -o "$(SOURCEDIR)/api/generated" "../src/grit_guardian" \
		--separate \
		--module-first \
		--no-toc

# Check all links in documentation
linkcheck:
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS) $(O)

# Build HTML documentation
html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Build PDF documentation (requires LaTeX)
latexpdf:
	@$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex" $(SPHINXOPTS) $(O)
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C "$(BUILDDIR)/latex" all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

# Build EPUB documentation
epub:
	@$(SPHINXBUILD) -b epub "$(SOURCEDIR)" "$(BUILDDIR)/epub" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

# Check documentation for common issues
doctest:
	@$(SPHINXBUILD) -b doctest "$(SOURCEDIR)" "$(BUILDDIR)/doctest" $(SPHINXOPTS) $(O)

# Build documentation and check for warnings/errors
stricthtml:
	@$(SPHINXBUILD) -b html -W --keep-going "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Development targets
.PHONY: dev-install dev-clean dev-build

# Install development dependencies
dev-install:
	poetry install --with=dev

# Clean and rebuild everything
dev-clean: clean apidoc html

# Quick development build
dev-build: html
	@echo "Documentation available at: file://$(PWD)/$(BUILDDIR)/html/index.html"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
