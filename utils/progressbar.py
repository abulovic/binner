import sys

def get_progress (perc):
    perc = float(perc)
    if perc < 0. or perc > 100.:
        raise ValueError('Progress bar percentage out of range (%f)' % perc)
    perc = int(perc);
    perc_str = "<" + "="*perc + " "*(100-perc) + ">" + " %3d%%" % perc
    return perc_str

def print_progress (perc):
    progress = get_progress
    sys.stdout.write(progress + "\r")
    sys.stdout.flush()

if __name__ == '__main__':
    import time
    for i in range(1,101):
        time.sleep(1)
        progress = get_progress(i) + "\r"
        sys.stdout.write(progress)
        sys.stdout.flush()