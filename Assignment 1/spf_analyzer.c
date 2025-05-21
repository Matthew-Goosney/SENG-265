/**
 * Name: Matthew Goosney
 * V-Number: V01040408
 * Date: February 13th, 2025
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RECORDS 6608

/**
 * Struct: CurricularData
 * ----------------------
 * @brief Represents a row from the a1-data-curricular.csv file.
 */
typedef struct
{
    int record_id;         // Maps to the "Record_ID" column
    int hours_studied;     // Maps to the "Hours_Studied" column
    int attendance;        // Maps to the "Attendance" column
    int tutoring_sessions; // Maps to the "Tutoring_Sessions" column
    int exam_score;        // Maps to the "Exam_Score" column
} CurricularData;

/**
 * Struct: ExtracurricularData
 * ----------------------
 * @brief Represents a row from the a1-data-extracurricular.yaml file.
 */
typedef struct
{
    int extracurricular_activities; // Maps to the Extracurricular_Activities column
    int physical_activity;          // Maps to the Physical_Activity column
    int record_id;                  // Maps to the Record_ID column
    int sleep_hours;                // Maps to the Sleep_Hours column
} ExtracurricularData;

/**
 * Struct: MegedData
 * ----------------------
 * @brief A struct used to combine the different parameters from both the yaml and csv dataset files
 */
typedef struct
{
    int record_id;                  // Maps to the  Record_ID column
    int hours_studied;              // Maps to the Hours_Studied column
    int attendance;                 // Maps to the Attendance column
    int tutoring_sessions;          // Maps to the Tutoring_Sessions column
    int exam_score;                 // Maps to the Exam_Score column
    int extracurricular_activities; // Maps to the Extracurricular_Activities column
    int physical_activity;          // Maps to the Physical_Activity column
    int sleep_hours;                // Maps to the Sleep_Hours column
} MergedData;

/**
 * Function: read_csv_file
 * -----------------------
 * @brief Reads data from the a1-data-curricular.csv file and populates an array of CurricularData structs.
 *
 * @param filename The name of the CSV file to read.
 * @param data Array of CurricularData where the CSV data will be stored.
 * @return int The number of records successfully read.
 */
int read_csv_file(const char *filename, CurricularData data[])
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        printf("Error: Could not open file %s\n", filename);
        return -1;
    }

    // Skip the header line
    char buffer[256];
    fgets(buffer, sizeof(buffer), file);

    int index = 0;
    while (fgets(buffer, sizeof(buffer), file) != NULL && index < MAX_RECORDS)
    {
        sscanf(buffer, "%d,%d,%d,%d,%d",
               &data[index].record_id,
               &data[index].hours_studied,
               &data[index].attendance,
               &data[index].tutoring_sessions,
               &data[index].exam_score);
        index++;
    }

    fclose(file);
    return index;
}

/**
 * Function: read_yaml_file
 * -----------------------
 * @brief Reads data from the a1-data-extracurricular.yaml file and populates an array of ExtracurricularData structs.
 *
 * @param filename The name of the YAML file to read.
 * @param data Array of ExtracurricularData where the YAML data will be stored.
 * @return int The number of records successfully read.
 */
int read_yaml_file(const char *filename, ExtracurricularData data[])
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        printf("Error: Could not open file %s\n", filename);
        return -1;
    }

    char buffer[256];
    int index = -1; // Index that skips the very first line
    while (fgets(buffer, sizeof(buffer), file))
    {
        // Buffer to remove trailing with every new line
        buffer[strcspn(buffer, "\n")] = 0;

        if (buffer[0] == '-')
        {
            index++;
        }

        // Buffer to remove leading spaces
        char *trimmed = buffer;
        while (*trimmed == ' ')
            trimmed++;

        char key[256], value[256];

        if (sscanf(trimmed, "%[^:]: %[^\n]", key, value) == 2)
        {
            if (strcmp(key, "- Extracurricular_Activities") == 0)
            {
                if (strcmp(value, "'Yes'") == 0)
                {
                    data[index].extracurricular_activities = 1;
                }
                else if (strcmp(value, "'No'") == 0)
                {
                    data[index].extracurricular_activities = 0;
                }
            }
            else if (strcmp(key, "Physical_Activity") == 0)
            {
                data[index].physical_activity = atoi(value);
            }
            else if (strcmp(key, "Record_ID") == 0)
            {
                data[index].record_id = atoi(value);
            }
            else if (strcmp(key, "Sleep_Hours") == 0)
            {
                data[index].sleep_hours = atoi(value);
            }
        }
    }

    fclose(file);
    return index + 1;
}

