#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jan 28 10:04:26 2025
Based on: https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
Sample input: --TASK="1"
@author: Matthew Goosney
@author: V01040408
"""

import sys
import pandas as pd
from typing import Optional, List, Dict



def task_1(df: pd.DataFrame) -> pd.DataFrame:
     """
     Function for Task #1 that filters the results of students who have studied more than 40 hours.
     
        Parameters
        -------
        df (pd.DataFrame): Input DataFrame imported from the pandas library that contains data from our given dataset.

        Returns
        -------
        result_df: Variable that contains the imported DataFrame connected to our given dataset; filters Record_ID,
        Hours_Studied, and Exam_Score for students who have studied for more than 40 hours.  
     """
     # Filter students who studied more than 40 hours
     filtered_df = df[df['Hours_Studied'] > 40]

     # Selected (filtered) columns in the dataset for output
     result_df = filtered_df[['Record_ID', 'Hours_Studied', 'Exam_Score']]
     
     return result_df



def task_2(df: pd.DataFrame) -> pd.DataFrame:
    """
    Funtion for Task #2 that filters the results of the top 10 students with exam scores of 85 or higher.

        Parameters
        -------
        df (pd.DataFrame): Input DataFrame imported from the pandas library that contains data from our given dataset.

        Returns
        -------
        result_df: Variable that filters Record_ID, Hours_Studied, and Exam_Score for the top 10 students 
        with exam scores, sorted by score (descending) and ID (ascending).
    """
    filtered_df = df[df['Exam_Score'] >= 85]

    # Sort by exam score (descending) and record id (ascending)
    sort_df = filtered_df.sort_values(by=['Exam_Score', 'Record_ID'], ascending=[False, True])

    result_df = sort_df[['Record_ID', 'Hours_Studied', 'Exam_Score']]

    result_df = result_df.head(10) # Write only the top 10 results

    return result_df



def task_3(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function for Task #3 that filters students with perfect attendance who participate in extracurricular activities.

        Parameters
        -------
        df (pd.DataFrame): Input DataFrame imported from the pandas library that contains data from our given dataset.

        Returns
        -------
        result_df: Variable that filters Record_ID and Exam_Score for students with 100% attendance and excurriculars. 
    """
    filtered_df = df[(df['Attendance'] == 100) & (df['Extracurricular_Activities'] == 'Yes')]
    
    # Selected columns in the dataset for output
    result_df = filtered_df[['Record_ID', 'Exam_Score']]
    
    return result_df



