import argparse
import random
import string
import subprocess as spr


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


def handle_command(cmd, passwd, stdin):
    if stdin:
        p = spr.Popen(cmd, stdin=spr.PIPE, stdout=spr.PIPE)
        out, err = p.communicate(input=passwd)
        if err:
            raise spr.CalledProcessError(err)
        print out.strip()
    else:
        print spr.check_output(cmd + [passwd])


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('users', nargs='*')
    argp.add_argument('-c', '--command')
    argp.add_argument('-i', '--stdin', action='store_true',
                      help='pass generated password to command' 'as stdin')
    argp.add_argument('-l', '--length', default=DEFAULT_LENGTH, type=int,
                      help='length of password')
    args = argp.parse_args()

    if args.command:
        import shlex
        cmd = shlex.split(args.command)
    elif args.stdin:
        print '--stdin must be used with --command'
        return

    if not args.users:
        passwd = gen_passwd(args.length)
        print passwd
        if args.command:
            handle_command(cmd, passwd, args.stdin)

    for username in args.users:
        passwd = gen_passwd(args.length)
        print '{0}: {1}'.format(username, passwd)

        if args.command:
            handle_command(cmd, passwd, args.stdin)


if __name__ == "__main__":
    main()
