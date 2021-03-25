#!/usr/bin/env python3

# ****** # # # # # # # # # # # # # # # # # # # # # # ****** #
# ******                                             ****** #
# ******   Name: Siddhant Shah                       ****** #
# ******   Date: 24/03/2020                          ****** #
# ******   Desc: SCRAPER FOR SOURCESCRUB             ****** #
# ******   Email: siddhant.shah.1986@gmail.com       ****** #
# ******                                             ****** #
# ****** # # # # # # # # # # # # # # # # # # # # # # ****** #


# ! PROJECT REQUIREMENTS 
# ## Script to fetch data from Sourcescrub.com


# >> IMPORTANT IMPORT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from termcolor import cprint
from datetime import datetime
import pandas as pd
from colorama import init
from random import choice, randint
import json, requests, os, pyfiglet, time, sys, emoji


# >> GLOBAL VARIABLES
SLEEP_TIME = []
CONFIG = {}
BROWSER = None
COMPANY = []


# >> just for decoration
def intro():
    print()
    print(pyfiglet.figlet_format(" GeekySid"))
    print()
    print('  # # # # # # # # # # # # # # #  # # # # # # # #')
    print('  #                                            #')
    print('  #          SCRAPER FOR SOURCESCRUB           #')
    print('  #             By: SIDDHANT SHAH              #')
    print('  #               Dt: 24/03/2020               #')
    print('  #        siddhant.shah.1986@gmail.com        #')
    print('  #      **Just for Educational Purpose**      #')
    print('  #                                            #')
    print('  # # # # # # # # # # # # #  # # # # # # # # # #')
    print()


# >> reading config data
def read_config():
    global CONFIG
    if os.path.exists('config.json'):
        with open('config.json', 'r') as r:
            CONFIG = json.load(r)
            # print(json.dumps(CONFIG, indent=4))
        return True


# >> returns randome sleep time
def get_random_sleep():
    sleep_time = CONFIG['sleep_time']
    if len(sleep_time) > 1:
        return randint(sleep_time[0], sleep_time[1])/10
    else:
        return sleep_time[0]


# >> function to generate new browser
def get_new_browser(headless=False):
    global BROWSER

    # Setting up Options for web browser
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") # also works
    chrome_options.add_argument("--disable-dev-shm-usage") # also works
    chrome_options.headless = headless
    try:
        chrome_options.add_extension('lastpass.crx')
    except:
        pass

    BROWSER = webdriver.Chrome(executable_path = CONFIG['path_to_chromedriver'], options=chrome_options)

    BROWSER.maximize_window()
    BROWSER.get(CONFIG['starting_pont'])


# >> function to generate new browser
def save_company_to_file(file_name):
    # # saving json
    # with open(f'{file_name}.json', 'w') as w:
    #     json.dump(COMPANY, w)

    # saving csv
    pd.DataFrame(COMPANY).to_csv(f'Data/{file_name}.csv', index=False)
    

