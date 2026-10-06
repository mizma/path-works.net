import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class JapaneseLinebreakPreprocessor(Preprocessor):
    # Fenced code blocks.
    FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")

    # Markdown block elements that must not be joined with surrounding prose.
    HEADING_RE = re.compile(r"^\s{0,3}#{1,6}(?:\s|$)")
    HR_RE = re.compile(r"^\s{0,3}((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})$")

    # Markdown table separator row.
    #
    # Examples:
    #   | --- | --- |
    #   | :--- | ---: |
    #   | :---: | --- |
    TABLE_SEPARATOR_RE = re.compile(
        r"^\s*\|?\s*:?-{1,}:?\s*"
        r"(?:\|\s*:?-{1,}:?\s*)+"
        r"\|?\s*$"
    )

    # Blockquote prefix, e.g. "> " or ">> ".
    BLOCKQUOTE_RE = re.compile(r"^(\s*(?:>\s*)+)")

    # List item prefix.
    UL_RE = re.compile(r"^(\s*)([-+*])(\s+)(.*)$")
    OL_RE = re.compile(r"^(\s*)(\d+[.)])(\s+)(.*)$")

    def run(self, lines):
        result = []
        paragraph = []

        in_metadata = True
        fence_char = None
        fence_length = 0

        def flush_paragraph():
            if paragraph:
                result.append("".join(paragraph))
                paragraph.clear()

        def is_blank(line):
            return not line.strip()

        def is_heading(line):
            return bool(self.HEADING_RE.match(line))

        def is_horizontal_rule(line):
            return bool(self.HR_RE.match(line))

        def get_blockquote_prefix(line):
            match = self.BLOCKQUOTE_RE.match(line)
            return match.group(1) if match else None

        def get_list_item(line):
            match = self.UL_RE.match(line)
            if match:
                return (
                    match.group(1),
                    match.group(2),
                    match.group(3),
                    match.group(4),
                )

            match = self.OL_RE.match(line)
            if match:
                return (
                    match.group(1),
                    match.group(2),
                    match.group(3),
                    match.group(4),
                )

            return None

        def is_table_separator(line):
            return bool(self.TABLE_SEPARATOR_RE.match(line))

        def is_table_row(line):
            """
            Return True if the line looks like a Markdown table row.

            A table row needs at least one unescaped pipe.
            """
            stripped = line.strip()

            if not stripped:
                return False

            # Count unescaped pipes.
            pipe_count = 0
            escaped = False

            for char in stripped:
                if escaped:
                    escaped = False
                    continue

                if char == "\\":
                    escaped = True
                    continue

                if char == "|":
                    pipe_count += 1

            return pipe_count >= 1

        def is_table_start(index):
            """
            A Markdown table starts with a row followed immediately
            by a separator row.

                | Header | Header |
                | ------ | ------ |

            This prevents ordinary prose containing "|" from
            accidentally being treated as a table.
            """
            if index + 1 >= len(lines):
                return False

            return (
                is_table_row(lines[index])
                and is_table_separator(lines[index + 1])
            )

        i = 0

        while i < len(lines):
            line = lines[i]

            # ---------------------------------------------------------
            # Pelican metadata
            # ---------------------------------------------------------
            #
            # Everything before the first blank line is metadata.
            #
            if in_metadata:
                result.append(line)

                if is_blank(line):
                    in_metadata = False

                i += 1
                continue

            # ---------------------------------------------------------
            # Fenced code blocks
            # ---------------------------------------------------------
            #
            # Leave everything inside them completely untouched.
            #
            if fence_char is not None:
                result.append(line)

                match = self.FENCE_RE.match(line)

                if match:
                    fence = match.group(2)

                    if (
                        fence[0] == fence_char
                        and len(fence) >= fence_length
                    ):
                        fence_char = None
                        fence_length = 0

                i += 1
                continue

            # Opening fence.
            match = self.FENCE_RE.match(line)

            if match:
                flush_paragraph()

                fence = match.group(2)
                fence_char = fence[0]
                fence_length = len(fence)

                result.append(line)

                i += 1
                continue

            # ---------------------------------------------------------
            # Markdown tables
            # ---------------------------------------------------------
            #
            # Tables must be passed through untouched. Otherwise their
            # individual rows would be concatenated into one paragraph.
            #
            #   | Project | 概要 |
            #   | ------- | ---- |
            #   | foo     | bar  |
            #
            # remains exactly as written.
            #
            if is_table_start(i):
                flush_paragraph()

                # Copy the table header + separator + subsequent rows.
                while i < len(lines):
                    table_line = lines[i]

                    if is_blank(table_line):
                        break

                    if not is_table_row(table_line):
                        break

                    result.append(table_line)
                    i += 1

                continue

            # ---------------------------------------------------------
            # Blank line
            # ---------------------------------------------------------
            if is_blank(line):
                flush_paragraph()
                result.append(line)

                i += 1
                continue

            # ---------------------------------------------------------
            # Headings
            # ---------------------------------------------------------
            if is_heading(line):
                flush_paragraph()
                result.append(line)

                i += 1
                continue

            # ---------------------------------------------------------
            # Horizontal rules
            # ---------------------------------------------------------
            if is_horizontal_rule(line):
                flush_paragraph()
                result.append(line)

                i += 1
                continue

            # ---------------------------------------------------------
            # Blockquotes
            # ---------------------------------------------------------
            #
            # Join consecutive blockquote lines while preserving the
            # blockquote prefix.
            #
            #   > これは引用を
            #   > 改行して書いています。
            #
            # becomes:
            #
            #   > これは引用を改行して書いています。
            #
            quote_prefix = get_blockquote_prefix(line)

            if quote_prefix is not None:
                flush_paragraph()

                quote_lines = []
                quote_prefixes = []

                while i < len(lines):
                    quote_line = lines[i]

                    prefix = get_blockquote_prefix(quote_line)

                    if prefix is None:
                        break

                    content = quote_line[len(prefix):]

                    quote_prefixes.append(prefix)
                    quote_lines.append(content)

                    i += 1

                # Use the first line's prefix. This preserves normal
                # single-level and nested blockquotes in the common case.
                prefix = quote_prefixes[0]

                result.append(prefix + "".join(quote_lines))

                continue

            # ---------------------------------------------------------
            # Lists
            # ---------------------------------------------------------
            #
            # For simple consecutive list items, preserve each item's
            # marker but join continuation lines belonging to that item.
            #
            #   - これはリスト項目です。
            #     続きです。
            #
            # remains structurally intact.
            #
            list_item = get_list_item(line)

            if list_item is not None:
                flush_paragraph()

                indent, marker, spacing, content = list_item

                result.append(
                    indent + marker + spacing + content
                )

                i += 1
                continue

            # ---------------------------------------------------------
            # Ordinary prose
            # ---------------------------------------------------------
            #
            # Join source lines without inserting whitespace.
            #
            paragraph.append(line)

            i += 1

        flush_paragraph()

        return result


class JapaneseLinebreakExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(
            JapaneseLinebreakPreprocessor(md),
            "japanese_linebreaks",
            35,
        )


def makeExtension(**kwargs):
    return JapaneseLinebreakExtension(**kwargs)
