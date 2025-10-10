import pandas as pd
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from datetime import datetime
import os
from PyPDF2 import PdfReader
import re
from rapidfuzz import fuzz, process



def random_number():
    '''
    >  Function generates a random number |
    >  Mainly used for time.sleeps to imitate human behavior |
    '''
    x = random.uniform(10, 15)
    return x



def define_options():
    '''
    >  Function defines options for webdriver |
    >  Options are used for general crawlings, mainly text |
    >  Language configuration does not seem to work |
    '''
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=de-DE")
    return options



def initiate_webdriver():
    '''
    >  Function initiates webdriver instance | 
    >  Driver is used for most crawlings, mainly for text data | 
    >  Includes normal options |
    '''
    _options = define_options()
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=_options)
    return driver



def define_options_pdf():
    '''
    >  Function defines options for webdriver for Download PDF driver |
    >  Options are configured to automatically download the pdf file when a new 
       tab with a pdf viewer is opened | 
    >  Function defines a specific directory where pdfs are stored
    '''
    options = uc.ChromeOptions()
    timestamp = datetime.now()
    download_dir = os.path.join(os.getcwd(), f'PDF Downloads {timestamp}')
    os.makedirs(download_dir, exist_ok=True)
    prefs = {
        "download.default_directory": download_dir,  # custom folder
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,  # download PDFs directly
        "download.directory_upgrade": True,          # allow folder change
        }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=de-DE")
    return options



def initiate_webdriver_pdf():
    '''
    >  Function initiates webdriver instance for pdf download driver |
    >  Driver includes options specifically configured for pdf download |
    '''
    _options = define_options_pdf()
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=_options)
    return driver



class Driver_ScienceDirect():
    '''
    >  Driver extracts the titles of the search results using a search query 
        url for ScienceDirect |
    >  Class takes the search query url and the number of pages of the search 
        results as input variables | 
    >  Program creates an .xlsx file with the column 'Title' |
    '''
    
    def __init__(self, search_query_url, pages):
        self.search_query_url = search_query_url 
        self.pages = pages

    
    def crawl_page(self):
        driver = initiate_webdriver() 
        driver.get(self.search_query_url)
        wait = WebDriverWait(driver, 120)
        
        title_list = []
        page_count = 1

        while page_count <= self.pages:
            try:
                print(f"Crawling page {page_count}...")

                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))                
                time.sleep(random_number())
                title_elements = driver.find_elements(By.TAG_NAME, "h2") 

                for title in title_elements:
                    title_text = title.text.strip()
                    print(title_text)
                    title_list.append(title_text)    
                
                page_count += 1
                print(page_count)

                if page_count < self.pages:
                    next_button_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-aa-name='srp-next-page']")))
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button_element)
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-aa-name='srp-next-page']")))
                    next_button_element.click()
                else:
                    pass

                time.sleep(random_number())

            except Exception as e:
                print(f"Error crawling science direct page number {page_count}")
                page_count += 1
                print(e) 

        driver.quit()
        print(title_list)
        df_titles = pd.DataFrame(title_list)
        df_titles.columns = ["Title"]
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
        df_titles.to_excel(f"ALL_TITLES_{timestamp}.xlsx", index=False)



