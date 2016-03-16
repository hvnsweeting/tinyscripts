#!/usr/bin/env python
import yaml


ALLOW_LEN = 50


def shortern(s):
    return str(s)[:ALLOW_LEN] + '.....' if len(str(s)) > ALLOW_LEN else s


def ddiff(d1, d2, depth=0, sign='+'):
    for k, v in d1.iteritems():
        if k in d2:
            if d1[k] == d2[k]:
                continue
            else:
                if isinstance(v, dict) and isinstance(d2[k], dict):
                    print '%s%s:' % (depth * '  ', k)
                    ddiff(v, d2[k], depth+1, sign)
                else:
                    print '%s%s: %s != %s' % (depth * '  ', k, shortern(v), shortern(d2[k]))
        else:
            print '%s%s%s: %s' % (sign, depth * '  ', shortern(k), shortern(v))


def main():
    import sys
    with open(sys.argv[1]) as f1, open(sys.argv[2]) as f2:
        d1 = yaml.load(f1)
        d2 = yaml.load(f2)
        ddiff(d1, d2)
        print '*' * 40
        ddiff(d2, d1, sign='-')


if __name__ == "__main__":
    main()
