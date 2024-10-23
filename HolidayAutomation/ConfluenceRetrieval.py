'''
This code is to retrieve all documentation added onto Confluence in the form of Tables / nested tables
An excel of all available configuration is the main input.
For each row in the excel where there is an entry in DocumentationLink and the corresponding ID, a new column that is created will store the corresponding
Confluence ID obtained from stripping the Documentation Link
Checks are done through the Link as it is not always correct (Confluence has different variations of shortened URL, words or ID)
Run multi-threaded JSON GET requests to Confluence to obtain the Confluence page HTML
Clean up by parsing with BeautifulSoup and breaking down all tables correctly
Remap into new Excel sheets
'''
import json
import pandas as pd
import datetime
from datetime import datetime, timedelta
import glob
import re
import os

#Librarise for decoding base64 shared tinyurl
import base64
import struct

from atlassian import Confluence
import requests
import json

#For running threading to make operations run faster
import concurrent
from concurrent.futures import ThreadPoolExecutor

#BeautifulSoup
from bs4 import BeautifulSoup
import lxml

#markdown table
from py_markdown_table.markdown_table import markdown_table

############
# Details  #
############

mainDirectory = 'FILEDIRECTORY'

#Declare global variables
benefitTemplate_list = []

#Credentials
conf_auth = {
    "Username": "Username", #Confluence account ID
    "Token": "APIToken" #Confluence Personal token --> Please get from ''
}

################
# Method       #
################

###
# Write to excel file
###
def writeDFToExcel(data):
    
    filename = data[4] + '_' + data[3].replace(' ', '_') + '.xlsx'
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        
        sheets_length = len(data[1])

        data[0].to_excel(writer, sheet_name='Summary', index=False)
        for item in range(sheets_length):
            data[2][item].to_excel(writer, sheet_name=data[1][item], index=False)

        #df.to_excel(writer, sheet_name=sheetname, index=False)
        #worksheet = writer.sheets[sheetname]
        print("The excel file " + filename + "has been created.")

###
# Find Latest file
###
def find_latest_file(pattern):
    files = glob.glob(os.path.join(os.getcwd(), pattern))
    if not files:
        return None
    latest_file=max(files, key=os.path.getmtime)
    return latest_file

###
# Method to retrieve confluence ID from a shared tiny URL through base 64 decoding
###
def get_confluence_page_id_from_tiny_url(tiny_url):
        page_short_id = tiny_url.split("/")[-1:][0]
        page_short_id = (
            page_short_id.replace("/", "\n").replace("-", "/").replace("_", "+")
        )
        padded_id = page_short_id.ljust(11, "A") + "="
        decoded_id = base64.b64decode(padded_id)
        return struct.unpack("Q", decoded_id)[0]

###
# Method to retrieve Page ID from given confluence link by title and space key
###
def confluenceAPIReq(title, spaceKey):
  import urllib3
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  pageURL = "https://space.confluence.com/rest/api/content?title=" + title + "&spaceKey=" + spaceKey
  #print(pageURL)
  confpage_req = requests.get(
      url = pageURL,
      #params = {'title': title, 'spaceKey': spaceKey}, #Can't use params because + sign change to ASCII
      #auth = (conf_auth["Username"], conf_auth["Password"]), #Use token for safety
      headers = {"Authorization" : "Bearer " + conf_auth['Token']},
      verify= False #WE NEED THIS TO STOP SSL ERROR
  )
  page_data = json.loads(confpage_req.text)

  #If the page does not exist, this page cannot be found
  #We catch the exception and return as NaN if that is the case
  try:
    pageId = page_data['results'][0]['id']
  except IndexError:
    pageId = np.nan
    return pageId
  else:
    return pageId