class Driver_GoogleScholar():
    '''
    >  Driver crawls the full citations from Google Scholar |
    >  Class takes the ScienceDirect titles as .xlsx file with the column name 'Title' as 
        input |
    >  Driver creates an .xlsx file with the column name 'Full_citation' |
    '''

    def __init__(self, titles_filename):
        self.titles_filename = titles_filename 


    def crawl_page(self):
        driver = initiate_webdriver()    
        wait = WebDriverWait(driver, 120)
        mydata_titles = pd.read_excel(self.titles_filename)
        print(mydata_titles)

        all_quotes = []

        try:
            for index, row in mydata_titles.iterrows():
                title = row['Title']
                print(title)

                driver.get("https://scholar.google.at/") # Go always back to startpage because it helps with anti-bot system
                
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gs_hdr_tsi")))
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gs_hdr_tsb")))

                search_input = driver.find_element(By.CSS_SELECTOR, "#gs_hdr_tsi")
                time.sleep(random_number())
                search_input.send_keys(title)
                time.sleep(random_number())
                search_button = driver.find_element(By.CSS_SELECTOR, "#gs_hdr_tsb")
                search_button.click()

                time.sleep(random_number())
                wait.until(EC.presence_of_all_elements_located((By.LINK_TEXT, "Цитирај")))
                citation = driver.find_element(By.LINK_TEXT, "Цитирај")
                citation.click()

                time.sleep(random_number())
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/div[4]/div/div[2]/div/div[1]/table/tbody/tr[2]/td/div")))
                apa_citation = driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div[2]/div/div[1]/table/tbody/tr[2]/td/div")
                text = apa_citation.text.strip()
                print(text)
                all_quotes.append(text)
                time.sleep(random_number())

        except Exception as e:
            print(e)    
            driver.quit()


        print(all_quotes)
        df_citations_all = pd.DataFrame(all_quotes)
        df_citations_all.columns = ["Full_citation"]
        print(df_citations_all)
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
        df_citations_all.to_excel(f"ALL_GOOGLE_SCHOLAR_CITATIONS_{timestamp}.xlsx", index=False)



class Dataset_All_Citations_Structured():
    '''
    >  Program uses the raw dataset from Google Scholar and transforms the raw data into 
       a structured dataset |
    >  Class parses the full citation and creates a separate column for each 
       information: full citation, authors, year, title and publisher name |
    >  Class takes the Google Scholar .xlsx file with the 'Full_citation' column as input | 
    >  Program creates an .xlsx file with the structured citations |
    '''

    def __init__(self, df_filename):
        self.filename = df_filename
    

    def prepare_dataframe(self, filename):
        mydata = pd.read_excel(filename)
        mydata.drop_duplicates(subset=['Full_citation'], inplace=True, keep='first')
        mydata.dropna(subset=['Full_citation'], inplace=True)
        return mydata

    
    def extract_authors(self, citation):
        try:
            citation_string = str(citation)
            citation_string = citation_string.split('(')
            authors = citation_string[0]
            print(authors)
        except Exception as e:
            print(f"Author not found due to error: {e}")
            authors = None
        return authors
    

    def extract_year(self, citation):
        try:
            citation_string = str(citation)
            citation_string = citation_string.split('(')
            year_string = citation_string[1]
            year_string = year_string.split(')')
            year = year_string[0]
            print(year)
        except Exception as e:
            print(f"Year not found due to error: {e}")
            year = None 
        return year


    def extract_title(self, citation):
        try:
            citation_string = str(citation)
            citation_string = citation_string.split(').')
            citation_string = citation_string[1]
            citation_string = citation_string.split('. ')
            title = citation_string[0]
            print(title)
        except Exception as e:
            print(f"Title not found due to error: {e}")
            title = None
        return title
    

    def extract_publisher(self, citation):
        try:
            citation_string = str(citation)
            citation_string = citation_string.split(').')
            citation_string = citation_string[1]
            citation_string = citation_string.split('. ')
            citation_string = citation_string[1]
            try:
                publisher_list = citation_string.split(',')
                publisher = publisher_list[0]
            except Exception as e:
                print(f"Publisher not found due to error: {e}")
                publisher = None
            
            print(publisher)
        except Exception as e:
            print(f"Publisher not found due to error: {e}")
            publisher = None 
        return publisher
    

    def generate_dataframe(self):
        filename = self.filename
        print(filename)
        mydata = self.prepare_dataframe(filename)
        mydata['Authors'] = mydata['Full_citation'].apply(self.extract_authors)
        mydata['Year'] = mydata['Full_citation'].apply(self.extract_year)
        mydata['Title'] = mydata['Full_citation'].apply(self.extract_title)
        mydata['Publisher'] = mydata['Full_citation'].apply(self.extract_publisher)
        print(mydata)

        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
        mydata.to_excel(f'ALL_CITATIONS__{timestamp}.xlsx', index=False)    



