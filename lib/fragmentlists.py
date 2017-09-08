from lib.tr_fragment import TextReuseFragment


def get_fragmentlist(cluster_data, document_text_data,
                     docid_indexmap_ascii,
                     docid_indexmap_unicode):
    print("> Getting fragment list ...")
    cluster_data_length = len(cluster_data) - 1
    fragment_list = []
    i = 0
    print("items in list: " + str(cluster_data_length))
    for item in cluster_data:
        if i % 20 == 0:
            print("Processing item: " + str(i) +
                  " / " + str(cluster_data_length))
            print("documentID: " + item.get('documentID'))
            print("clusterID:  " + str(item.get('clusterID')))
        i = i + 1
        fragment = TextReuseFragment(ecco_id=item.get('documentID'),
                                     cluster_id=item.get('clusterID'),
                                     text=item.get('text'),
                                     start_index=None,
                                     end_index=None)
        fragment.set_fragment_encoding(document_text_data=document_text_data)
        if fragment.encoding == "ascii":
            fragment.set_octavo_indices(docid_indexmap_ascii)
        else:
            fragment.set_octavo_indices(docid_indexmap_unicode)
        fragment_list.append(fragment)
    print("  >> Done!")
    return fragment_list


def get_doctext_indexmap(orig_text, method_ascii):
    whitespace_chars = [' ', '\t', '\n', '\r', '\x0b', '\x0c']
    orig_text_length = len(orig_text)
    # results to return. array (list) of fragmenttext_index,chars_lost
    fragment_indices = []
    chars_lost_list = []
    # cumlative index of characters lost
    chars_lost = 0
    # set flags
    # start with prev_char_hit -flag set to account for leading zeros
    prev_char_wshit = True
    this_char_wshit = False
    save_pending = False
    # iterate every char in text.
    # add entry to index if previous char was lost, and current isn't
    for char_index in range(0, orig_text_length):
        if method_ascii and ord(orig_text[char_index]) > 127:
            # getting non-ascii: if ord(char) is > 127
            # this_char_hit = True
            chars_lost += 1
            save_pending = True
            continue
        if orig_text[char_index] in whitespace_chars:
            this_char_wshit = True
        else:
            this_char_wshit = False
        if prev_char_wshit and this_char_wshit:
            chars_lost += 1
            save_pending = True
        prev_char_wshit = this_char_wshit
        if save_pending and not this_char_wshit:
            fragment_index = char_index - chars_lost
            fragment_indices.append(fragment_index)
            chars_lost_list.append(chars_lost)
            # results.append([fragment_index, chars_lost])
            save_pending = False
    if method_ascii:
        method_description = "ascii"
    else:
        method_description = "unicode"
    results = {'method': method_description,
               'fragment_index': fragment_indices,
               'chars_lost': chars_lost_list}
    return results
