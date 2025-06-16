#!/usr/bin/env python

import datetime
import re
import sys
import tempfile


def main():
    directive_re = re.compile(r"^(\d{4}-\d{2}-\d{2})", re.MULTILINE)
    by_date = {}

    for path in sys.argv[1:]:
        with open(path) as in_f:
            content = in_f.read()
            records = directive_re.split(content)
            if len(records) % 2 != 1:
                print("fatal error, even number of records", file=sys.stderr)
                sys.exit(1)
            for i in range(len(records) // 2):
                date_str = records[2 * i + 1]
                d = datetime.date.fromisoformat(date_str).toordinal()
                body = date_str + records[2 * i + 2]
                if d in by_date:
                    by_date[d].append(body)
                else:
                    by_date[d] = [body]

    for d in sorted(by_date.keys()):
        for body in by_date[d]:
            sys.stdout.write(body)


if __name__ == "__main__":
    main()