def task_4(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function for Task #4 that calculates the average attendance for each letter grade.

        Parameters
        -------
        df (pd.DataFrame): Input DataFrame imported from the pandas library that contains data from our given dataset.

        Returns
        -------
        result_df: Variable with the average attendance for each letter grade, sorted from highest (A+) 
        to lowest (D). F is included, but not printed.
    """

    def letter_grade(score: float) -> str:
        """
        Converts exam score to letter grade using UVic scale.

            Parameters
            -------
            score (float): Numerical exam score

            Returns
            -------
            str: Letter grade corresponding to a given score
        """
        if 90 <= score <= 101:
            return 'A+'
        elif 85 <= score <= 89:
            return 'A'
        elif 80 <= score <= 84:
            return 'A-'
        elif 77 <= score <= 79:
            return 'B+'
        elif 73 <= score <= 76:
            return 'B'
        elif 70 <= score <= 72:
            return 'B-'
        elif 65 <= score <= 69:
            return 'C+'
        elif 60 <= score <= 64:
            return 'C'
        elif 50 <= score <= 59:
            return 'D'
        else:
            return 'F'
    
    df['Grade'] = df['Exam_Score'].apply(letter_grade)

    # Group by grade and calculate mean attendance for each grade
    result_df = df.groupby('Grade')['Attendance'].mean().reset_index()

    result_df['Attendance'] = result_df['Attendance'].round(1)

    sort_grade = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D']

    result_df = result_df[result_df['Grade'].isin(sort_grade)]

    result_df = result_df.set_index('Grade').reindex(sort_grade).reset_index()

    return result_df
    


def task_5(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function that calculates the average number of tutoring sessions for each grade group.

        Parameters
        -------
        df (pd.DataFrame): Input DataFrame imported from the pandas library that contains data from our given dataset.

        Returns
        -------
        result_df: Variable that analyzes the number of tutoring sessions for the top 50 students (by exam score)
    """
    def secondary_grade_scale(score: float) -> str:
        """
        Converts exam score to a simplified letter grade (A-F), much like Task #4.

            Parameters
            -------
            score (float): Numerical exam score.

            Returns
            -------
            str: Simplified letter grades (A, B, C, D, F)
        """
        if 80 <= score <= 101:
            return 'A'
        elif 70 <= score <= 79:
            return 'B'
        elif 60 <= score <= 69:
            return 'C'
        elif 50 <= score <= 59:
            return 'D'
        else:
            return 'F'
    
    # Creates a copy of columns to not modify the initial dataframe - I was encountering errors. This was a quick fix.
    result_df = df[['Record_ID', 'Tutoring_Sessions', 'Exam_Score']].copy()

    result_df['Grade'] = df['Exam_Score'].apply(secondary_grade_scale)

    # Calculates average tutoring sessions per grade grouping
    grade_avg = df.groupby(df['Exam_Score'].apply(secondary_grade_scale))['Tutoring_Sessions'].mean().round(1)
    grade_avg_dict = grade_avg.to_dict()

    # Adds a column with grade average tutoring sessions
    result_df['Grade_Average_Tutoring_Sessions'] = result_df['Grade'].map(grade_avg_dict)
    result_df['Above_Average'] = result_df['Tutoring_Sessions'] > result_df['Grade_Average_Tutoring_Sessions']

    # Sets the column order
    result_df = result_df[['Record_ID', 'Tutoring_Sessions', 'Grade_Average_Tutoring_Sessions', 'Above_Average', 'Exam_Score', 'Grade']]
    result_df = result_df.sort_values(by=['Exam_Score', 'Record_ID'], ascending=[False, True])

    result_df = result_df.head(50) # Top 50 results

    return result_df


def write_output(df: pd.DataFrame, output_file: str = "output.csv") -> None:
     """
     Function that uses pandas DataFrame to generate a CSV file.

        Parameters:
        -------
        df(pd.DataFrame): DataFrame containing the given dataset to write to CSV.
        output_file (str, optional): Output file path that defaults to output.csv (as per instructions).
     """

     df.to_csv(output_file, index=False)



def parse_arguments() -> int:
    """
    Error-Handling function that parses command line arguments to extract the task number.

        Returns
        -------
        int: Task number from command line

        - Not entirely necessary, but good for covering all bases in case of errors (for debugging, primarily)
    """
    
    # Check if arguments were provided
    if len(sys.argv) < 2:
        print("Usage: python spf_analyzer.py --TASK=\"<task_number>\"")
        sys.exit(1)
        
    for arg in sys.argv[1:]:
        if arg.startswith("--TASK="):
            try:
                task_number = int(arg.split("=")[1].strip('"'))
                return task_number
            except ValueError:
                print("Error: Task number must be an integer")
                sys.exit(1)
    
    print("Error: --TASK argument not found")
    sys.exit(1)
               



def main():
    """
    Main entry point of the program.
    
        - Reads the dataset and executes the specified task in the command line.
        - Writes results into output.csv
        - Exits with error if an invalid task number is written
    """
   
    # Parse command line arguments for task number
    task_number = parse_arguments()

    # Load the given DataFrame and its dataset
    df = pd.read_csv("data/a2-data.csv")

    # Execute the requested task in command line
    if task_number == 1:
         result_df = task_1(df)
         write_output(result_df)
    elif task_number == 2:
         result_df = task_2(df)
         write_output(result_df)
    elif task_number ==3:
         result_df = task_3(df)
         write_output(result_df)
    elif task_number == 4:
         result_df = task_4(df)
         write_output(result_df)
    elif task_number == 5:
         result_df = task_5(df)
         write_output(result_df)
    else:
         print(f"Error: Compilation failed.")
         sys.exit(1)



if __name__ == '__main__':
    main()
