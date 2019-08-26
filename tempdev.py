pagefile_simple = ("/home/vvaara/projects/comhis/data-own-common/ecco-xml-img/0145000201/pagetexts/0145000201_page124.txt")
pagefile_complex = ("/home/vvaara/projects/comhis/data-own-common/ecco-xml-img/0145000201/pagetexts/0145000201_page155.txt")
pagefile_noheader = ("/home/vvaara/projects/comhis/data-own-common/ecco-xml-img/0145000201/pagetexts/0145000201_page156.txt")

testpage = pagefile_noheader

with open(testpage, 'r') as pagefile:
    pagetext_list = list(pagefile)
    header_length = 0
    # if first char of first line is # start counting header length
    if pagetext_list[0][0] == "#":
        for line in pagetext_list:
            if line[0] == "#" or line[0] == "\n":
                header_length += len(line)
            else:
                break
    print(header_length)