class Driver_ScienceDirect_Abstract():
    '''
    >  Webdriver extracts the abstracts from ScienceDirect |
    >  Driver searches for h2 tag with the text "Abstract" and takes the 
        next div tag with the text. If the string "Abstract" cannot be found, program 
        skips the title and inserts "NO ABSTRACT" |
    >  Driver takes as input a list of titles as an .xlsx file with column name 
        'Title' | 
    >  Input data should also have a column titled "Excluded" with the variables 
        "Excluded" or "". Driver only extracts abstracts for papers that were 
        not excluded | 
    >  Program generates an .xlsx file with the structured citation and the 
        corresponding abstracts |
    '''

    def __init__(self, filename):
        self.filename = filename


    def crawl_page(self):
        driver = initiate_webdriver()
        wait = WebDriverWait(driver, 120)
        mydata = pd.read_excel(self.filename)
        print(mydata)

        all_abstracts = []

        try:
            for index, row in mydata.iterrows():
                title = row['Title']
                print(title)

                if row['Excluded'] == True:
                    abstract_text = "NO ABSTRACT"
                    print(abstract_text)
                    all_abstracts.append(abstract_text)
                    continue

                driver.get("https://www.sciencedirect.com/search") # Go always back to startpage because it helps with anti-bot system
                
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#qs")))
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/section/div/div[1]/div/div/div/div[2]/div/form/div/div/div[4]/div/div[2]/button")))

                # Insert title of paper in search bar

                search_input = driver.find_element(By.CSS_SELECTOR, "#qs")
                search_input.send_keys(title)
                time.sleep(random_number())

                # Click search button 

                search_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/section/div/div[1]/div/div/div/div[2]/div/form/div/div/div[4]/div/div[2]/button")
                search_button.click()
                time.sleep(random_number())

                # Click on first result of search result 

                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//h2//a")))
                anchors = driver.find_elements(By.XPATH, "//h2//a")

                if anchors:
                    first_anchor = anchors[0]
                    href = first_anchor.get_attribute('href')
                    if href:
                        print(href)
                        driver.get(href)

                # Find abstract and extract abstract text

                time.sleep(random_number())
                try:
                    ## I am search here for the h2 tag that includes the text 'Abstract'. Then I take the next
                    ## div and extract the text
                    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//h2[normalize-space(.)='Abstract']/following-sibling::div[1]")))
                    abstract_element = driver.find_element(By.XPATH, "//h2[normalize-space(.)='Abstract']/following-sibling::div[1]")
                    abstract_text = abstract_element.text.strip()
                    print(abstract_text)
                    
                    all_abstracts.append(abstract_text)
                    time.sleep(random_number())
                except Exception as e:
                    print(f"Error during crawling abstract due to {e}")
                    abstract_text = "NO ABSTRACT"
                    print(abstract_text)
                    all_abstracts.append(abstract_text)
                    time.sleep(random_number())

        except Exception as e:
            print(f"Error during crawling abstract due to: {e}")
            abstract_text = "NO ABSTRACT"
            all_abstracts.append(abstract_text)

        df_all_abstracts = pd.DataFrame(all_abstracts)

        mydata['All_abstracts'] = df_all_abstracts
        
        print(mydata)
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
        df_all_abstracts.to_excel(f"ALL_ABSTRACTS_{timestamp}.xlsx", index=False)
        mydata.to_excel(f'ALL_CITATIONS_with_abstracts_{timestamp}.xlsx', index=False)
        driver.quit()



