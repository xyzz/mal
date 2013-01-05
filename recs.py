import urllib.request
import re
import http.client

def get_page(url):
    try:
        return urllib.request.urlopen(url).read().decode("utf-8")
    except http.client.IncompleteRead:
        return get_page(url)

edges = {}
weight = {}
name = {}
score = {}
def load():
    """ Loads edges & vertices """
    fin = open("edges", "r")
    for line in fin:
        u, v, w = [int(x) for x in line.split()]
        if u not in edges:
            edges[u] = []
            weight[u] = []
        edges[u].append(v)
        weight[u].append(w)
    fin.close()

    fin = open("vertices", "r")
    while True:
        s = fin.readline()
        if s == "":
            break
        aname = fin.readline().strip()
        s = s.split()
        aid = int(s[0])
        ascore = float(s[1])
        name[aid] = aname
        score[aid] = ascore
    fin.close()

def recommend(series):
    watched = {}
    for x in series:
        watched[x] = True
    val = {}
    for x in series:
        if x not in edges:
            continue
        for i in range(len(edges[x])):
            if edges[x][i] in watched:
                continue
            if edges[x][i] not in val:
                val[edges[x][i]] = 0
            # lol, wtf
            val[edges[x][i]] += score[edges[x][i]] * weight[x][i]
    sorted_val = sorted(val.items(), key=lambda x: x[1], reverse=True)
    print("Recommended for you")
    print("-" * 40)
    for x in range(min(50, len(sorted_val))):
        if sorted_val[x][1] > 0:
            print("%d. %s [%.3f]" % (x + 1, name[sorted_val[x][0]], sorted_val[x][1]))
            print("-" * 40)

if __name__ == "__main__":
    login = input("Your MAL login: ")
    page = get_page("http://myanimelist.net/animelist/%s&status=2&order=0" % login)
    series_raw = re.findall("anime\/(\d+)\/", page)
    series = [int(x) for x in series_raw]
    load()
    recommend(series)
