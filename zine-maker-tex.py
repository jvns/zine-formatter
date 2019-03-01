import subprocess
import tempfile
import sys
import argparse
from jinja2 import Template

TEMPLATE = Template('''
\\batchmode
\\documentclass[{{papersize}},landscape]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[monochrome]{xcolor}
\\usepackage{pdfpages}

\\begin{document}

{% if should_print -%}
\\includepdfmerge[booklet=true,landscape=true,signature=12,scale=1.0,offset=0cm 0cm,trim=0mm {{trim_bottom}} 00mm 00mm,clip]{
{%- else %}
\includepdfmerge[trim=0mm {{trim_bottom}} 0mm 0mm,clip]{
{%- endif %}
{{cover}},
{{zine}},2-{{pages}}}

\end{document}
''')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--zine', required=True)
    parser.add_argument('--pages', required=True)
    parser.add_argument('--print-output', required=True)
    parser.add_argument('--view-output')
    parser.add_argument('--papersize', default='letter')
    parser.add_argument('--trim-bottom', default='0mm')
    parser.add_argument('--cover')
    parser.add_argument('--bw', dest='bw', action='store_true')
    parser.add_argument('--rotate', dest='rotate', action='store_true')

    return parser.parse_args()

def run(args):
    print(' '.join(args))
    subprocess.check_call(args)

import os

def temp_filename():
    return tempfile.NamedTemporaryFile(delete=False, dir='tmp', suffix='.pdf').name

def render(zine=None, pages=None, should_print=None, trim_bottom=None, cover=None, rotate=None,
        papersize=None, filename=None):
    latex = TEMPLATE.render(zine=zine, pages=pages,
            should_print=should_print, trim_bottom=trim_bottom,
            cover=cover,
            rotate=rotate, papersize=papersize)
    tex_file = '%s.tex' % filename.replace('.pdf', '')
    with open(tex_file, 'w') as f:
        f.write(latex)
    run(["pdflatex", tex_file])
    if os.path.basename(filename) != filename:
        run(["mv", os.path.basename(filename), filename])

if __name__ == '__main__':
    args = parse_args()

    temp_cover = temp_filename()

    if args.trim_bottom:
        run(["pdfcrop", "--margins", "0 0 00 800", args.cover, "asdf2.pdf"])
        run(["pdfjam", "--outfile", temp_cover, "--papersize", "{8.5in,11in}", "asdf2.pdf"])
    if args.view_output:
        render(zine=args.zine, pages=args.pages,
                should_print=False, trim_bottom=args.trim_bottom,
                cover=temp_cover,
                rotate=args.rotate, papersize=args.papersize, filename=args.view_output)
    render(zine=args.zine, pages=args.pages,
            should_print=True, trim_bottom=args.trim_bottom,
            cover='asdf.pdf',
            rotate=args.rotate, papersize=args.papersize, filename=args.print_output)

