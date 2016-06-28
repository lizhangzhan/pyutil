# -*- encoding: utf-8 -*-
import sys

class PrettyTable(object):
    def __init__(self):
        self.headers = None
        self.data = list([])

        self.padding_width = 1
        self.vchar = '|'
        self.hchar = '-'
        self.jchar = '+'

    def set_header(self, names):
        """ set the table header names
        Parameters
        ----------
        names : list of strs
          the header names
        """
        if not names or len(names) == 0:
            raise Exception("Header names is empty!")
        self.headers = names

    def add_row(self, row):
        """ add a row data to the table
        Parameters
        ----------
        row : list of values
          row of data, should be a list, length aligned with the table
        """
        if self.headers and len(row) != len(self.headers):
            raise Exception("row length is unaligned with header, row_len=%d, \
                    header_len = %d" % (len(row), len(self.headers)))
        if not self.headers:
            self.headers = ["Field %d" % (n+1) for n in xrange(len(row))]
        self.data.append(row)

    def _get_divider_line(self, col_widths):
        """get the header horizontal divider line"""
        divider_line = self.jchar
        divider_line += self.jchar.join([self.hchar * w for w in col_widths])
        divider_line += self.jchar
        return divider_line

    def _stringify_row(self, row, col_widths):
        fmt_row = []
        pw = self.padding_width
        for i in xrange(len(row)):
            if type(row[i]) is str:
                fmt_row.append(row[i].ljust(col_widths[i] - pw) + ' ' * pw)
            else:
                fmt_row.append(str(row[i]).rjust(col_widths[i] - pw) + ' ' * pw)
        return self.vchar + self.vchar.join(fmt_row) + self.vchar

    def _stringify_header(self, col_widths):
        fmt_header = []
        pw = self.padding_width
        for i in xrange(len(self.headers)):
            if type(self.data[0][i]) is str:
                fmt_header.append(self.headers[i].ljust(col_widths[i] - pw)
                        + ' ' * pw)
            else:
                fmt_header.append(self.headers[i].rjust(col_widths[i] - pw)
                        + ' ' * pw)
        return self.vchar + self.vchar.join(fmt_header) + self.vchar

    def pprint(self, out=sys.stdout):
        col_widths = []

        column_width = lambda c: max([len(str(row[c])) for row in self.data])
        # 1. get column width in print format
        for i in xrange(len(self.headers)):
            col_widths.append(max(column_width(i), len(self.headers[i])) + \
                    2 * self.padding_width)

        # 2. print header
        divider_line = self._get_divider_line(col_widths)
        print >> out, divider_line
        print >> out, self._stringify_header(col_widths)
        print >> out, divider_line

        # 3. print data
        for row in self.data:
            print >> out, self._stringify_row(row, col_widths)
        print >> out, divider_line

if __name__ == "__main__":
    pt = PrettyTable()
    pt.set_header(["name", "age", "salary"])
    pt.add_row(["xiaoming", 32, 225.5555])
    pt.add_row(["wanglei", 25, 68.5555])
    pt.pprint()
