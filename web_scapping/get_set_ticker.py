import requests
import lxml.html as lh
import pandas as pd

def get_set_ticker(sector="SET100"):
    """ Get Thailand's stock qoute from www.set.or.th

    Args : 
        - sector : valid sector --> "SET50","SET100","sSET","SETCLMV","SETHD","SETTHSI","SETWB"

    Return :
        - df : stock qoute dataframe

    """
    
    url = f'https://marketdata.set.or.th/mkt/sectorquotation.do?sector={sector}&language=en&country=US'
    
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    
    #Parse data that are stored between <tr>..</tr> of HTML
    th_tr_elements = doc.xpath('//*[@id="maincontent"]/div/div[2]/div/div/div/div[3]/table/thead/tr')
    tb_tr_elements = doc.xpath('//*[@id="maincontent"]/div/div[2]/div/div/div/div[3]/table/tbody/tr')
    
    #Create empty list
    col=[]
    i=0
    
    #For each row, store each first element (header) and an empty list
    for t in th_tr_elements[0]:
        i+=1
        name=t.text_content()
        # print('%d:"%s"'%(i,name))
        col.append((name,[]))

    # print(col)

    #Since out first row is the header, data is stored on the second row onwards
    for j in range(0,len(tb_tr_elements)):
        #T is our j'th row
        T=tb_tr_elements[j]

        #i is the index of our column
        i=0

        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1

    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    df.drop(columns="Sign", inplace=True)
    df["Symbol"] = df["Symbol"].str.replace('\r\n', '').str.replace('^ +| +$', '')
    # print(df)
    return df.Symbol

get_set_ticker("SET100")