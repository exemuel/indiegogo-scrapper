# load standard libraries
import sys
import os

# load data analysis library
import pandas as pd

# load modules in scraper
from scraper import *

def main():
    args = sys.argv[1:]

    if os.path.exists("chromedriver\chromedriver.exe") is False:
        print("Put chromedriver.exe into chromedriver directory.")
    else:
        if os.path.exists("data\Indiegogo.csv") is False:
            print("Put Indiegogo.csv into data directory.")
        else:
            if len(args) < 1:
                print("Define the json filename.")
            elif args[0].find(".json")!=-1:
                dir_path_data = "data"
                dir_path_output = "out\\" + args[0]

                filenames = next(os.walk(dir_path_data), (None, None, []))[2]

                list_project_site = []
                for ele in filenames:
                    df_indiegogo = pd.read_csv(dir_path_data + "\\" + ele)
                    list_project_site.extend(extract_project_url(df_indiegogo))
                
                try:
                    with open(dir_path_output) as json_file:
                        data = json.load(json_file)
                        print("\nCheckpoint from", str(len(data)), "of", str(len(list_project_site)))
                        print("Project site:", data[str(len(data)-1)]["site"])
                        print("\nStarting to scrape...")
                except Exception as e:
                    data = {}
                    print("\nStarting to scrape...")
                
                if len(data) < 1:
                    for idx, val in enumerate(list_project_site):
                        dict_tmp = {}
                        if idx < 1:
                            print(str(idx+1), "of", str(len(list_project_site)), "| Scrape", val)
                            dict_tmp[idx] = {
                                "site": val,
                                "basic_story": scrape_basic_and_story(val),
                                "faq": scrape_faq(val),
                                "updates": scrape_updates(val),
                                "disscusion": scrape_discussion(val),
                                "comments": scrape_comments(val)
                            }

                            with open(dir_path_output, 'w') as f:
                                json.dump(dict_tmp, f)
                        else:
                            with open(dir_path_output, "r+") as file:
                                dict_tmp = json.load(file)
                                print(str(idx+1), "of", str(len(list_project_site)), "| Scrape", val)
                                dict_tmp[idx] = {
                                    "site": val,
                                    "basic_story": scrape_basic_and_story(val),
                                    "faq": scrape_faq(val),
                                    "updates": scrape_updates(val),
                                    "disscusion": scrape_discussion(val),
                                    "comments": scrape_comments(val)
                                }
                                file.seek(0)
                                json.dump(dict_tmp, file)
                else:
                    for idx, val in enumerate(list_project_site):
                        if idx < (len(data)-1):
                            continue
                        elif idx == (len(data)-1):
                            data.popitem()
                            with open(dir_path_output, 'w') as f:
                                json.dump(data, f)
                            
                            with open(dir_path_output, "r+") as file:
                                dict_tmp = json.load(file)
                                print(str(idx+1), "of", str(len(list_project_site)), "| Scrape", val)
                                dict_tmp[idx] = {
                                    "site": val,
                                    "basic_story": scrape_basic_and_story(val),
                                    "faq": scrape_faq(val),
                                    "updates": scrape_updates(val),
                                    "disscusion": scrape_discussion(val),
                                    "comments": scrape_comments(val)
                                }
                                file.seek(0)
                                json.dump(dict_tmp, file)
                        else:
                            with open(dir_path_output, "r+") as file:
                                dict_tmp = json.load(file)
                                print(str(idx+1), "of", str(len(list_project_site)), "| Scrape", val)
                                dict_tmp[idx] = {
                                    "site": val,
                                    "basic_story": scrape_basic_and_story(val),
                                    "faq": scrape_faq(val),
                                    "updates": scrape_updates(val),
                                    "disscusion": scrape_discussion(val),
                                    "comments": scrape_comments(val)
                                }
                                file.seek(0)
                                json.dump(dict_tmp, file)
            else:
                print("Wrong output file extension. Use JSON extension.")
            print("*** End ***")

if __name__ == '__main__':
    main()