###
# Method to get page ID based on URL string provided
# There are different links being pasted into JIRA
# Variation 1: pageID directly provided -> We just substring the relevant pageId after truncating any other requests
# Variation 2: title and space key is provided -> Need to call API request to get pageId
# Variation 3: tinyurl through Shared function on confluence -> Need to decode to get page ID
# Other variations: These includes other modifiers such as ? or # that needs to be removed properly
###
def getConfId(index, urlString):
  #print(urlString)

  if type(urlString) != str:
    pageId = np.nan
  #PageID is provided directly
  elif 'pageId' in urlString:
    #remove contextnavpage
    if '&' in urlString:
      urlString = urlString.split("&")[0]
    pageId = str(urlString.split("=")[-1])
    pageId = ''.join(c for c in pageId if c.isdigit())
  #title and space key is provided
  elif 'title' in urlString or 'spaceKey' in urlString:
    spaceKey = urlString.split('=')[1].split('&')[0]
    title = urlString.split("=")[-1]
    #print(title, spaceKey)
    pageId = confluenceAPIReq(title,spaceKey)
  #every other combination
  else:
    #remove all ? modifiers for string
    if '?' in urlString:
      urlString = urlString.split('?')[0]
    spaceKey = urlString.split('/')[-2]
    title = urlString.split('/')[-1]

    if '#' in title:
      title = title.split('#')[0]

    #print(spaceKey, title)

    #using shared tinyurl
    if spaceKey == 'x':
      pageId = get_confluence_page_id_from_tiny_url(title)
      pageId = str(pageId)
    else:
      pageId = confluenceAPIReq(title,spaceKey)

  if(pd.isnull(pageId)):
    print("Incorrect urlString at: " + str(index))
  return pageId

###
# Extract readable text
###
def stringify_list(inner_child):
    list_items = [] #For each li element, we make into a hyphenated string
    for li in inner_child.find_all('li'):
        list_items.append(f"- {li.get_text(strip=True)}")
    return "\n".join(list_items)

def stringify_table(inner_child):
    th_rows = []
    tr_rows = []
    th_rows = [inner_th.get_text(strip=True) for inner_th in inner_child.find_all('th')]

    for idx, inner_tr in enumerate(inner_child.find_all('tr')):
        if idx == 0:
            continue
        else:
            tr_items = {}
            for id, inner_td in enumerate(inner_tr.find_all('td')):
                tr_items[th_rows[id]] = inner_td.get_text(strip=True)
            
            tr_rows.append(tr_items)
    
    markdown_t = markdown_table(tr_rows).get_markdown()

    return markdown_t

###
# Extract from table
###
def table_extract(element):
  tr_mainRows = element.find('tbody').find_all('tr', recursive=False)

  header_row = []
  rows = []
  for main_tr in tr_mainRows:
      #print("ele", element)
      parts = []
      if len(main_tr.find_all()) == 0:
          parts.append(main_tr.get_text(strip=True))
      else:
          for child in main_tr.find_all(recursive=False): #each Child is <td> element
              #print("child: ", child)
              if len(child.find_all()) == 0:
                  parts.append(child.get_text(strip=True))
              else:
                  column_parts = []
                  for inner_child in child.find_all(recursive=False): #each inner_child is an element in <td>
                      #print("inner_child: ", inner_child)
                      if inner_child.has_attr("class") and 'content-wrapper' in inner_child.get("class"):
                        for in_c in inner_child.find_all(recursive=False): #because this is a content wrapper, we need to dive deep again
                            if in_c.find_all('li'):
                                column_parts.append(stringify_list(in_c))
                            elif in_c.find_all('tbody'):
                                column_parts.append(stringify_table(in_c))
                            else:
                                column_parts.append(in_c.get_text(strip=True))
                      elif inner_child.find_all('li'): #The element is a <ul> or <li>
                        column_parts.append(stringify_list(inner_child))
                      elif inner_child.find_all('tbody'): #The element is a <table>
                        column_parts.append(stringify_table(inner_child))
                      else:
                          column_parts.append(inner_child.get_text(strip=True))

                  parts.append('\n'.join(column_parts) if len(column_parts) > 1 else column_parts[0])
          
      #print("td: ", parts)
      if len(header_row) == 0:
          header_row = parts
      else:
          rows.append(parts)

  if len(rows) == 0:
     single_df = pd.DataFrame(columns = header_row, data=[[''] * len(header_row)])
  else:
     single_df = pd.DataFrame(columns=header_row, data=rows)

  return single_df

