import argparse
import string
import random


PUNC_NO_QUOTE = string.punctuation.replace('"', '').replace("'", "")
DEFAULT_LENGTH = 16


def gen_passwd(length=DEFAULT_LENGTH):
    result = []
    result.append(random.choice(string.ascii_lowercase))
    result.append(random.choice(string.ascii_uppercase))
    result.append(random.choice(string.digits))
    result.append(random.choice(PUNC_NO_QUOTE))
    for i in range(length-len(result)):
        result.append(random.choice(
            string.ascii_letters +
            string.digits + PUNC_NO_QUOTE))
    random.shuffle(result)
    return ''.join(result)


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('users', nargs='*')
    argp.add_argument('-c', '--command')
    argp.add_argument('-l', '--length', default=DEFAULT_LENGTH, type=int,
                      help='length of password')
    args = argp.parse_args()

    if not args.users:
        print gen_passwd(args.length)
        return

    if args.command:
        import shlex
        cmd = shlex.split(args.command)

    for username in args.users:
        passwd = gen_passwd(args.length)
        print '{0}: {1}'.format(username, passwd)
        if args.command:
            cmd = shlex.split(args.command)
            import subprocess
            print subprocess.check_output(cmd + [passwd])


if __name__ == "__main__":
    main()
