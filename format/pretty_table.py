# -*- encoding: utf-8 -*-
import sys

class PrettyTable(object):
    def __init__(self):
        self.header_names = None
        self.margin_width = 1
        self.data = list([])

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
        self.header_names = names

    def add_row(self, row):
        """ add a row data to the table
        Parameters
        ----------
        row : list of values
          row of data, should be a list, length aligned with the table
        """
        if self.header_names and len(row) != len(self.header_names):
            raise Exception("row length is unaligned with header, row_len=%d, \
                    header_len = %d" % (len(row), len(self.header_names)))
        if not self.header_names:
            self.header_names = ["Field %d" % (n+1) for n in xrange(len(row))]
        self.data.append(row)

    def _get_divider_line(self, col_widths):
        divider_line = self.jchar
        divider_line += self.jchar.join([self.hchar * w for w in col_widths])
        divider_line += self.jchar
        return divider_line

    def _stringfy_row(self, row, col_widths):
        fmt_row = []
        for i in xrange(len(row)):
            if type(row[i]) is str:
                fmt_row.append(row[i].ljust(col_widths[i]))
            else:
                fmt_row.append(str(row[i]).rjust(col_widths[i]))
        return self.vchar + self.vchar.join(fmt_row) + self.vchar

    def pprint(self, out=sys.stdout):
        col_widths = []

        get_column_width = lambda c: max([len(str(row[c])) for row in self.data])
        # get column width in print format
        for i in xrange(len(self.header_names)):
            col_widths.append((get_column_width(i) + 2 * self.margin_width))

        # print header
        divider_line = self._get_divider_line(col_widths)
        print >> out, divider_line
        fmt_header = []
        for i in xrange(len(self.header_names)):
            if type(self.data[0][i]) is str:
                fmt_header.append(self.header_names[i].ljust(col_widths[i]))
            else:
                fmt_header.append(self.header_names[i].rjust(col_widths[i]))
        print >> out, self.vchar + self.vchar.join(fmt_header) + self.vchar
        print >> out, divider_line

        # print data
        for row in self.data:
            print >> out, self._stringfy_row(row, col_widths)
        print >> out, divider_line

if __name__ == "__main__":
    pt = PrettyTable()
    pt.set_header(["name", "age", "salary"])
    pt.add_row(["xiaoming", 23, 25.5555])
    pt.add_row(["wanglei", 25, 25.5555])
    pt.pprint()
