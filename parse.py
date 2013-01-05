import urllib.request
import re
import sys
import http.client

def get_page(url):
    try:
        return urllib.request.urlopen(url).read().decode("utf-8")
    except http.client.IncompleteRead:
        return get_page(url)

def parse_page(aid, fout_v, fout_e):
    url = "http://myanimelist.net/anime/%d/a/userrecs" % aid
    page = get_page(url)

    if page.find("<h1>Invalid Request</h1>") != -1:
        return

    name = re.search("<\/div>(.*?)<\/h1>", page).group(1)
    score = re.search("<\/span> (.*?)<sup><small>1<\/small>", page).group(1)

    fout_v.write("%d %s\n%s\n" % (aid, score, name))

    rec_regexp = re.compile("""<div class="borderClass">(.*?)<\/table>""", re.DOTALL)
    recommendations = rec_regexp.findall(page)
    for x in recommendations:
        rid = re.search("anime\/(\d+)\/", x).group(1)
        rcnt = re.search("<strong>(\d+)<\/strong>", x)
        if rcnt == None:
            rcnt = 0
        else:
            rcnt = int(rcnt.group(1))
        rcnt += 1

        fout_e.write("%d %s %d\n" % (aid, rid, rcnt))
    #print(recommendations[0])
    #print(len(recommendations))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: parse start end")
    else:
        start = int(sys.argv[1])
        end = int(sys.argv[2])

        fout_v = open("vertices.%.5d" % start, "w")
        fout_e = open("edges.%.5d" % start, "w")

        for x in range(start, end + 1):
            if x % 10 == 0:
                print("processed %d out of %d" % (x - start, end - start + 1))
            parse_page(x, fout_v, fout_e)

        fout_v.close()
        fout_e.close()
