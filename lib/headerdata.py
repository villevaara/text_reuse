import re


def get_headers_from_document_text(document_text):
    header_index_and_text = []
    header_indices = []
    # !!!obs does this work?
    # for match in re.finditer('\n\n#', document_text):
    for match in re.finditer('\n\n# ', document_text):
        header_indices.append(match.start())
    for index in header_indices:
        from_header = document_text[index + 4:]  # 3:]
        newline_position = from_header.find('\n')
        header_text = (from_header[0:newline_position]).strip()
        # leave the \n\n# plus whitespace from the header text
        header_index_and_text.append([index, header_text])
    return header_index_and_text


def get_header_for_textindex(start_index, headerdata):

    header_text = "** NO HEADER FOUND **"

    for entry in headerdata:
        if (entry[0] - start_index) < 0:
            header_text = entry[1]
        else:
            break

    return header_text


def get_header_and_index_for_textindex(start_index, headerdata):
    header_text = "** NO HEADER FOUND **"
    header_index = -1
    for entry in headerdata:
        if (entry[0] - start_index) < 0:
            header_index = entry[0]
            header_text = entry[1]
        else:
            break
    return {'text': header_text, 'index': header_index}
