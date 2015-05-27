import sublime, sublime_plugin, re

# Copied from https://github.com/gkhn/SectionComment/blob/f94b87b82ff261b009a402710a43af362234376b/SectionComment.py#L6-L35
def build_comment_data(view, pt):
    shell_vars = view.meta_info("shellVariables", pt)
    print (shell_vars)
    if not shell_vars:
        return ([], [])

    # transform the list of dicts into a single dict
    all_vars = {}
    for v in shell_vars:
        if 'name' in v and 'value' in v:
            all_vars[v['name']] = v['value']

    line_comments = []
    block_comments = []

    # transform the dict into a single array of valid comments
    suffixes = [""] + ["_" + str(i) for i in range(1, 10)]
    for suffix in suffixes:
        start = all_vars.setdefault("TM_COMMENT_START" + suffix)
        end = all_vars.setdefault("TM_COMMENT_END" + suffix)
        mode = all_vars.setdefault("TM_COMMENT_MODE" + suffix)
        disable_indent = all_vars.setdefault("TM_COMMENT_DISABLE_INDENT" + suffix)

        if start and end:
            block_comments.append((start.strip(), end.strip(), disable_indent == 'yes'))
            block_comments.append((start, end, disable_indent == 'yes'))
        elif start:
            line_comments.append((start.strip(), disable_indent == 'yes'))
            line_comments.append((start, disable_indent == 'yes'))

    return (line_comments, block_comments)

class CenterCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("center_comment.sublime-settings")
        line_width = settings.get('line_width')
        if not isinstance(line_width, int):
            line_width = self.view.settings().get('wrap_width')
        if not line_width:
            line_width = 79

        for region in self.view.sel():
            lines = self.view.lines(region)
            for line in lines:
                line_comments, block_comments = build_comment_data(self.view, line.begin())

                text = self.view.substr(line)
                # Line comments
                m = None
                for line_comment in line_comments:
                    m = re.match(r'^(.*?)' + '(' + re.escape(line_comment[0]) + ')' + r'(\s?)\s*([\-=*]*)\s*?(\s?)(\w.*?)?([ \-=*]*?)([ ]?)()$', text)
                    if m:
                        break

                # Single-line block comments
                if not m:
                    for block_comment in block_comments:
                        restr = r'^(.*?)' + '(' + re.escape(block_comment[0]) + ')' + r'(\s?)\s*([\-=*]*)\s*?(\s?)(\w.*?)?([ \-=*]*?)([ ]?)' + '(' + re.escape(block_comment[1]) + ')' + r'$'
                        # print(repr(restr))
                        m = re.match(restr, text)
                        if m:
                            break;

                if m:
                    # print(m.groups())
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

                    padsNeeded = line_width - lengthExclPad
                    numToAdd = int(padsNeeded / 2)
                    if numToAdd < 0:
                        numToAdd = 0
                        numToAdd2 = 0
                    else:
                        numToAdd2 = padsNeeded - numToAdd

                    newText = m.group(1) + m.group(2) + m.group(3) + (padChar * numToAdd) + titleSpace + titleText + titleSpace + (padChar * numToAdd2) + trailingSpace + trailingCommentMark

                    # Remove trailing spaces, for the case that the padding char is itself a space
                    newText = re.sub(r'\s+$', '', newText)

                    self.view.replace(edit, line, newText)