###
#Get content from Confluence
###
def getContentFromConfluence(idx, pageId):
    confpage_summaryReq = requests.get(
      url = "https://space.tobdarwin.com/rest/api/content/"+ pageId,
      headers = {"Authorization" : "Bearer " + conf_auth['Token']},
      verify=False #WE NEED THIS TO STOP SSL Error
    )
    conf_summary_json = json.loads(confpage_summaryReq.text)
    page_title = conf_summary_json['title']
    page_id = conf_summary_json['id']
    page_creator = conf_summary_json['history']['createdBy']['displayName']
    page_createdDate = conf_summary_json['history']['createdDate']
    page_currentVersion = conf_summary_json['version']['number']
    page_lastModifier = conf_summary_json['version']['by']['displayName']
    page_lastModified = conf_summary_json['version']['when']

    confpage_req = requests.get(
      url = "https://space.tobdarwin.com/rest/api/content/"+ pageId + "?expand=body.storage",
      headers = {"Authorization" : "Bearer " + conf_auth['Token']},
      verify=False #WE NEED THIS TO STOP SSL Error
    )

    if confpage_req.status_code != 200:
      print(confpage_req.text)

    try:
        page_data = json.loads(confpage_req.text)
    except:
       print('No page found for row: ' + str(idx))
    else:
       htmlContent = page_data['body']['storage']['value']
       htmlPageTitle = page_data['title']
    
    #parse the HTML content with BeautifulSoup to remove HTML tags. Parser is lxml
    soup = BeautifulSoup(htmlContent, "lxml")
    
    #Find all rows
    first_table = soup.find('table')
    rows = first_table.find_all('tr')

    #For the page information
    page_summary = {}
    th_string = []
    td_string = []
    for row in rows:
       #Extract <th> and <td> elements
       th = row.find('th')
       td = row.find('td')

       #Extract text content, handle missing or empty elements
       th_text = th.get_text(strip=True) if th else None
       td_text = td.get_text(strip=True) if td else None

       #Store the pair in the dictionary
       #page_summary[th_text] = td_text
       th_string.append(th_text)
       td_string.append(td_text)

    page_summary = {
       "Header": th_string,
       "Description": td_string 
    }
    
    summary_df = pd.DataFrame(page_summary)
    additional_info = {"Header": ["Page Title", "Page ID", "Created By", "Created Date", "Current Version", "Last Modified By", "Last Modified Date"],
                        "Description": [page_title, page_id, page_creator, page_createdDate, int(page_currentVersion), page_lastModifier, page_lastModified]}
    summary_df = pd.concat([summary_df, pd.DataFrame(additional_info)], ignore_index=True)

    #For the different section
    expands = soup.find_all('ac:structured-macro', {"ac:name":"ui-expand"})

    tables = []
    item_count = {}
    updated_sheetName_list = []
    count = 0
    for expand in expands:

      #These finds the different expanded section
      title_header = expand.find('ac:parameter', {"ac:name":"title"})
      title_text = title_header.get_text(strip=True) if title_header else None

      #For the specific section that has nested ui-expand
      print(title_text)
      if 'SomeText' in title_text:
        nested_expand = expand.find_all('ac:structured-macro', {'ac:name': 'ui-expand'})

        if len(nested_expand) > 0:
          for sub_expand in nested_expand:
            subtitle_header = sub_expand.find('ac:parameter', {"ac:name":"title"})
            subtitle_text = subtitle_header.get_text(strip=True) if subtitle_header else None

            sub_df = table_extract(sub_expand)
            sub_df['Section'] = title_text + " " + subtitle_text

            tables.append(sub_df)
        else:
          single_df = table_extract(expand)
          single_df['Section'] = title_text

          tables.append(single_df)
      else:
        if expand.find_parents('ac:structured-macro', {"ac:name": "ui-expand"}):
          continue
        
        if expand.find_all('table'):
          single_df = table_extract(expand)
          single_df['Section'] = title_text
        else:
          single_df = pd.DataFrame({'Section': [title_text]})

        tables.append(single_df)
      
      # if count == 0:
      #    break
    
    #Get the sheet names
    #For each Section which is stored as a column, take only one instance through unique, and remove all additional text in parantheses
    #Then, since excel sheet name can only be 31 characters long, truncate to 31 characters
    sheetName_list = [eachPage['Section'].unique()[0].split('(')[0].strip() for eachPage in tables]

    for item in sheetName_list:
      item = re.sub(r'[\[\]:*?\\/]', ' ', item)
      if item in item_count:
        item_count[item] += 1
        updated_item = f"{item[:28]} {item_count[item]}"[:31] #Truncate to 28 characters to allow for suffix
      else:
         item_count[item] = 1
         updated_item = item[:31] #Truncate to 31 characters
      updated_sheetName_list.append(updated_item)

    writeDFToExcel([summary_df, updated_sheetName_list, tables, htmlPageTitle, pageId])
    return print("The page " + pageId + "has been processed.")

################
# Run the code #
################

latest_FullFile = find_latest_file('List_*.xlsx')
List_df = pd.read_excel(latest_FullFile, header=0)

exclude_list = List_df[~(List_df['Column'].str.contains('https://space.confluence.com/', na=False))][['ID', 'DocumentationLink']]
possible_df = List_df[~List_df.index.isin(exclude_list.index)].reset_index(drop=True)
