# If any subdir has a makefile, run that makefile and don't do anything else to 
# those files?

## Configure how to connect to the server.
WEB_SERVER		:= kalekundert_borecole@ssh.phx.nearlyfreespeech.net
WEB_DIR			:= 

## Define the structure of the site.
CONTENT			:= content
THEME			:= theme
NAVBAR			:= theme/navbar
BUILD			:= build

## Define the commands that will be used to generate the site.
JINJA			:= jinja2 --template-dir $(THEME) --trim-whitespace
SASS			:= sass
COPY			:= cp
RSYNC			:= rsync -av --delete

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

GALLERY_HTML_OUT := \
	$(BUILD)/welcome.html \
	$(BUILD)/gallery.html
GALLERY_HTML_DEP := \
	$(CONTENT)/pictures/pictures_with_captions.html

NAVBAR_IN := $(wildcard $(NAVBAR)/*)
NAVBAR_PNG_IN := \
	$(NAVBAR)/make_spritesheet.sh \
	$(NAVBAR)/sprite_link.png \
	$(NAVBAR)/sprite_hover.png \
	$(NAVBAR)/sprite_current.png
NAVBAR_PNG_OUT := \
	$(BUILD)/navbar.png
NAVBAR_CSS_IN := \
	$(NAVBAR)/make_css.py \
	$(NAVBAR)/sprite_divisions.png \
	$(NAVBAR)/navbar.scss.jinja
NAVBAR_CSS_OUT := \
	$(BUILD)/navbar.css

THEME_HTML := $(wildcard $(THEME)/*.html) $(THEME)/make_page.py
THEME_SCSS_IN := $(wildcard $(THEME)/*.scss)
THEME_CSS_OUT := $(patsubst \
	$(THEME)/%.scss, $(BUILD)/%.css, $(THEME_SCSS_IN))

THEME_IN := $(filter-out \
	$(THEME_HTML) $(THEME_SCSS_IN) $(NAVBAR_IN), \
	$(shell find $(THEME) $(INCLUDE_RULES)))
THEME_OUT := $(patsubst \
	$(THEME)/%, $(BUILD)/%, $(THEME_IN))

ALL_OUTPUTS := \
	$(CONTENT_OUT) $(CONTENT_HTML_OUT) \
	$(THEME_OUT) $(THEME_CSS_OUT) \
	$(NAVBAR_PNG_OUT) $(NAVBAR_CSS_OUT)

## Specify how to build the site.
html: $(ALL_OUTPUTS)

$(BUILD)/%.html : $(CONTENT)/%.html $(THEME_HTML)
	$(THEME)/make_page.py $< > $@

$(GALLERY_HTML_OUT) : $(GALLERY_HTML_DEP)

$(NAVBAR_PNG_OUT) : $(NAVBAR_PNG_IN)
	$(NAVBAR)/make_spritesheet.sh $@

$(NAVBAR_CSS_OUT) : $(NAVBAR_CSS_IN)
	$(NAVBAR)/make_css.py > $@

$(BUILD)/%.css : $(THEME)/%.scss
	$(SASS) $^ $@

$(BUILD)/% : $(CONTENT)/%
	@mkdir -p $(shell dirname $@)
	$(COPY) $^ $@

$(BUILD)/% : $(THEME)/%
	@mkdir -p $(shell dirname $@)
	$(COPY) $^ $@

upload: html
	$(RSYNC) $(BUILD)/ $(WEB_SERVER):

clean:
	rm -rf $(BUILD)/*

.PHONY = html clean upload

