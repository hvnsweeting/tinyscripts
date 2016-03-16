import yaml


def ddiff(d1, d2, depth=0):
    for k, v in d1.iteritems():
        if k in d2:
            if d1[k] == d2[k]:
                continue
            else:
                if isinstance(v, dict) and isinstance(d2[k], dict):
                    print '%s%s:' % (depth * '  ', k)
                    ddiff(v, d2[k], depth+1)
                else:
                    print '%s%s: %s != %s' % (depth * '  ', k, v, d2[k])
        else:
            print '%s%s:...' % (depth * '  ', k)


def test():
    da = {'a': {'b': {'1': 1}}, 'b': {2: 3}}
    db = {'a': {'c': '1'}, 'c': {2: 3}}
    print da
    print db
    ddiff(da, db)
    print '*' * 40
    ddiff(db, da)


def main():
    import sys
    with open(sys.argv[1]) as f1, open(sys.argv[2]) as f2:
        d1 = yaml.load(f1)
        d2 = yaml.load(f2)
        ddiff(d1, d2)
        print '*' * 40
        ddiff(d2, d1)


if __name__ == "__main__":
    main()
