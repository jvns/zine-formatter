A small script for formatting zines suitable so that they can be printed on your home printer on US letter paper.
It uses pdftk/pdfjam/pdfcrop behind the scenes.

### Requirements

```
apt install pdfjam pdftk texlive-extra-utils 
```

Format requirements: the inputs to `--zine` and `--cover` must be 4inchx6inch files. (or at least a
2:3 aspect ratio)

### What it does

* Take an input zine like this: https://jvns.ca/strace-zine-v2.pdf
* Add a little padding to every page so that nothing gets cut off
* Truncate the input zine to the number of pages specified in `--pages`
* Create a US letter page booklet like this: https://jvns.ca/strace-zine-v2-print.pdf

There's also an optional `--cover` argument. If you include a cover, it'll cut off the first page of your zine and replace
it with the supplied cover page.

### Try it out!

```
# Fetch a zine to generate the print version of
git clone https://github.com/jvns/zine-formatter.py
cd zine-formatter
wget https://jvns.ca/strace-zine-v2.pdf
python zine-formatter.py \
  --zine strace-zine-v2.pdf \
  --pages 16 \
  --view-output strace-zine-view.pdf \
  --print-output strace-zine-print.pdf
```
