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
    parser.add_argument('--size')
    parser.add_argument('--trim-bottom')
    parser.add_argument('--cover')
    parser.add_argument('--bw', dest='bw', action='store_true')
    parser.add_argument('--rotate', dest='rotate', action='store_true')

    return parser.parse_args()


def multiple_of_four(value):
    i = int(value)
    if i % 4 != 0:
         raise argparse.ArgumentTypeError("Number of pages (%s) is not a multiple of four" % i)
    return i

def run(args):
    if len(args) > 10:
        print(args)
    else:
        print(' '.join(args))
    if type(args) == list:
        subprocess.check_call(args)
    else:
        subprocess.check_call(args.split())

def temp_filename():
    return tempfile.NamedTemporaryFile(delete=False, dir='.', suffix='.pdf').name


def make_zine(zine, pages, print_output, view_output, trim_bottom='0mm', cover=None, size=None, bw=False, rotate=False):
    cropped = temp_filename()
    run(['pdfcrop', zine, cropped])
    zine = cropped
    if rotate:
        zine_rotated = temp_filename()
        cover_rotated = temp_filename()
        run("pdftk {zine} rotate 1-{pages}west output {rotated}".format(
            zine=zine,
            pages=pages,
            rotated=zine_rotated))
        zine = zine_rotated
        if cover is not None:
            run("pdftk {cover} rotate 1-1west output {cover_rotated}".format(cover=cover,
                cover_rotated=cover_rotated))
            cover = cover_rotated
    if cover is not None:
        cover_resized = temp_filename()
        zine_resized = temp_filename()
        zine_step1 = temp_filename()
        inside = temp_filename()
        run("pdftk {zine} cat 2-{pages} output {inside}".format(
            zine=zine,
            pages=pages,
            inside=inside))
        run(['pdfjam', '--outfile', zine_resized, '--papersize', '{4in,6in}', inside])
        run(['pdfjam', '--outfile', cover_resized, '--papersize', '{4in,6in}', cover])
        if bw:
            zine_bw = temp_filename()
            run("convert -density 600 {zine_resized} -negate -threshold 0 -negate {zine_bw}".format(zine_resized=zine_resized,
                zine_bw=zine_bw))
            zine_resized = zine_bw
        run(['pdftk', cover_resized, zine_resized, 'cat', 'output', zine_step1])
    else:
        inside = temp_filename()
        run("pdftk {zine} cat 1-{pages} output {inside}".format(zine=zine, pages=pages, inside=inside))
        zine_step1 = inside
    run(['pdfcrop', '--margin', '14 0 14 0', zine_step1, view_output])
    if size is None:
        size_arg = '--letterpaper'
    elif size == 'a4':
        size_arg = '--a4paper'
    run(['pdfjam', '--booklet', 'true', '--landscape', '--suffix', 'book', size_arg,
    '--signature', '12', '--booklet', 'true', '--trim', '0mm 0mm %s 0mm' % trim_bottom, '--clip' , 'true', '--scale', '1.0', '--offset', '0cm 0cm',
    '--landscape', view_output, '-o', print_output])

if __name__ == '__main__':
    args = parse_args()
    make_zine(args.zine, args.pages, args.print_output, args.view_output, trim_bottom=args.trim_bottom, size=args.size, cover=args.cover, bw=args.bw, rotate=args.rotate)


