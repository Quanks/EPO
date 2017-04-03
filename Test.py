import requests
from bs4 import BeautifulSoup
import lxml
import html5lib
import time
import epo_ops
import oauth2

payload = {'inUserName': 'DuncanBarr', 'inUserPass': '1'}

start_number = 1000000
run_size = 2000
wait_time = 2
publication_languages = [0] * run_size
grant_check = [0] * run_size
agent_nationality = [0] * run_size
agent_name = [0] * run_size

for EP_number in range (start_number, start_number + run_size):
    print (EP_number)



    response = requests.get("http://ops.epo.org/3.1/rest-services/register/publication/epodoc/EP" + str(EP_number) + "/biblio", payload)
    print (response.status_code)
#    print(response.content)
    
    if response.status_code == 403:
        wait_multiplier = 1
        while True:
            time.sleep(60 * wait_multiplier)
            response = requests.get("http://ops.epo.org/3.1/rest-services/register/publication/epodoc/EP" + str(EP_number) + "/biblio", payload)
            print(response.status_code)
            wait_multiplier = wait_multiplier + 1
            if response.status_code == 200 or response.status_code == 404:
                break
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html5lib")
    #    print(soup)
        refs = soup.findAll("reg:publication-reference")
        array_length = len(refs)
    #    print (refs)
        for i in range(array_length):
    #        print (i)
    #        print(refs[i])
    #        print(refs[i].find('reg:country').contents[0])
    #        print(refs[i].find('reg:kind').contents[0])
            if refs[i].find('reg:kind').contents[0] != "B9" and refs[i].find('reg:kind').contents[0] != "B8" and refs[i].find('reg:kind').contents[0] != "A3" and refs[i].find('reg:kind').contents[0] != "A1 / A2 re":
                publication_language = refs[i].find('reg:document-id').attrs['lang']
            else:
                publication_language = refs[i-1].find('reg:document-id').attrs['lang']
     #       test2 = test['lang']
     #       print (publication_language)
            
            if refs[i].find('reg:country').contents[0] == "EP":
                if refs[i].find('reg:kind').contents[0] == "A1" or refs[i].find('reg:kind').contents[0] == "A2":
                    publication_languages[EP_number-start_number]= publication_language
                elif refs[i].find('reg:kind').contents[0] == "B1":
                    grant_check[EP_number - start_number] = 1
        
        agents_refs = soup.findAll("reg:agents")
    #    print (agents_refs)
        i_agent_country_finder = 0
        agents_refs_length = len(agents_refs)
        if agents_refs_length > 0:
            while True:
    #            print(i_agent_country_finder)
                if agents_refs[i_agent_country_finder].find("reg:name").contents[0] != "(deleted)":
                    agent_nationality[EP_number-start_number] = agents_refs[i_agent_country_finder].find("reg:country").contents[0]
                    agent_name[EP_number-start_number] = agents_refs[i_agent_country_finder].find("reg:name").contents[0]
                    break
                i_agent_country_finder = i_agent_country_finder + 1
    #    print (refs)
       
        
        time.sleep(wait_time)
    
    elif response.status_code == 404:
        print ("No Record")
    else:
        break
    
    
    
    
#    print (refs)
 #   print(soup)
print (publication_languages)
print(agent_nationality)
print(agent_name)
print(grant_check)

english_count = 0
english_grant_count = 0
english_publication_english_agent_count = 0
english_publication_german_agent_count = 0
english_publication_english_agent_grant_count = 0
english_publication_BWT_agent_count = 0
english_publication_BWT_agent_grant_count = 0
english_publication_german_agent_grant_count = 0
english_publication_no_agent_count = 0
english_publication_no_agent_grant_count = 0
german_count = 0
german_grant_count = 0
german_publication_english_agent_count = 0
german_publication_german_agent_count = 0
german_publication_english_agent_grant_count = 0
german_publication_german_agent_grant_count = 0
german_publication_no_agent_count = 0
german_publication_no_agent_grant_count = 0
french_count = 0
french_grant_count = 0
french_publication_english_agent_count = 0
french_publication_german_agent_count = 0
french_publication_english_agent_grant_count = 0
french_publication_german_agent_grant_count = 0
french_publication_no_agent_count = 0
french_publication_no_agent_grant_count = 0


