import gc
import time
import os
import json

from scheduling_algorithms.brute_force import BruteForce
# from scheduling_algorithms.brute_force_lightweight import BruteForce
from utils.time import get_human_readable_timestamp

# MAX_TESTS = 100
MAX_TESTS = float('inf')
WORKER_LIMIT = 3

if __name__ == "__main__":
    human_readable_time = get_human_readable_timestamp()
    file_name =  f"test_{human_readable_time}"

    with open((os.path.join("test_results", f"{file_name}.json")), "a") as results_file:
        results_file.write("[\n")
        
        i = 1
        w = 3  # Start from 3
        can_execute = True
        while can_execute:  # Infinite loop
            for t in range(2, w + 1):
                start_time = time.time()  # Record the start time

                bf = BruteForce(w, t)
                sims, min_val, min_keys = bf.run()
                print(f"Test {i}: Workers - {w} | Tasks - {t} | Simulations - {sims} | Lowest Net Cost - {min_val}")

                end_time = time.time()  # Record the end time
                elapsed_time = end_time - start_time  # Calculate the elapsed time
                print(f"Time taken: {elapsed_time} seconds\n")

                # Output to a JSON file
                # Create a dictionary with the test results
                test_result = {
                    "Test": i,
                    "Workers": w,
                    "Tasks": t,
                    "Simulations": sims,
                    "Lowest_Net_Cost": min_val,
                    "Time_taken": elapsed_time
                }

                # Convert the dictionary to a JSON string
                json_string = json.dumps(test_result)

                # Write the JSON string to the file
                results_file.write(json_string + ",\n")
                results_file.flush()
                
                i += 1
                if i > MAX_TESTS:  # Condition to exit the loop
                    can_execute = False
                    break
            
            if w >= WORKER_LIMIT:  # Condition to exit the loop
                    can_execute = False
                    break

            # Clean up memory
            gc.collect()

            w += 1
    
        results_file.write("]\n")