class Driver_ScienceDirect_PDFs():
    '''
    >  Webdriver downloads the pdfs from ScienceDirect |
    >  Driver searches for view pdf button, opens the pdf and automatically 
        downloads the pdf. To do this the driver has to switch between different tabs, pdf tab 
        should be closed immediately |
    >  Driver takes as input a list of titles as an .xlsx file with column name 
        'Title' | 
    >  Input data should also have a column titled "Excluded" with the variables 
        "Excluded" or "". Crawler only extracts pdfs for papers that were 
        not excluded | 
    >  Program generates an .xlsx file with the pdf urls and a directory with 
        the downloaded pdfs |
    '''

    def __init__(self, filename):
        self.filename = filename


    def crawl_page(self):
        driver = initiate_webdriver_pdf()
        wait = WebDriverWait(driver, 120)
        mydata = pd.read_excel(self.filename)
        print(mydata)

        all_pdf_urls = []

        try:
            for index, row in mydata.iterrows():
                title = row['Title']
                print(title)

                if row['Excluded'] == "Excluded":
                    url_string = "NO PDF"
                    print(url_string)
                    all_pdf_urls.append(url_string)
                    continue

                driver.get("https://www.sciencedirect.com/search") # Go always back to startpage because it helps with anti-bot system
                
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#qs")))
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/section/div/div[1]/div/div/div/div[2]/div/form/div/div/div[4]/div/div[2]/button")))

                # Insert title of paper in search bar

                search_input = driver.find_element(By.CSS_SELECTOR, "#qs")
                search_input.send_keys(title)
                time.sleep(random_number())

                # Click search button 

                search_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/section/div/div[1]/div/div/div/div[2]/div/form/div/div/div[4]/div/div[2]/button")
                search_button.click()
                time.sleep(random_number())

                # Click on first result of search result 

                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//h2//a")))
                anchors = driver.find_elements(By.XPATH, "//h2//a")

                if anchors:
                    first_anchor = anchors[0]
                    href = first_anchor.get_attribute('href')
                    if href:
                        print(href)
                        driver.get(href)

                # Find pdf url and download pdf

                time.sleep(random_number())
                try:
                    ## The options of the webdriver were specifically defined to make this work. 
                    ## Driver clicks on pdf link, opens the pdf, switches the driver to next tab, 
                    ## driver automatically downloads the pdf, closes the tab and switches back to the
                    ## main tab of the driver. Main operation in main tab stops working if I don't switch!
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".link-button")))
                    pdf_link = driver.find_element(By.CSS_SELECTOR, ".link-button")
                    
                    original_window = driver.current_window_handle
                    pdf_link.click()
                    wait.until(EC.number_of_windows_to_be(2))
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(5)
                    driver.close()
                    driver.switch_to.window(original_window)

                    pdf_url = pdf_link.get_attribute("href")
                    print(pdf_url)                    
                    all_pdf_urls.append(pdf_url)
                    time.sleep(random_number())
                except Exception as e:
                    print(f"Error during crawling pdf due to {e}")
                    pdf_url = "NO PDF"
                    print(pdf_url)
                    all_pdf_urls.append(pdf_url)
                    time.sleep(random_number())

        except Exception as e:
            print(f"Error during crawling abstract due to: {e}")
            pdf_url = "NO PDF"
            all_pdf_urls.append(pdf_url)

        df_all_pdf_urls = pd.DataFrame(all_pdf_urls)

        mydata['All_pdf_urls'] = df_all_pdf_urls
        
        print(mydata)
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
        df_all_pdf_urls.to_excel(f"ALL_PDF_URLS_{timestamp}.xlsx", index=False)
        mydata.to_excel(f'ALL_CITATIONS_with_pdf_urls_{timestamp}.xlsx', index=False)
        driver.quit()



