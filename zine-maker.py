import subprocess
import tempfile
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--zine', required=True)
    parser.add_argument('--pages', required=True, type=multiple_of_four)
    parser.add_argument('--print-output', required=True)
    parser.add_argument('--view-output', required=True)
    parser.add_argument('--cover')
    return parser.parse_args()


def multiple_of_four(value):
    i = int(value)
    if i % 4 != 0:
         raise argparse.ArgumentTypeError("Number of pages (%s) is not a multiple of four" % i)
    return i

def run(args):
    print(args)
    if type(args) == list:
        subprocess.check_call(args)
    else:
        subprocess.check_call(args.split())

def temp_filename():
    return tempfile.mktemp('.pdf')


def make_zine(zine, pages, print_output, view_output, cover=None):
    if cover is not None:
        inside = temp_filename()
        cover_resized = temp_filename()
        zine_step1 = temp_filename()
        run("pdftk {zine} cat 2-{pages} output {inside}".format(
            zine=zine,
            pages=pages,
            inside=inside))
        run(['pdfjam', '--outfile', cover_resized, '--papersize', '{4in,6in}', cover])
        run(['pdftk', cover_resized, inside, 'cat', 'output', zine_step1])
    else:
        inside = temp_filename()
        run("pdftk {zine} cat 1-{pages} output {inside}".format(zine=zine, pages=pages, inside=inside))
        zine_step1 = inside
    run(['pdfcrop', '--margin', '14 0 14 0', zine_step1, view_output])
    run(['pdfjam', '--booklet', 'true', '--landscape', '--suffix', 'book', '--letterpaper',
    '--signature', '12', '--booklet', 'true', '--scale', '1.0', '--offset', '0cm 0cm',
    '--landscape', view_output, '-o', print_output])

if __name__ == '__main__':
    args = parse_args()
    make_zine(args.zine, args.pages, args.print_output, args.view_output, cover=args.cover)


