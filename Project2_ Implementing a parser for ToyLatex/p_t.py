__author__ = 'GaryGoh'
import sys
import parser
import pandas


def main(argv):
    # Write output to
    output_file_name = argv[1]
    output_file = file(output_file_name, 'w')
    sys.stdout = output_file

    retrieval_table = pandas.DataFrame(columns=["open_tag", "contents", "close_tag"])
    project2 = parser.TxtToTex(argv[0], retrieval_table)
    project2.info_retrival(parser.TxtToTex.xml_tag_retrieve)

    print project2.retrieval_table.sort()

    return


if __name__ == "__main__":
    main(sys.argv[1:])