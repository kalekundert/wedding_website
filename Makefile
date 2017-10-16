## Define the structure of the site.
CONTENT   := content
THEME     := theme
BUILD	  := build

## Define the commands that will be used to generate the site.
JINJA     	:= jinja2 --template-dir $(THEME) --trim-whitespace
SASS		:= sass
COPY		:= cp

## Work out the paths for all the files we need to generate.
INCLUDE_RULES := \
	-type f \
	-not -name '*.swp' \
	-not -name '*.html'

CONTENT_HTML_IN := $(wildcard $(CONTENT)/*.html)
CONTENT_HTML_OUT := $(patsubst \
	$(CONTENT)/%.html, $(BUILD)/%.html, $(CONTENT_HTML_IN))

CONTENT_IN := $(filter-out \
	$(CONTENT_HTML_IN), \
	$(shell find $(CONTENT) $(INCLUDE_RULES)))
CONTENT_OUT := $(patsubst \
	$(CONTENT)/%, $(BUILD)/%, $(CONTENT_IN))

THEME_HTML := $(wildcard $(THEME)/*.html)
THEME_SCSS_IN := $(wildcard $(THEME)/*.scss)
THEME_CSS_OUT := $(patsubst \
	$(THEME)/%.scss, $(BUILD)/%.css, $(THEME_SCSS_IN))

THEME_IN := $(filter-out \
	$(THEME_HTML) $(THEME_SCSS_IN), \
	$(shell find $(THEME) $(INCLUDE_RULES)))
THEME_OUT := $(patsubst \
	$(THEME)/%, $(BUILD)/%, $(THEME_IN))

ALL_OUTPUTS := \
	$(CONTENT_OUT) $(CONTENT_HTML_OUT) \
	$(THEME_OUT) $(THEME_CSS_OUT) 

## Specify how to build the site.
html: $(ALL_OUTPUTS)

$(BUILD)/%.html : $(CONTENT)/%.html $(THEME_HTML)
	$(JINJA) $< > $@.tmp
	@mv $@.tmp $@

$(BUILD)/%.css : $(THEME)/%.scss
	$(SASS) $^ $@

$(BUILD)/% : $(CONTENT)/%
	@mkdir -p $(shell dirname $@)
	$(COPY) $^ $@

$(BUILD)/% : $(THEME)/%
	@mkdir -p $(shell dirname $@)
	$(COPY) $^ $@

upload: site
	rsync

clean:
	rm -rf $(BUILD)/*

test:
	@echo 'CONTENT_OUT:       ' $(CONTENT_OUT)
	@echo 'CONTENT_HTML_OUT:  ' $(CONTENT_HTML_OUT)
	@echo 'THEME_OUT:         ' $(THEME_OUT)
	@echo 'THEME_CSS_OUT:     ' $(THEME_CSS_OUT)

.PHONY = html clean upload