/**
 * Function: merge_csv
 * -----------------------
 * @brief File that merges the two given datasets together - required for tasks 2, 3, and 6
 *
 * @param csvData Array that holds the information from our curricular dataset
 * @param num_csv int variable that holds the size of the csv dataset
 * @param yamlData Array that holds the information from our extracurricular dataset
 * @param num_yaml int variable that holds the size of the yaml dataset
 * @param merged Array that merges the information from our curricular AND extracurricular datasets
 * @param task int variable used in the if-clause to determine which task from the main method is being performed
 */
int merge_csv(const CurricularData csvData[], int num_csv, const ExtracurricularData yamlData[], int num_yaml, MergedData merged[], int task)
{
    int count = 0;
    for (int i = 0; i < num_csv; i++)
    {
        if (task == 3 && csvData[i].exam_score <= 90)
        {
            continue;
        }
        for (int j = 0; j < num_yaml; j++)
        {
            if (csvData[i].record_id == yamlData[j].record_id)
            {
                merged[count].record_id = csvData[i].record_id;
                merged[count].hours_studied = csvData[i].hours_studied;
                merged[count].attendance = csvData[i].attendance;
                merged[count].tutoring_sessions = csvData[i].tutoring_sessions;
                merged[count].exam_score = csvData[i].exam_score;
                merged[count].extracurricular_activities = yamlData[j].extracurricular_activities;
                merged[count].physical_activity = yamlData[j].physical_activity;
                merged[count].sleep_hours = yamlData[j].sleep_hours;
                count++;
                break;
            }
        }
    }
    return count;
}

/**
 * Function: low_score_output
 * -----------------------
 * @brief Output function used exclusively for task 6
 *
 * @param filename name of the csv file to be generated
 * @param data Array of merged data from the curricular and extracurricular datasets
 * @param size holds the size of the merged array
 */
int low_score_output(const char *filename, const MergedData data[], int size)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        printf("Error: Could not open file %s\n", filename);
        return -1;
    }

    fprintf(file, "Record_ID,Exam_Score,Extracurricular_Activities\n");

    for (int i = 0; i < size; i++)
    {
        if (data[i].exam_score < 60)
        {
            fprintf(file, "%d,%d,%s\n",
                    data[i].record_id,
                    data[i].exam_score,
                    data[i].extracurricular_activities == 1 ? "Yes" : "No");
        }
    }
    fclose(file);
    return 0;
}

/**
 * Function: merged_hours_output
 * -----------------------
 * @brief Output function used exclusively for task 5
 *
 * @param filename name of the csv file to be generated
 * @param merged_data Array of the merged data from the curricular and extracurricular datasets
 * @param cur_extr_merged variable that holds the size of the merged datasets
 */
int merged_hours_output(const char *filename, const MergedData merged_data[], int cur_extr_merged)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        printf("Error: Could not open file %s\n", filename);
        return -1;
    }

    fprintf(file, "Record_ID,Exam_Score\n");

    for (int i = 0; i < cur_extr_merged; i++)
    {
        if (merged_data[i].sleep_hours >= merged_data[i].hours_studied)
        {
            fprintf(file, "%d,%d\n",
                    merged_data[i].record_id,
                    merged_data[i].exam_score);
        }
    }
    fclose(file);
    return 0;
}

/**
 * Function: merged_csv_output
 * -----------------------
 * @brief Output function used exclusively for task 3
 *
 * @param filename name of the csv file to be generated
 * @param data Array of the merged data from curricular and extracurricular datasets
 * @param size variable that holds the size of the merged datasets
 */
int merged_csv_output(const char *filename, const MergedData data[], int size)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        printf("Error: Could not open file %s\n", filename);
        return -1;
    }

    // Header
    fprintf(file, "Record_ID,Hours_Studied,Attendance,Tutoring_Sessions,Exam_Score,Extracurricular_Activities,Physical_Activity,Sleep_Hours\n");

    for (int i = 0; i < size; i++)
    {

        // If-Else clause to determine whether Extracurricular_Activity will print "Yes" or "No"
        if (data[i].extracurricular_activities == 1)
        {
            fprintf(file, "%d,%d,%d,%d,%d,%s,%d,%d\n",
                    data[i].record_id,
                    data[i].hours_studied,
                    data[i].attendance,
                    data[i].tutoring_sessions,
                    data[i].exam_score,
                    "Yes",
                    data[i].physical_activity,
                    data[i].sleep_hours);
        }
        else
        {
            fprintf(file, "%d,%d,%d,%d,%d,%s,%d,%d\n",
                    data[i].record_id,
                    data[i].hours_studied,
                    data[i].attendance,
                    data[i].tutoring_sessions,
                    data[i].exam_score,
                    "No",
                    data[i].physical_activity,
                    data[i].sleep_hours);
        }
    }
    fclose(file);
    return 0;
}