# >> fetch data or company
def fetch_company_data(company):
    global COMPANY
    company_dict = {'COMPANY': company}

    try:
        content_div = BROWSER.find_element_by_id('overview')
        general_info_group = content_div.find_elements_by_class_name('general-info_group')


        # ! links 
        links = content_div.find_element_by_tag_name('h2').find_elements_by_class_name('main-info_title-web-link')
        for link in links:
            value = link.get_attribute('href')
            key = value.split('//')[-1].split('www.')[-1].split('.')[0]
            if not key == 'linkedin':
                key = 'website'
            company_dict[key.upper()] = value
            # cprint(f'              [>>>] {key}: {value}', 'yellow')


        # ! description 
        description_div = general_info_group[0]
        description = description_div.find_element_by_tag_name('p').text.strip()
        company_dict['description'.upper()] = description
        # cprint(f'              [>>>] Description: {description[:10]}', 'yellow')
        

        # ! details 
        details_div = general_info_group[1]
        details_col_count = len(details_div.find_elements_by_class_name('native-table_header-item'))
        for i in range(0, details_col_count):
            key = details_div.find_elements_by_class_name('native-table_header-item')[i].text.strip()
            value = details_div.find_elements_by_class_name('native-table_row-column')[i].text.strip()
            company_dict[key.upper()] = value
            # cprint(f'              [>>>] {key}: {value}', 'yellow')


        # ! specialities 
        specialities_div = general_info_group[2]
        specialities_list = specialities_div.find_elements_by_tag_name('label')
        specialities = []
        for i in range(len(specialities_list)):
            specialities.append(specialities_list[i].text.strip().title())
        specialities = ', '.join(specialities)
        company_dict['SPECIALTIES'] = specialities
        # cprint(f'              [>>>] Specialities: {specialities}', 'yellow')


        # ! investors 
        investors_div = general_info_group[3]
        investors = investors_div.find_element_by_class_name('default_paragraph').text
        company_dict['INVESTORS'] = investors
        # cprint(f'              [>>>] Investors: {investors}', 'yellow')


        # ! investements 
        investments_div = general_info_group[4]
        investments = []
        try:
            investments_value_cols = investments_div.find_element_by_class_name('ag-center-cols-container').find_element_by_xpath('./div').find_elements_by_class_name('ag-cell-value')
            for investments_value_col in investments_value_cols:
                key = investments_value_col.get_attribute('col-id')
                value = investments_value_col.text.split('Show')[0].strip()
                investments.append(f'{key}: {value}')
                # cprint(f'              [>>>] {key}: {value}', 'yellow')
        except:
            pass

        company_dict['investements'.upper()] = '\n'.join(investments)


        # ! financials 
        financials_div = general_info_group[5]
        try:
            financials = []
            financials_headers = []
            financials_headers_cols = financials_div.find_elements_by_class_name('native-table_header-item')
            for financials_headers_col in financials_headers_cols:
                financials_headers.append(financials_headers_col.text.strip())
            
            financials_rows = financials_div.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            for financials_row in financials_rows:
                financials_datapoints = financials_row.find_elements_by_class_name('native-table_row-column')
                datapoint_count = 0
                for financials_datapoint in financials_datapoints:
                    key = financials_headers[datapoint_count]
                    value = financials_datapoint.text.strip()
                    datapoint_count += 1
                    financials.append(f'{key}: {value}')
                    # cprint(f'              [>>>] {key}: {value}', 'yellow')
                break
        except:
            pass
        
        company_dict['financials'.upper()] = '\n'.join(financials)


        # ! People 
        try:
            # people = []
            sidebar_div = content_div.find_element_by_class_name('general-info_chart')
            try:
                content_div.find_element_by_class_name('general-info_show-more').click()
            except:
                pass

            executives = sidebar_div.find_elements_by_class_name('executive_info')
            people_count =  0

            for executive in executives:
                people_count += 1
                executive_name = executive.find_element_by_class_name('executive_name').text.strip()
                # people.append(f'Name: {executive_name}')
                company_dict[f'EXEC_{people_count}--NAME'] = executive_name
                # cprint(f'              [>>>] Executive Name: {executive_name}', 'yellow')

                executives_detail = executive.find_element_by_xpath("./div/div/div").text
                company_dict[f'EXEC_{people_count}--DETAILS'] = executives_detail
                # people.append(f'Detail: {executives_detail}')
                # cprint(f'              [>>>] Executive Detail: {executives_detail}', 'yellow')

                executives_email = executive.find_element_by_class_name('exec-email').find_element_by_tag_name('a').text
                company_dict[f'EXEC_{people_count}--EMAIL'] = executives_email
                # people.append(f'Email: {executives_email}')
                # cprint(f'              [>>>] Executive Email: {executives_email}', 'yellow')

                try:
                    executive_socials = executive.find_element_by_xpath('./div/div[2]').find_elements_by_tag_name('a')
                    for executive_social in executive_socials:
                        key = executive_social.get_attribute('data-id').upper().replace("EXECUTIVE-", '')
                        value = executive_social.get_attribute('href')
                        # people.append(f'{key}: {value}')
                        company_dict[f'EXEC_{people_count}--{key.upper()}'] = value
                        # cprint(f'              [>>>] {key}: {value}', 'yellow')
                except Exception as e:
                    pass
                # people.append('\n')
        except Exception as e:
            pass
            # print(str(e))
        
        # company_dict['people'.upper()] = '\n'.join(people)

        cprint(f'              [>>>] Fetched', 'green')
    except Exception as e:
        cprint(f'              [>>>] Exception: {str(e)}', 'red')
    
    COMPANY.append(company_dict)


# >> go to inividual Company Page
def go_to_company(companies):
    print('\n')
    cprint(f'      [>] STARTING TO PULL DATA FOR INVIDUAL COMPANIES ', 'blue', 'on_white', attrs=['bold'])
    company_count = 1

    for company in companies:
        cprint(f'\n          [{company_count}] {company["name"]} ', 'cyan')
        company_count += 1

        # Open a new window tab
        BROWSER.execute_script("window.open('');")

        # Switch to the new window
        BROWSER.switch_to.window(BROWSER.window_handles[1])
        BROWSER.get(company['url'])
        time.sleep(3)

        fetch_company_data(company["name"])

        # close the active tab
        BROWSER.close()
        time.sleep(1)

        # Switch back to the first tab
        BROWSER.switch_to.window(BROWSER.window_handles[0])
        time.sleep(2)


