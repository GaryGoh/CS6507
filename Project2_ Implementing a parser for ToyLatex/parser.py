__author__ = 'GaryGoh'

import re
import sys
import pandas


class TxtToTex():
    # new a data structure for storing retrieval information
    # retrieval_table = None

    # pattern of regular expression
    xml_tag_retrieve = re.compile(r"(<.*?>)(.*?)(</.*?>)")
    tag_first_row_retrieve = re.compile(r"(<.*?>)(\w+)")

    def __init__(self, name, table):
        self.name = name
        self.retrieval_table = table
        self.index = 0

    def documentclass(self, documentclass):
        print "\\documentclass{%s}" % (documentclass)

    def usepackage(self, usepackage):
        print "\\usepackage{%s}" % (usepackage)

    def hline(self):
        print "\\hline"

    def begin_one_parameter(self, begin):
        print "\\begin{%s}" % (begin)

    def begin_two_parameters(self, begin1, begin2):
        print "\\begin{%s}{%s}" % (begin1, begin2)

    def textcolor(self, color, text):
        print "\\textcolor{%s}{%s}" % (color, text)

    def end(self, end_tag):
        print "\\end{%s}" % (end_tag)

    def includegraphics(self, width, pic):
        print "\\includegraphics[width={%f}\\textwidth]{%s}" % (width, pic)

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
                        print row.replace(",", " & ") + "\\\\"
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

                    # Refine the retrieved data to be latex format
                    for row in table_contents:
                        print row
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
            # tag_retrival = re.search(r"(<.*?>)(.*?)(</.*?>)", combine_lines, re.M)
            regex_result = pattern.search(combine_lines)

            if regex_result:
                # new_file_DT.append((str(tag_retrival.group(1)), str(tag_retrival.group(2))))
                self.retrieval_table.loc[-1] = [regex_result.group(1), regex_result.group(2), regex_result.group(3),
                                                self.index]
                self.retrieval_table.index += 1
                self.index += 1
                combine_lines = ""
            else:
                continue


def main(argv):
    # Write output to
    output_file_name = argv[1]
    output_file = file(output_file_name, 'w')
    sys.stdout = output_file

    retrieval_table = pandas.DataFrame(columns=["open_tag", "contents", "close_tag", "index"])
    project2 = TxtToTex(argv[0], retrieval_table)
    project2.info_retrival(TxtToTex.xml_tag_retrieve)

    project2.documentclass("artical")
    project2.usepackage("color")
    project2.usepackage("graphicx")

    project2.begin_one_parameter("document")
    project2.textcolor("red", "ToyLatex")
    project2.print_paragraph(1)
    project2.print_table(1)
    project2.print_paragraph(2)
    project2.print_graphics(1)
    project2.end("document")


    # print project2.retrieval_table

    return


if __name__ == "__main__":
    main(sys.argv[1:])

