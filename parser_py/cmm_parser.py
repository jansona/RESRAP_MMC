import sys, getopt
from subparser.sig_table import get_key
from subparser.lex_parser import LexParser
from subparser.syntax_parser import SyntaxParser
from subparser.forms import commands
from subparser.inter_runner import InterRunner


class CmmParser(object):

    def __init__(self, lparser, sparser):
        self.lparser = lparser
        self.sparser = sparser

    def covert_int2str(self, tokens):
        for token in tokens:
            token.idt = get_key(token.idt)[0]

    def parse(self, ifilename, ofilename=None, show_lex=False, show_syntax=False, file_name=None, draw_graph=False, checkpoints=[]):
        code_str = None

        with open(ifilename, 'r') as fin:
            code_str = '\n'.join(fin.readlines())

        tokens = self.lparser.parse_sentence(code_str)
        self.covert_int2str(tokens)

        if show_lex:
            self.lparser.check_tokens_2(tokens, file_name=file_name)

        if self.sparser.parse_tokens(tokens, show_syntax=show_syntax, file_name=file_name, draw_graph=draw_graph, checkpoints=checkpoints):
            print("Succeeded")
        else:
            print("Failed")


help_str = """
Usage: python cmm_parser.py source_file [options]
Options:
    -h, --help   Show this help
    -l, --lex    Show the intermediate result of the lex parsing
    -s, --syntax Show the process of the syntax parsing
    -f, --file   Write the intermediate result to a file with the name same as the source file
    -c, --check=[n,...]  Set the checkpoints
"""

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hlsfgo:c:", ["check=", "output=", "help", "lex", "syntax", "file", "graph"])
        
        if len(args) != 1:
            raise Exception

    except getopt.GetoptError:
        print(help_str)
        sys.exit(1)
    except Exception:
        print(help_str)
        sys.exit(1)

    infile = args[0]
    outfile = None

    is_show_lex = False
    is_show_syntax = False
    file_name = None
    draw_graph = False
    checkpoints = []
    
    for opt, arg in opts:
        if opt in ("-o", "--output"):
            outfile = arg
        elif opt in ("-h", "--help"):
            print(help_str)
        elif opt in ("-l", "--lex"):
            is_show_lex = True
        elif opt in ("-s", "--syntax"):
            is_show_syntax = True
        elif opt in ("-f", "--file"):
            file_name = infile.split(".cmm")[0]
        elif opt in ("-g", "--graph"):
            draw_graph = True
        elif opt in ("-c", "--check"):
            checkpoints = eval(arg)

    if not outfile:
        outfile = infile.split(".")

    parser = CmmParser(LexParser(), SyntaxParser())

    parser.parse(infile, ofilename=outfile, show_lex=is_show_lex, show_syntax=is_show_syntax, 
            file_name=file_name, draw_graph=draw_graph, checkpoints=checkpoints)

    runner = InterRunner()
    runner(commands)


def test():
    parser = CmmParser(LexParser(), SyntaxParser())  
    parser.parse("test_code.cmm", show_lex=False, show_syntax=False)  

    for index, cmd in enumerate(commands):
        print("{:3}: ({:^6},{:^6},{:^6},{:^6})".format(index, cmd.op, str(cmd.arg0), str(cmd.arg1), str(cmd.result)))

    runner = InterRunner()
    runner(commands)


if __name__ == '__main__':
    # test()
    main(sys.argv[1:])
