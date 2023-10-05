import argparse


def httpc_get(args):
    # Implement HTTP GET logic here
    print("HTTP GET Request")
    print("Verbose:", args.verbose)
    print("URL:", args.URL)
    print("Headers:", args.headers)


def httpc_post(args):
    # Implement HTTP POST logic here
    print("HTTP POST Request")
    print("Verbose:", args.verbose)
    print("URL:", args.URL)
    print("Headers:", args.headers)
    print("Data from Inline Data (-d):", args.data)
    print("Data from File (-f):", args.file.read())


def main():
    parser = argparse.ArgumentParser(description="httpc (get|post) [-v] (-h 'k:v')* [-d inline-data] [-f file] URL")
    subparsers = parser.add_subparsers(help="Available commands", dest="command")

    # Subparser for the "get" command
    get_parser = subparsers.add_parser("get", help="Perform an HTTP GET request")
    get_parser.add_argument("URL", help="The URL to send the GET request to")
    get_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    get_parser.add_argument("-h", "--headers", nargs='+', help="Additional headers in the format 'key:value'")
    get_parser.set_defaults(func=httpc_get)

    # Subparser for the "post" command
    post_parser = subparsers.add_parser("post", help="Perform an HTTP POST request")
    post_parser.add_argument("URL", help="The URL to send the POST request to")
    post_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    post_parser.add_argument("-h", "--headers", nargs='+', help="Additional headers in the format 'key:value'")
    post_parser.add_argument("-d", "--data", help="Inline data for the POST request")
    post_parser.add_argument("-f", "--file", type=argparse.FileType('r'),
                             help="File containing data for the POST request")
    post_parser.set_defaults(func=httpc_post)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
