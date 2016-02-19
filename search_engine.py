import time

start_time=0

def get_page(url):
    try:
        import urllib2

        request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "http://thewebsite.com",
                "Connection": "keep-alive" 
        }

        request = urllib2.Request(url, headers=request_headers)
        return urllib2.urlopen(request).read()
    except:
        return "error"

def get_all_links(text,links,crawled):
    end=0
    new_links=[]
    while(1):
        start=text.find("a href",end)
        if(start==-1):
            return new_links    #returns list of links on the current page 
        start=text.find('"',start)
        end=text.find('"',start+1)
        link=text[start+1:end]
        
        if link not in crawled: #to ensure that a link is not crawled again
            links.append(link)  #also helps to avoid condition of memory overflow + reduces traversal in the main function
        new_links.append(link)

def add_to_index(index,text,url):
    words=text.split()
    for word in words:
        if word not in index:
            index[word]=[]
        if url not in index[word]:
            index[word].append(url)
    return index

def calculate_ranks(graph):
    d=.8    #damping factor
    loops=10
    rank={}
    dp={}
    total_url=len(graph)

    for url in graph:
        if url not in dp:
            dp[url]=[0 for x in range(0,loops)]
        dp[url][0]=1.0/total_url

    for t in range(1,loops):
        for url in graph:
            dp[url][t]=(1-d)/total_url  #constant value in expression
            sum=0.0               #calculating the summation part
            for i in graph:
                if url in graph[i] and len(graph[i]):
                    sum+=dp[i][t-1]/len(graph[i])
            sum*=d
            dp[url][t]+=sum     #total rank of page at t'th loop

    for url in graph:
        rank[url]=dp[url][loops-1]
    return rank

def partition(s,ranks,lb,ub):
    i=lb+1
    j=lb+1
    while(j<=ub):
        if(ranks[s[j]]>=ranks[s[lb]]):  #decreasing order
            s[j],s[i]=s[i],s[j]
            i+=1
        j+=1
    s[lb],s[i-1]=s[i-1],s[lb]
    return i-1

def quicksort(s,ranks,lb,ub):
    if(lb<ub):
        pivot=partition(s,ranks,lb,ub)
        quicksort(s,ranks,lb,pivot-1)
        quicksort(s,ranks,pivot+1,ub)

def url_ordering(ranks,index):
    for word in index:
        quicksort(index[word],ranks,0,len(index[word])-1)

def display_time(time_taken):
    hr=int(time_taken)/3600
    min=int(time_taken)/60
    sec=int(time_taken)%60
    print "Total time elapsed : ",
    if(hr):
        print hr,"hrs",
    if(min):
        print min,"minutes",
    if(sec):
        print sec,"seconds"
        
def crawl_web(page_url):
    global start_time

    links=[page_url]
    level=1
    links.append(level)
    crawled=[]
    index={}    #dict storing ( keyword->list of urls associated )
    graph={}    #dict storing ( url-> list of urls on that page )
    while(len(links)):
        url=links[0]
        links=links[1:]
        if(type(url)==int):
            #print level,start_time
            if(url>2 and int(time.time()-start_time)>14*60):    #adjust the depth of graph (web) crawled - bfs depth
                break
            level+=1
            links.append(level)
            continue
        crawled.append(url)
        flag=5
        while(flag):
            text=get_page(url)      #html source code of the page
            if text!="error":       #check if page was sucessfully extracted/loaded
                break               #else try (max 5 times) till its not loaded properly
            flag-=1
        if not flag:                #if page doesnt load , contains error
            continue                #den ignore it
        add_to_index(index,text,url)
        new_links=get_all_links(text,links,crawled)
        #print time.time()-start_time, time.asctime( time.localtime(time.time()) )
        graph[url]=new_links    #add new_links to the graph

    ranks=calculate_ranks(graph)
    print "Compiling the results, wait for few moments...\n"
    url_ordering(ranks,index)   #sorts the urls of each keyword

    return index,ranks

def input_seedpage():
    while(1):
        url=raw_input("Enter the complete url of seed page to crawl the web : ")
        if get_page(url)!="error" :
            return url
        print "\nCouldn't connect to web, please check the url entered or try again later\n"

def lookup():
    global start_time

    seed_url=input_seedpage()
    start_time=time.time()
    print "\nIt will take some time to fetch results, Please sit back and relax..."
    index_sorted,ranks=crawl_web(seed_url)

    print "Web Crawled and results processed Successfully !!"
    display_time(time.time()-start_time)
    
    while(1):
        word=raw_input("\nEnter the word to be searched : (-1 to exit) ")
        if word=='-1' :
            exit()
        if word not in index_sorted:
            print "Sorry, no related results were found."
            continue
        print "\nSome of the top results are as follows (with their ranks) : \n"
        count=10
        for i in index_sorted[word]:
            print i,"  -->  ",ranks[i],"\n"
            count-=1
            if not count :
                break

lookup()