class PDF_File_Titles():
    '''
    >  Program extracts the titles from the pdf meta data and then renames the files 
        into extracted title | 
    >  Class takes the PDF directory name as input | 
    '''

    def __init__(self, pdf_directory_name):
        self.pdf_directory_name = pdf_directory_name


    def extract_title_metadata_from_pdf(self, filepath):
        try:
            reader = PdfReader(filepath)
            title = reader.metadata.title
            if title:
                title_stripped = title.strip()
                return title_stripped
        except Exception as e:
            print(e)
            return None
        
    
    def clean_filename(self, name):
        name = re.sub(r'[\\/*?:"<>|]', "", name)
        return name[:150]
        
    
    def rename_file_into_pdf_title(self):
        working_dir = os.getcwd()
        directory_path = os.path.join(working_dir, self.pdf_directory_name)
        file_list = os.listdir(directory_path)
        for filename in file_list:
            if filename.lower().endswith(".pdf"):
                filepath = os.path.join(directory_path, filename)
                title = self.extract_title_metadata_from_pdf(filepath)
                if title:
                    new_name = self.clean_filename(title) + ".pdf"
                    new_path = os.path.join(directory_path, new_name)
                    try:
                        os.rename(filepath, new_path)
                        print(f"Renamed: {filename} → {new_name}")
                    except Exception as e:
                        print(f"Error renaming {filename}: {e}")
                else:
                    print(f"No metadata title found for: {filename}")



class Dataset_Check_For_PDF():
    '''
    >  Program checks whether a PDF file corresponds with titles dataset |
    >  Class takes the name of the PDF directory and the .xlsx file with the titles 
        as input variables. The .xlsx file should have a column titled "Title". The
        pdf directory should include the pdf files with the titles as filenames |
    >  Program creates an .xlsx file with the structured citations, especially titles,
        the best match with a filename and the matching score between 0-100 % |
    '''

    def __init__(self, directory_name, filename):
        self.directory_name = directory_name
        self.filename = filename


    def get_best_match_and_score(self, title, choices):
        title_lower = str(title).lower()
        choices_lower = [c.lower() for c in choices]
        match = process.extractOne(title_lower, choices_lower, scorer=fuzz.token_sort_ratio)
        if match:
            return match[0], match[1]
        return None, 0

    
    def check_dataset(self):
        mydata = pd.read_excel(self.filename)
        print(mydata)

        working_dir = os.getcwd()
        directory_path = os.path.join(working_dir, self.directory_name)
        file_list = os.listdir(directory_path)

        df_file_list = pd.DataFrame(file_list)
        df_file_list.columns = ["PDF_filenames"]
        print(df_file_list)

        mydata[["Best_match", "Similarity_to_filelist"]] = mydata["Title"].apply(
            lambda x: pd.Series(self.get_best_match_and_score(x, df_file_list["PDF_filenames"]))
        )

        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
        mydata.to_excel(f"ALL_CITATIONS_with_pdf_check_{timestamp}.xlsx", index=False)



def join_excel_tables():
    '''
    ->  Function merges the different datasets |
    '''
    df_full_citations_w_abstracts = pd.read_excel('ALL_CITATIONS_with_abstracts_08-10-2025_12-51-08.xlsx')
    df_full_citations_w_pdf_urls = pd.read_excel('ALL_CITATIONS_with_pdf_urls_08-10-2025_18-14-29.xlsx')
    df_full_citations_w_abstracts['PDF_urls'] = df_full_citations_w_pdf_urls['All_pdf_urls']
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")
    df_full_citations_w_abstracts.to_excel(f"FINAL_DATASET_ALL_CITATIONS_{timestamp}.xlsx", index=False)



#### How to use the programs ####

#### Crawl titles from sciencedirect using a search query
#### I use ScienceDirect to crawl the PDFs because they have a large amount of 
#### publicly available papers. SD also allows to enter a search string via an url and apply filters
#### to search for papers. The quality of the papers is generally very high.

