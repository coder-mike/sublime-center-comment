import sublime, sublime_plugin, re

class CenterCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            lines = self.view.lines(region)
            for line in lines:
                text = self.view.substr(line)
                # // -------------------------- abc --------------------------
                m = re.match(r'^(.*?)(//+)(\s?)\s*([-=*]*)\s*?(\s?)(\w.*?)?([ -=*]*?)([ ]?)()$', text)

                # Try C style comment
                # /* ------------------------- abc ------------------------- */
                if not m:
                    m = re.match(r'^(.*?)(/\*+)(\s?)\s*([-=*]*)\s*?(\s?)(\w.*?)?([ -=*]*?)([ ]?)(\*/)$', text)

                if m:
                    print(m.groups())
                    titleText = m.group(6)
                    if not titleText:
                        titleText = ''
                    titleSpace = m.group(5) # Space on either side of the title
                    if len(m.group(4)) > 0:
                        padChar = m.group(4)[0]
                    else:
                        padChar = ' '
                        titleSpace = ''

                    trailingCommentMark = m.group(9)
                    if trailingCommentMark != '':
                        trailingSpace = m.group(3)
                    else:
                        trailingSpace = ''

                    lengthExclPad = len(m.group(1)) + len(m.group(2)) + len(m.group(3)) + len(titleSpace) * 2 + len(titleText) + len(trailingSpace) + len(trailingCommentMark)
                    wrapWidth = self.view.settings().get('wrap_width')
                    if wrapWidth == 0:
                        wrapWidth = 80
                    wrapWidth -= 1

                    numToAdd = int((wrapWidth - lengthExclPad) / 2)
                    if numToAdd < 0:
                        numToAdd = 0

                    newText = m.group(1) + m.group(2) + m.group(3) + (padChar * numToAdd) + titleSpace + titleText + titleSpace + (padChar * numToAdd) + trailingSpace + trailingCommentMark

                    # Remove trailing spaces, for the case that the padding char is itself a space
                    newText = re.sub(r'\s+$', '', newText)

                    self.view.replace(edit, line, newText)
