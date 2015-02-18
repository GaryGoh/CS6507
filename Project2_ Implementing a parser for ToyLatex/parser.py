__author__ = 'GaryGoh'

import re
import sys
import pandas


class TxtToTex(object):
    # name, the name of target file
    # retrieval_table, the table using pandas to store retrieving information
    # index, for sort table and index when searching
    # output, the output file what user defines

    # pattern of regular expression
    # match <tag>contents</tag>
    xml_tag_retrieve = re.compile(r"(<.*?>)(.*?)(</.*?>)")
    # match <tag>contents, this regrex is used for defining table because there is one line is to be header.
    tag_first_row_retrieve = re.compile(r"(<.*?>)(\w+)")

    def __init__(self, name, table, output):
        self.name = name
        self.retrieval_table = table
        self.index = 0
        self.output = file(output, "w")

    def documentclass(self, documentclass):
        self.output.write("\\documentclass{%s}\n" % (documentclass))

    def usepackage(self, usepackage):
        self.output.write("\\usepackage{%s}\n" % (usepackage))

    def hline(self):
        self.output.write("\\hline\n")

    def begin_one_parameter(self, begin):
        self.output.write("\n\\begin{%s}\n" % (begin))

    def begin_two_parameters(self, begin1, begin2):
        self.output.write("\\begin{%s}{%s}\n\n" % (begin1, begin2))

    def textcolor(self, color, text):
        self.output.write("\\textcolor{%s}{%s}\n\n" % (color, text))

    def end(self, end_tag):
        self.output.write("\\end{%s}\n" % (end_tag))

    def includegraphics(self, width, pic):
        self.output.write("\\includegraphics[width=%f\\textwidth]{%s}\n" % (width, pic))

    def print_table(self, number_of_occurs):

        table_occurs = 0
        self.begin_one_parameter("center")

        # Find out the table tag contents
        for data_index, data_row in self.retrieval_table.iterrows():
            if self.retrieval_table.ix[data_index, "open_tag"] == "<table>":
                table_occurs += 1
                if table_occurs == number_of_occurs:
                    # When occurs the ith table that you want
                    table_contents = self.retrieval_table.ix[data_index, "contents"].split()

                    # get the length of header and print the time of "r"
                    self.begin_two_parameters("tabular", len(table_contents[0].replace(",", "")) * "r")

                    # Refine the retrieved data to be latex format
                    for row in table_contents:
                        if table_contents.index(row) == 0:
                            self.hline()
                            self.output.write(row.replace(",", " & ") + "\\\\\n")
                            self.hline()
                        else:
                            self.output.write(row.replace(",", " & ") + "\\\\\n")

                    break
                elif table_occurs < number_of_occurs:
                    continue
                else:
                    raise Exception("Not such more contents from the data.")

        self.end("tabular")
        self.end("center")

    def print_paragraph(self, number_of_occurs):

        table_occurs = 0

        # Find out the table tag contents
        for data_index, data_row in self.retrieval_table.iterrows():
            if self.retrieval_table.ix[data_index, "open_tag"] == "<paragraph>":
                table_occurs += 1
                if table_occurs == number_of_occurs:
                    # When occurs the ith table that you want
                    table_contents = self.retrieval_table.ix[data_index, "contents"].split()

                    self.output.write("\n")
                    for row in table_contents:
                        # all words are no space after split() then refine the format.
                        self.output.write(row + " ")
                    self.output.write("\n")
                    break
                elif table_occurs < number_of_occurs:
                    continue
                else:
                    raise Exception("Not such more contents from the data.")


    def print_graphics(self, number_of_occurs):
        table_occurs = 0
        self.begin_one_parameter("center")

        # Find out the table tag contents
        for data_index, data_row in self.retrieval_table.iterrows():
            if self.retrieval_table.ix[data_index, "open_tag"] == "<figure>":
                table_occurs += 1
                if table_occurs == number_of_occurs:
                    # When occurs the ith table that you want
                    table_contents = self.retrieval_table.ix[data_index, "contents"].split()

                    # print out graphics
                    # includegraphics(width, figure name)
                    self.includegraphics(0.5, table_contents[0])
                    break
                elif table_occurs < number_of_occurs:
                    continue
                else:
                    raise Exception("Not such more contents from the data.")

        self.end("center")

    def info_retrival(self, pattern):
        # read object file
        txt_file = open(self.name, "r")

        # for culmulated store lines
        combine_lines = ""

        # read txt file line by line
        for line in txt_file.readlines():
            combine_lines += " " + line.rstrip('\n')
            regex_result = pattern.search(combine_lines)

            if regex_result:
                self.retrieval_table.loc[-1] = [regex_result.group(1), regex_result.group(2), regex_result.group(3),
                                                self.index]
                self.retrieval_table.index += 1
                self.index += 1
                combine_lines = ""
            else:
                continue


def main(argv):
    # new a pandas table for storing data
    retrieval_table = pandas.DataFrame(columns=["open_tag", "contents", "close_tag", "index"])

    # new a instance for a parser.
    project2 = TxtToTex(argv[0], retrieval_table, argv[1])
    project2.info_retrival(TxtToTex.xml_tag_retrieve)

    # The top statements from latex file.
    project2.documentclass("article")
    project2.usepackage("color")
    project2.usepackage("graphicx")

    # Each session retrieved from regrex, after refining format and output.
    project2.begin_one_parameter("document")
    project2.textcolor("red", "ToyLatex")
    project2.print_paragraph(1)
    project2.print_paragraph(2)
    project2.print_table(1)
    project2.print_paragraph(3)
    project2.print_graphics(1)

    # End of latex
    project2.end("document")

    return


if __name__ == "__main__":
    main(sys.argv[1:])

