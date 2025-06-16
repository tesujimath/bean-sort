#!/usr/bin/env python

import datetime
import re
import sys
import tempfile


def main():
    directive_re = re.compile(r"^(\d{4}-\d{2}-\d{2})", re.MULTILINE)
    for inpath in sys.argv[1:]:
        outpath = f"{inpath}.sorted"
        print(f"processing {inpath}")
        with open(inpath) as in_f:
            content = in_f.read()
            records = directive_re.split(content)
            if len(records) % 2 != 1:
                print("fatal error, even number of records")
            by_date = {}
            for i in range(len(records) // 2):
                date_str = records[2 * i + 1]
                d = datetime.date.fromisoformat(date_str).toordinal()
                body = date_str + records[2 * i + 2]
                # print(f"<<< {date}{body} >>>")
                if d in by_date:
                    by_date[d].append(body)
                    # print(f"appending {body} to {d}", file=sys.stderr)
                else:
                    by_date[d] = [body]
                    # print(f"initializing {body} in {d}", file=sys.stderr)

            for d in sorted(by_date.keys()):
                for body in by_date[d]:
                    sys.stdout.write(body)


if __name__ == "__main__":
    main()
