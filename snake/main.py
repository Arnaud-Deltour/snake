import argparse

def hello():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-a', help="A text explaining what is the use of the -a option and what type of value it takes.")
    args = parser.parse_args()
    print(args)
    print("The value of -a is accessed with args.a: " + args.a)
    print('Hello World')