# >> function to load all companies
def load_all_companies(filtered_company_count):
    cprint(f'          [>>] Making sure all compnies ({filtered_company_count}) are loaded on the page.', 'cyan')
    companies = []

    # checking if all companies are loaded on the page
    while True:
        companies_div = BROWSER.find_elements_by_xpath('//span[@class="ss-grid_entity-name-name"]')
        
        if len(companies_div) >= filtered_company_count:
            cprint(f'              [>>>] All ({filtered_company_count}) are loaded on the page.', 'green')

            for company in companies_div:
                companies.append({
                    'name': company.find_element_by_tag_name('a').text,
                    'url': company.find_element_by_tag_name('a').get_attribute('href')
                })

            time.sleep(1)
            BROWSER.execute_script("document.body.style.zoom='100%'")
            
            break
        else:            
            cprint(f'              [>>>] Only {len(companies_div)} out of {filtered_company_count} are loaded on the page. Trying To load more', 'yellow')
            BROWSER.execute_script("document.body.style.zoom='1%'")
            time.sleep(2)

    go_to_company(companies)


# >> get total number of companies that are found 
def get_company_count():
    print()

    cprint(f'[?] Please enter total Number of filtered companies. ', 'yellow', attrs=['bold'])
    while True:
        try:
            filtered_company_count = int(input().strip())
            break
        except:
            cprint(f'[?] Not a avlid Number. Please enter again ', 'yellow', attrs=['bold'])

    cprint(f'\n      [>] Script is Starting ', 'blue', 'on_white', attrs=['bold'])
    return filtered_company_count

    # # getting count of compnaies filtered
    # try:
    #     count_text = BROWSER.find_element_by_xpath('/html/body/app-root/app-site-layout/div/div/app-company-search/div/h3').text
    #     filtered_company_count = int(count_text.split(' ')[0].strip().replace('+', ''))
    #     cprint(f'\n          [>>] Total {filtered_company_count} of Companies Filtered.', 'cyan')
    #     return filtered_company_count
    # except Exception as e:
    #     cprint(f'\n          [x] Error in fetching count of filtered companies.', 'red')
    #     cprint(f'          [x] Exception: {str(e)}', 'red')


# >> main function
def main():
    print()
    while True:
        cprint(f'  [+] Kindly Press Enter when script should start to read data. (Max 500 COmpanies) ', 'magenta', attrs=['bold'])
        input()
        file_name = f'{time.time()}'
        filtered_company_count = get_company_count()
        if filtered_company_count:
            load_all_companies(filtered_company_count)
            save_company_to_file(file_name)
        else:
            cprint(f'          [x] No filtered companies found.', 'red')
        
        print('\n')
        cprint(f'  [?] Press 1 if you want to search for more tags else press 0  ', 'white', 'on_blue', attrs=['bold'])
        
        if not input().strip() == '1':
            print()
            cprint(f'  [+] Terminating Script  ', 'magenta', attrs=['bold'])
            break
        else:
            print('\n')


# >> displays total time taken for entire script to run
def time_calculator(start_time):
    end_time = time.time()

    time_diff = (end_time-start_time)
    hrs = int((time_diff)//3600)
    mins = int(((time_diff)%3600)//60)
    secs = int(((time_diff)%3600)%60)
    time_string = f'  [🕐] Total Time taken: {hrs}hrs {mins}mins {secs}secs  '
    time.sleep(5)

    print('\n')
    cprint("="*len(time_string), 'grey', 'on_white', attrs=['bold'])
    cprint(time_string, 'grey', 'on_white', attrs=['bold'])
    cprint("="*len(time_string), 'grey', 'on_white', attrs=['bold'])
    print('\n')


# >> executed only if not used as an imported module
if __name__ == '__main__':
    init()
    start_time = time.time()
    intro()

    if read_config():
        try:
            get_new_browser()
            main()
        except Exception as e:
           cprint(f'\n\n  [X] Exception: {str(e)}\n\n', 'red', attrs=['bold'])
           input('press enter to quit')
        
        if BROWSER:
            BROWSER.quit()
    else:
        cprint(f'\n\n  [X] Problem in reading CONFIG file.\n\n', 'red', attrs=['bold'])

    time_calculator(start_time)