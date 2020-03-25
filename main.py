import re
from bs4 import BeautifulSoup
import requests, time, csv, string


sticker_set = set()
SAFE_MODE = True
MAX_ITERATIONS = 10

def main():
    global sticker_set
    with open('Stickers.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for a in csv_reader:
            for b in a:
                sticker_set.add(b)

    hit_list = []
    website = "https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20M4A4%20%7C%20Faded%20Zebra%20%28Field-Tested%29"
    page_start_index = 0
    additive_string = "?query=&start="+str(page_start_index)+"&count=100"
    page = requests.get(website + additive_string)
    soup = BeautifulSoup(page.content, "html.parser")
    total_amount = int(soup.find('span', id="searchResults_total").contents[0].translate(str.maketrans('', '', string.punctuation)))
    print(total_amount)
    total_iterations = (total_amount // 100) + 1
    total_iterations = min(total_iterations,MAX_ITERATIONS)
    #total_iterations = 1
    for i in range(total_iterations):
        print("PAGE: "+str(i+1))
        print("\n")
        page_start_index = 100 * i
        additive_string = "?query=&start="+str(page_start_index)+"&count=100"
        page = requests.get(website + additive_string)
        soup = BeautifulSoup(page.content, "html.parser")
        the_search2(soup,page_start_index, website)



def the_search2(soup, page_start_index, website):



    search_results = soup.findAll('script', type="text/javascript")#{"type" : "text/javascript"})
    the_string = str(search_results[-1])
    #print(the_string)
    the_list = str.split(the_string,"\"market_name\":\"")
    the_list = the_list[1:] #get rid of useless stuff in front
    print(len(the_list))
    final_list = []
    

    for i in the_list:
        index = i.find("<br>Sticker:")
        if index == -1:
            final_list.append("")
        else:
            final_list.append(i[(13+index):])


    final_list2 = []

    for i in final_list:
        index = i.find("<\/center><\/div>")
        if index == -1:
            final_list2.append("")
        else:
            final_list2.append(i[:index])

    print("final list2 " +str(len(final_list2)))

    counter = 0
    for i in final_list2:
        split_str = str.split(i,",")
        flag = False
        for j in split_str:
            if j in sticker_set:
                flag = True
        if flag:
            print(i)
            if not SAFE_MODE:
                print(website+"?query=&start="+str(page_start_index+counter)+"&count=1")
            else:
                print(website+"?query=&start="+str(page_start_index+counter-6)+"&count=13")
        counter+=1

def the_search(soup):


    search_results = soup.findAll('script', type="text/javascript")#{"type" : "text/javascript"})
    the_string = str(search_results[-1])
    #print(the_string)
    the_list = str.split(the_string,"<br>Sticker:")

    for i in the_list:
        print (i)

    return
    #print(len(the_list))
    #for i in the_list:
    #    print(i)
    #    print("\n\n\n\n\n")

    the_list = the_list[1:] #get rid of stuff before in the script

    final_list = []

    for i in the_list:
        index = i.find("<\/center><\/div>")
        if i == -1:
            continue
        final_list.append(i[:index])

    actual_final_list = []
    for i in final_list:
        actual_final_list.extend(str.split(i,","))

    flag = False
    for i in actual_final_list:
        if i in sticker_set:
            print(i)
            flag = True


    return flag
    #for i in final_list:
    #    print(i)
    #guns = soup.findAll("div", {})
    #print(search_results.prettify())

    #guns = soup.findAll("div", {"class" : re.compile("market_listing_row_ market_recent_listing_row listing_*")})
    #print(type(guns))
    #for gun in guns:
    #    print(gun)
    #print(soup.prettify())
    # print([type(item) for item in list(soup.children)])

if __name__ == "__main__":
    main()