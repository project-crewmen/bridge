import gc
import time
import os
import json
from dotenv import load_dotenv

from utils.time import get_human_readable_timestamp
from scheduling_algorithms.bf.brute_force import BruteForce

if __name__ == "__main__":
    load_dotenv()
    
    human_readable_time = get_human_readable_timestamp()
    file_name =  f"test_{human_readable_time}"
     
    with open((os.path.join("out/sim_results", f"{file_name}.json")), "a") as results_file:
        results_file.write("[\n")

        t = 0
        for w_amt in range(3, 4):
            for t_amt in range(2, w_amt+1):
                start_time = time.time()  # Record the start time

                bf = BruteForce(w_amt, t_amt)
                perms, deps, min_netcost = bf.run()
                
                print(f"--- Test #{t} - Workers: {w_amt} | Tasks: {t_amt} ---")
                print("Total number of permutations: ", perms)
                print("Deployement Set (Least Net Cost): ")
                dep_maps: list[str] = []
                # print(deps)
                for d in deps:
                    dep_maps.append(d.get_display_text())

                print(dep_maps)

                print("Minimum Netcost: ", min_netcost, "\n")                

                end_time = time.time()  # Record the end time
                elapsed_time = end_time - start_time  # Calculate the elapsed time
                print(f"Time taken: {elapsed_time} seconds\n")

                 # Output to a JSON file
                # Create a dictionary with the test results
                test_result = {
                    "Test": t,
                    "Workers": w_amt,
                    "Tasks": t_amt,
                    "Total number of permutations": perms,
                    "Deployement Set (Least Net Cost)": dep_maps,
                    "Minimum Netcost": min_netcost,
                    "Time_taken": elapsed_time
                }

                # Convert the dictionary to a JSON string
                json_string = json.dumps(test_result)

                # Write the JSON string to the file
                results_file.write(json_string + ",\n")
                results_file.flush()

                t += 1 

                break
   
        # Clean up memory
        gc.collect()
    
        results_file.write("]\n")