for i_languageChecker in range(len(publication_languages)):
        if publication_languages[i_languageChecker] == "en":
            english_count = english_count + 1
            if grant_check[i_languageChecker] == 1:
                english_grant_count = english_grant_count + 1
            if agent_nationality[i_languageChecker] == "GB":
                english_publication_english_agent_count = english_publication_english_agent_count + 1
                if agent_name[i_languageChecker] == "Boult Wade Tennant":
                    english_publication_BWT_agent_count = english_publication_BWT_agent_count + 1
                if grant_check[i_languageChecker] == 1:
                    english_publication_english_agent_grant_count = english_publication_english_agent_grant_count + 1
                    if agent_name[i_languageChecker] == "Boult Wade Tennant":
                        english_publication_BWT_agent_grant_count = english_publication_BWT_agent_grant_count + 1
                
                    
            elif agent_nationality[i_languageChecker] == "DE":
                english_publication_german_agent_count = english_publication_german_agent_count + 1
                if grant_check[i_languageChecker] == 1:
                    english_publication_german_agent_grant_count = english_publication_german_agent_grant_count + 1
            elif agent_nationality[i_languageChecker] == 0:
                english_publication_no_agent_count = english_publication_no_agent_count + 1
                if grant_check[i_languageChecker] == 1:
                    english_publication_no_agent_grant_count = english_publication_no_agent_grant_count + 1
        elif publication_languages[i_languageChecker] == "de":
            german_count = german_count + 1
            if grant_check[i_languageChecker] == 1:
                german_grant_count = german_grant_count + 1
            if agent_nationality[i_languageChecker] == "GB":
                german_publication_english_agent_count = german_publication_english_agent_count + 1
                if grant_check[i_languageChecker] == 1:
                    german_publication_english_agent_grant_count = german_publication_english_agent_grant_count + 1
            elif agent_nationality[i_languageChecker] == "DE":
                    german_publication_german_agent_count = german_publication_german_agent_count + 1
                    if grant_check[i_languageChecker] == 1:
                        german_publication_german_agent_grant_count = german_publication_german_agent_grant_count + 1
            elif agent_nationality[i_languageChecker] == 0:
                german_publication_no_agent_count = german_publication_no_agent_count + 1
                if grant_check[i_languageChecker] == 1:
                    german_publication_no_agent_grant_count = german_publication_no_agent_grant_count + 1
        elif publication_languages[i_languageChecker] == "fr":
            french_count = french_count + 1
            if grant_check[i_languageChecker] == 1:
                french_grant_count = french_grant_count + 1
            if agent_nationality[i_languageChecker] == "GB":
                french_publication_english_agent_count = french_publication_english_agent_count + 1
                if grant_check[i_languageChecker] == 1:
                    french_publication_english_agent_grant_count = french_publication_english_agent_grant_count + 1
            elif agent_nationality[i_languageChecker] == "DE":
                    french_publication_german_agent_count = french_publication_german_agent_count + 1
                    if grant_check[i_languageChecker] == 1:
                        french_publication_german_agent_grant_count = french_publication_german_agent_grant_count + 1
            elif agent_nationality[i_languageChecker] == 0:
                french_publication_no_agent_count = french_publication_no_agent_count + 1
                if grant_check[i_languageChecker] == 1:
                    french_publication_no_agent_grant_count = french_publication_no_agent_grant_count + 1


print("")
print("Number Searched: %d" %run_size)
print("")
print("Number of English Publications: %d" %english_count)
print("Number of English Grants: %d" %english_grant_count)
print("Number of English Language Applications with English Agents: %d" %english_publication_english_agent_count)
print("Number of which granted: %d" %english_publication_english_agent_grant_count)
print("Number of English Language Applications with BWT as Agents: %d" %english_publication_BWT_agent_count)
print("Number of which granted: %d" %english_publication_BWT_agent_grant_count)
print("Number of English Language Applications with German Agents: %d" %english_publication_german_agent_count)
print("Number of which granted %d" %english_publication_german_agent_grant_count)
print("Number of English Language Applications with no Agents: %d" %english_publication_no_agent_count)
print("Number of which granted %d" %english_publication_no_agent_grant_count)
print("")
print("Number of German Publications: %d" %german_count)
print("Number of German Grants: %d" %german_grant_count)
print("Number of German Language Applications with English Agents: %d" %german_publication_english_agent_count)
print("Number of which granted: %d" %german_publication_english_agent_grant_count)
print("Number of German Language Applications with German Agents: %d" %german_publication_german_agent_count)
print("Number of which granted %d" %german_publication_german_agent_grant_count)
print("Number of German Language Applications with no Agents: %d" %german_publication_no_agent_count)
print("Number of which granted %d" %german_publication_no_agent_grant_count)
print("")
print("Number of French Publications: %d" %french_count)
print("Number French Grants: %d" %french_grant_count)
print("Number of French Language Applications with English Agents: %d" %french_publication_english_agent_count)
print("Number of which granted: %d" %french_publication_english_agent_grant_count)
print("Number of French Language Applications with German Agents: %d" %french_publication_german_agent_count)
print("Number of which granted %d" %french_publication_german_agent_grant_count)
print("Number of French Language Applications with no Agents: %d" %french_publication_no_agent_count)
print("Number of which granted %d" %french_publication_no_agent_grant_count)