# load standard libraries
import sys
import os

# load data analysis library
import pandas as pd

# load modules in scraper
from scraper import *
import multiprocessing

def main():
    args = sys.argv[1:]

    if os.path.exists("chromedriver\chromedriver.exe") is False:
        print("put chromedriver.exe into chromedriver directory.")
    else:
        if os.path.exists("data\Indiegogo.csv") is False:
            print("put Indiegogo.csv into data directory.")
        else:
            if len(args) < 1:
                print("define the json filename.")
            elif args[0].find(".json")!=-1:
                dir_path_data = "data"
                dir_path_output = "out/" + args[0]

                filenames = next(os.walk(dir_path_data), (None, None, []))[2]

                list_project_site = []
                for ele in filenames:
                    df_indiegogo = pd.read_csv(dir_path_data + "\\" + ele)
                    list_project_site.extend(extract_project_url(df_indiegogo))

                list_project_site = [[i, e] for i, e in enumerate(list_project_site)]
                
                try:
                    f = open(dir_path_output, "r")
                    data = json.loads(f.read())
                    f.close()
                except Exception as e:
                    data = {}
                
                list_processed = [e for e in list_project_site if e[1] \
                    not in [data[key]["site"] for key in data]]
                
                # process-based parallelism
                # use one third of the available processors
                processor = int(-1 * (multiprocessing.cpu_count()/3) // 1 * -1)
                # use one fourth of the available processors
                # processor = int(multiprocessing.cpu_count()/4)
                pool = multiprocessing.Pool(processes=processor)

                print("*** start ***")

                for b in [list_processed[i:i + processor] for i in range(0, len(list_processed), processor)]:
                    dict_tmp = {}
                    list_bres = pool.map(scrapes, b)
                    
                    for i in list_bres:
                        dict_tmp.update(i)

                    if len(data) < 1:
                        with open(dir_path_output, 'w') as file:
                            json.dump(dict_tmp, file, indent = 4)
                    else:
                        with open(dir_path_output, "r+") as file:
                            old_data = json.load(file)
                            old_data.update(dict_tmp)
                            file.seek(0)
                            json.dump(old_data, file, indent = 4)
                    print("scraped", str(b[-1][0]+1), "of", str(len(list_project_site)-1))
                    break
            else:
                print("wrong output file extension. use json extension.")
            print("*** end ***")

if __name__ == '__main__':
    main()