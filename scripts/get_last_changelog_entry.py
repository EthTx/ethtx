import sys, os

lines = open(os.path.dirname(__file__) + "/../CHANGELOG.md").readlines()[3:]
was_last_line_blank = False
log = ""
for line in lines:
    if line == "\n":
        if was_last_line_blank:
            print(log)
            sys.exit(0)
        else:
            was_last_line_blank = True
    else:
        log += line
        was_last_line_blank = False