# search_query_url = "https://www.sciencedirect.com/search?qs=%28%E2%80%9EFinancial+Performance%E2%80%9C+OR+%E2%80%9ECorporate+Finance%E2%80%9C%29+AND+%28%E2%80%9EESG%E2%80%9C+OR+%E2%80%9ESustainability%E2%80%9C+OR+%E2%80%9ECSR%E2%80%9C%29+AND+%28%E2%80%9EQuantitative%E2%80%9C+OR+%E2%80%9EStatistical%E2%80%9C+OR+%E2%80%9ECorrelation%E2%80%9C+OR+%E2%80%9ERegression%E2%80%9C%29&tak=%28%E2%80%9EFinancial+Performance%E2%80%9C+OR+%E2%80%9ECorporate+Finance%E2%80%9C%29+AND+%28%E2%80%9EESG%E2%80%9C+OR+%E2%80%9ESustainability%E2%80%9C+OR+%E2%80%9ECSR%E2%80%9C%29+AND+%28%E2%80%9EQuantitative%E2%80%9C+OR+%E2%80%9EStatistical%E2%80%9C+OR+%E2%80%9ECorrelation%E2%80%9C+OR+%E2%80%9ERegression%E2%80%9C%29&date=2015-2025&articleTypes=FLA&accessTypes=openaccess&lastSelectedFacet=accessTypes" # Needs to be a URL that includes the search query   
# pages = 4           # Define the number of pages of the search results that should be crawled / pages: 1-5 

# crawl_ScienceDirect = Driver_ScienceDirect(search_query_url, pages)
# crawl_ScienceDirect.crawl_page()

### The driver crawls the titles from ScienceDirect and saves the titles 
### as xlsx File with the column name 'Titles'


#### Crawl citations from Google Scholar using the titles from Science Direct

### Here we load the excel file with the titles of the papers into the program.
### We crawl Google Scholar because we can choose between different citation styles
### that will be later parsed. 
# 
### The program takes as an argument the filename of the excel file with the column name 'Titles'

# titles_filename = "ALL_TITLES_08-10-25_18-22-12.xlsx"

# crawl_GoogleScholar = Driver_GoogleScholar(titles_filename)
# crawl_GoogleScholar.crawl_page()


#### Extract information from GS full citation and generate structured dataset

### The program transforms the full citations from Google Scholar into a structured 
### dataset. The program's input is an excel sheet that contains a column "Full_Citations" with 
### string data.

# filename = "ALL_GOOGLE_SCHOLAR_CITATIONS_08-10-2025_12-33:11.xlsx"

# extract_citations = Dataset_All_Citations_Structured(filename)
# extract_citations.generate_dataframe()


# As soon as the dataset is generated, I manually edit the dataset by going
# through the titles and check whether the topics of the articles match with the
# topic of interest. 

# Here I manually included two columns: 'Excluded' and 'Reason_for_exclusion'. In
# the Excluded column I just inserted a Boolean "True" if the paper was excluded.
# In the column Reason_for_exclusion I inserted a note of the reason why the
# article was excluded. Large amounts of data such as the abstracts or the pdf 
# files will be only downloaded for non-excluded citations.


#### Crawl abstracts based on Titles from ScienceDirect 

# filename = "FINAL_DATASET_CITATIONS_06-10-2025_19-27-12.xlsx"

# crawl_abstracts = Driver_ScienceDirect_Abstract(filename)
# crawl_abstracts.crawl_page()


#### Download pdfs based on Titles from ScienceDirect

#filename = "FINAL_DATASET_CITATIONS_06-10-2025_19-27-12.xlsx"

#crawl_pdfs = Driver_ScienceDirect_PDFs(filename)
#crawl_pdfs.crawl_page()


#### Extract titles from PDFs meta data and rename files

#pdf_directory_name = "PDF_Downloads_ESG_Banking"

#extract_titles = PDF_File_Titles(pdf_directory_name)
#extract_titles.rename_file_into_pdf_title()


### Check dataset whether pdfs are available

# pdf_directory = "PDF_Downloads_ESG_Banking"
# filename = "FINAL_DATASET_CITATIONS_incl_pdf_urls_08-10-2025_18-14-29.xlsx"

# check_data = Dataset_Check_For_PDF(pdf_directory, filename)
# check_data.check_dataset()

# Class and function check whether the filenames in the pdf directory match with 
# the titles in the dataset 

# Then I manually check the matching scores 


### Finally merge the different datasets

# merge_data = join_excel_tables()
