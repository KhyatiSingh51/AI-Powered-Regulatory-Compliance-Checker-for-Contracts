import requests
import json
import data_extraction
import time
import notification

# scrape data from different links using GET API
def scrape_data(url, name):

    
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(name, "wb") as f:
               for chunk in response.iter_content(chunk_size=1024):
                  if chunk:
                      f.write(chunk)
            print("Download Successful", time.ctime())
        else:
            print("Failed to download", response.status_code)
            notification.send_notification("Failed to Download file", f"Response status is {response.status_code} and Download link is {url} \n Error is {response.text} ")
         



def call_scrape_funtion():
    try:
        # nested dict
        DOCUMENT_MAP = {
            "DPA": {"json_file":"json_file/dpa.json", "link":r"https://www.benchmarkone.com/wp-content/uploads/2018/05/GDPR-Sample-Agreement.pdf"},
        "JCA": {"json_file":"json_file/jca.json", "link":r"https://www.surf.nl/files/2019-11/model-joint-controllership-agreement.pdf"},
        "C2C":{"json_file":"json_file/c2c.json", "link":r"https://www.fcmtravel.com/sites/default/files/2020-03/2-Controller-to-controller-data-privacy-addendum.pdf"},    
        "SCC":{"json_file":"json_file/scc.json", "link":r"https://www.miller-insurance.com/assets/PDF-Downloads/Standard-Contractual-Clauses-SCCs.pdf"},    
        "subprocessing":{"json_file":"json_file/subprocessing.json", "link":r"https://greaterthan.eu/wp-content/uploads/Personal-Data-Sub-Processor-Agreement-2024-01-24.pdf"}    
    }

        temp_agreement = "temp_agreement.pdf"

        for key, value in DOCUMENT_MAP.items():
            # scrape agreement file
            scrape_data(DOCUMENT_MAP[key]["link"], temp_agreement)

            # extract clauses
            # clauses = data_extraction.Clause_extraction(temp_agreement)

            # Step 6: Update respective json file with new clauses
            # with open(DOCUMENT_MAP[key]["json_file"], "w", encoding="utf-8") as f:
            #     json.dump(clauses, f, indent=2, ensure_ascii=False)

        # print("All downloads and JSON updates completed successfully ✅")

    except Exception as e:
        print("Error Occured in Scrapping", e)
        notification.send_notification("Error Occured in Scrapping", f"Error is {e}")


# call_scrape_funtion()