/**
 * Function: write_csv_output
 * --------------------
 * @brief Outputs data for a CSV file - Tied specifically to Task #1 & #4
 *
 * @param filename The name of the csv file to read
 * @param size The number of records in the array
 */

int write_csv_output(const char *filename, const CurricularData data[], int size)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        printf("Error: Could not open file %s\n", filename);
        return -1;
    }

    fprintf(file, "Record_ID,Exam_Score\n");
    for (int i = 0; i < size; i++)
    {
        fprintf(file, "%d,%d\n", data[i].record_id, data[i].exam_score);
    }
    fclose(file);
    return 0;
}

/**
 * Function: extracurricular_csv_output
 * --------------------
 * @brief Creates output for Task #2 - works almost identically to the write_csv_output method, only with the addition of an if-else clause.
 *
 * @param filename The name of the csv file to read
 * @param size The number of records in the array
 * @param data Array that holds the data tied to our extracurricular dataset
 */
int extracurricular_csv_output(const char *filename, const ExtracurricularData data[], int size)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        printf("Error: Could not open file %s\n", filename);
        return -1;
    }

    // Header print statement
    fprintf(file, "Extracurricular_Activities,Physical_Activity,Record_ID,Sleep_Hours\n");

    // If-Else clause designed to transform the 0-1 value of Extracurricular_activities to a "Yes" or "No" statement.
    for (int i = 0; i < size; i++)
    {
        if (data[i].extracurricular_activities == 1)
        {
            fprintf(file, "%s,%d,%d,%d\n",
                    "Yes",
                    data[i].physical_activity,
                    data[i].record_id,
                    data[i].sleep_hours);
        }
        else
        {
            fprintf(file, "%s,%d,%d,%d\n",
                    "No",
                    data[i].physical_activity,
                    data[i].record_id,
                    data[i].sleep_hours);
        }
    }
    fclose(file);
    return 0;
}

/**
 * Function: main
 * --------------
 * @brief The main function and entry point of the program.
 *
 * @return int 0: No errors; 1: Errors produced.
 */
int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        return 1;
    }

    int task = -1;
    for (int i = 1; i < argc; i++)
    {
        if (strncmp(argv[i], "--TASK=", 7) == 0)
        {
            sscanf(argv[i] + 7, "%d", &task);
            break;
        }
    }

    // Task 1 & 4 only requires access to the curricular dataset
    CurricularData curricular_data[MAX_RECORDS];
    const char *curricular_filename = "data/a1-data-curricular.csv";
    int num_curricular_record = read_csv_file(curricular_filename, curricular_data);
    if (num_curricular_record < 0)
    {
        return 1; // Error handling
    }

    if (task == 1) // First task
    {
        CurricularData output_data[MAX_RECORDS];
        int output_index = 0;
        for (int i = 0; i < num_curricular_record; i++)
        {
            if (curricular_data[i].exam_score > 90)
            {
                output_data[output_index++] = curricular_data[i];
            }
        }
        return write_csv_output("output.csv", output_data, output_index);
    }

    if (task == 4) // Fourth task
    {
        CurricularData output_max_at[MAX_RECORDS];
        int at_index = 0;
        for (int i = 0; i < num_curricular_record; i++)
        {
            if (curricular_data[i].attendance == 100)
            {
                output_max_at[at_index++] = curricular_data[i];
            }
        }
        return write_csv_output("output.csv", output_max_at, at_index);
    }

    // Task 2 requires only access to the YAML dataset
    ExtracurricularData extracurricular_data[MAX_RECORDS];
    const char *extracurricular_filename = "data/a1-data-extracurricular.yaml";
    int num_extracurricular_record = read_yaml_file(extracurricular_filename, extracurricular_data);
    if (num_extracurricular_record < 0)
    {
        return 1;
    }

    if (task == 2) // Second task
    {
        return extracurricular_csv_output("output.csv", extracurricular_data, num_extracurricular_record);
    }

    // Task 3, 5, and 6 require access to both the curricular and extracurricular datasets, as well as this merge function
    MergedData merged_data[MAX_RECORDS];
    int num_merged = merge_csv(curricular_data, num_curricular_record, extracurricular_data, num_extracurricular_record,
                               merged_data, task);

    if (task == 3) // Third task
    {
        return merged_csv_output("output.csv", merged_data, num_merged);
    }

    if (task == 5) // Fifth task
    {
        return merged_hours_output("output.csv", merged_data, num_merged);
    }

    if (task == 6) // Sixth task
    {
        return low_score_output("output.csv", merged_data, num_merged);
    }

    return 0;
}
