import random
import json
import csv
import math



"""
* generate_jobs -> This function takes in a random sample of jobs and returns a list of job objects. This function also selects 
*   these jobs based on the given input parameters
* 
* INPUTS
*   jobs_array (List) -> an unsorted list of all of the jobs available to the user
*   start_time (int) -> The time after which all jobs must start
*   end_time (int) -> The time by which all jobs must end
*   max_length (int) -> The maximum duration of a given job
*   batch_size (int) -> The size of the batch
* 
* ADDITIONAL
* This function will select the jobs based on the parameters. However, it should not select different jobs than other algorithms becuase they will all
* be provided with the same jobs_array list and parameters
"""
def generate_jobs(jobs_array, start_time, end_time, max_length, batch_size):
    jobs = []

    # Iterate through the job objects and create an array of objects that fall within the specified time window
    i = 0
    curr_index = 0
    while (i < batch_size):
        aj = jobs_array[curr_index]['release']
        dj = jobs_array[curr_index]['deadline']
        lj = jobs_array[curr_index]['length']

        fj = aj - dj - lj

        # Check if the specific job lies within the correct window
        # The funky syntax is used to put the job id at the very front of the dictionary
        if aj >= start_time and dj <= end_time and lj <= max_length:
            job_id = {"job_id" : i}

            flexibility = {'flexibility': fj}
            flexible_object = {**job_id, **flexibility, **jobs_array[curr_index]}
            jobs.append(flexible_object)
            
            i += 1
        
        curr_index += 1

    # Sort the jobs in ascending order based on their flexibility
    jobs = sorted(jobs, key=lambda job: job['flexibility']) 

    return jobs



"""
* get_job_intervals -> This function is responsible for going through each of the jobs in the algorithm and returning all the intervals 
*   that the job could possibly run within
* 
* INPUTS
*   jobs (list) -> This is the list of jobs in this case
"""
def get_job_intervals(jobs, start_time):
    intervals = [[] for _ in range(len(jobs))]
    for i, job in enumerate(jobs):
        # Extract the necessary information from the job object
        release = job['release'] - start_time
        deadline = job['deadline'] - start_time
        duration = job['length']
        num = release

        # Add the execution intervals to the sublist
        while (num + duration <= deadline):
            intervals[i].append((num, num + duration))
            num += 1
    
    return intervals



"""
* get_job_heights -> This function returns a list of the height of each respective job. The index of the job height corresponds to the 
*   jobs id
* 
* INPUTS
*   jobs (list) -> The list of jobs for the trial
"""
def get_job_heights(jobs):
    height = [job['height'] for job in jobs]

    return height


"""
* generate_greedy_schedule -> This function takes in the jobs ordered by their flexibility and schedules them greedily based
*   on the amount of job area above the curve
* 
* INPUTS
*   intervals (list) -> the intervals during which each job can run
*   jobs (list) -> the list of jobs in the trial
*   num_time_steps -> the number of distinct time steps during the period
* 
* ADDITIONAL
* This function returns a list of height values across the entire time period. These are the heights generated by the greedy schedule
"""
def generate_greedy_schedule(jobs, resources, intervals, num_time_steps):
    final_heights = [0 for _ in range(num_time_steps)]
    for job_id, interval_set in enumerate(intervals):
        best_score = float(math.inf)
        best_interval = None

        job_height = jobs[job_id]['height']

        for interval in interval_set:
            interval_start, interval_end = interval[0], interval[1]

            # We want to find the max of this array above
            # because we are more concerned right now with PDAC
            score = sum([(final_heights[i] + job_height) - resources[i] for i in range(interval_start, interval_end)])

            if score < best_score:
                best_score = score
                best_interval = interval

        
        for i in range(best_interval[0], best_interval[1]):
            final_heights[i] += job_height    
    
    return final_heights


"""
* solve_aac_greedy -> This function calculates and returns the objective value for the greedy schedule
* 
* INPUTS
*   final_heigts (list) -> The list of heights generated by the greedy schedule
"""
def solve_aac_greedy(jobs_array, resources, start_time, end_time, max_length, batch_size):
    # Specify the number of time steps 
    num_time_steps = end_time - start_time

    # Generate the jobs
    jobs = generate_jobs(jobs_array, start_time, end_time, max_length, batch_size)

    # Generate the intervals
    intervals = get_job_intervals(jobs, start_time)

    final_heights = generate_greedy_schedule(jobs, resources, intervals, num_time_steps)

    objective_value = 0
    for i, height in enumerate(final_heights):
        if height - resources[i] > objective_value:
            objective_value = height - resources[i]


    # print("Greedy Objctive Value:", objective_value)
    return objective_value

