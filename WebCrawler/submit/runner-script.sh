#!/usr/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <LOCAL_INPUT_DIR> <HDFS_INPUT_DIR> <HDFS_OUTPUT_DIR>"
    exit 1
fi

chmod +x mapper_1.py
chmod +x reducer_1.py
chmod +x mapper_2.py
chmod +x reducer_2.py
chmod +x reducer_3.py
chmod +x library.mod


# Assign arguments to variables
LOCAL_INPUT=$1
HDFS_INPUT_DIR=$2
HDFS_OUTPUT_DIR=$3
HDFS_TEMP_DIR=helper


hadoop fs -rm -r "$HDFS_TEMP_DIR"

# Function to create HDFS directory if it doesn't exist
if ! hadoop fs -test -d "$HDFS_INPUT_DIR"; then
    printf "Creating HDFS_INPUT_FOLDER: $HDFS_INPUT_DIR"
    hadoop fs -mkdir -p "$HDFS_INPUT_DIR"
fi

# Upload local input files to HDFS input directory
hadoop fs -put "input.txt" "$HDFS_INPUT_DIR/"

# Specify the mapper and reducer scripts for the first stage
MAPPER_SCRIPT0=mapper_1.py
REDUCER_SCRIPT0=reducer_1.py
# Specify the mapper and reducer scripts for the second stage
MAPPER_SCRIPT1=mapper_2.py
REDUCER_SCRIPT1=reducer_2.py

# Specify the mapper and reducer scripts for the third stage
MAPPER_SCRIPT2=mapper_2.py
REDUCER_SCRIPT2=reducer_3.py

# Take the input from input.txt
input_0="input.txt"

# Create a new file to store modified input
output_file="input_0.txt"
hadoop fs -put "input_0.txt" "$HDFS_INPUT_DIR/"

# Read input.txt line by line
while IFS= read -r line || [ -n "$line" ]; do
    # Split the line into URL and depth
    url=$(echo "$line" | cut -d' ' -f1)
    depth=$(echo "$line" | cut -d' ' -f2)
    # Output the URL and depth (you can replace this with your desired actions)
    echo "URL: $url, Depth: $depth"
    # Store the depth value in a variable if needed for further processing

    # Split the line into URL and depth again for the second loop
    urll=$(echo "$line" | cut -d' ' -f1)
    
    # Write URL and depth 0 to the new file
    echo "$urll 0" >> "$output_file"
done < "$input_0"
depth=$(expr $depth + 0)
# print type of depth
i=1
while [ "$i" -le $depth ]; do

    mapred streaming \
        -files "mapper_1.py,reducer_1.py,library.mod,requests.mod" \
        -input "$HDFS_INPUT_DIR/input_$((i-1)).txt" \
        -output "$HDFS_TEMP_DIR/output_$i" \
        -mapper "mapper_1.py" \
        -reducer "reducer_1.py" \
        -numReduceTasks 3

    mapred streaming \
        -files "mapper_2.py,reducer_2.py" \
        -input "$HDFS_TEMP_DIR/output_$i" \
        -output "$HDFS_INPUT_DIR/input_$i.txt" \
        -mapper "mapper_2.py" \
        -reducer "reducer_2.py" \
        -numReduceTasks 3

    mapred streaming \
        -files "mapper_2.py,reducer_3.py" \
        -input "$HDFS_INPUT_DIR/input_$i.txt" \
        -output "$HDFS_TEMP_DIR/outputt_$i" \
        -mapper "mapper_2.py" \
        -reducer "reducer_3.py" \
        -numReduceTasks 3
    i=$(( i + 1 ))
done


# Remove all folders with names output_i from hdfs_temp_dir
hadoop fs -rm -r "$HDFS_TEMP_DIR/output_[1-9]*"

# Iterate through the desired depth (you'll need to set this value)
for ((i=1; i<=depth; i++)); do
    # Iterate through files in output_i
    for file in $(hadoop fs -ls "$HDFS_TEMP_DIR/outputt_$i" | awk '{print $8}'); do
        # Extract the file name
        filename=$(basename "$file")
        # Create a new file name by appending folder name and file name
        if [[ "$filename" != "_SUCCESS" ]]; then
            # Create a new file name by appending folder name and file name
            new_filename="output${i}_$filename"
            # Copy the file to the helper directory
            hadoop fs -cp "$file" "$HDFS_TEMP_DIR/$new_filename"
        fi
    done
    # Remove original output_i folder
    hadoop fs -rm -r "$HDFS_TEMP_DIR/outputt_$i"
done
HDFS_FINAL_OUTPUT_DIR=finall
mapred streaming \
    -files "mapper_4.py,reducer_4.py" \
    -input "$HDFS_TEMP_DIR" \
    -output "$HDFS_FINAL_OUTPUT_DIR" \
    -mapper "mapper_4.py" \
    -reducer "reducer_4.py" \
    -numReduceTasks 3

# Concatenate the output files and save to main_out.txt
# hdfs dfs -cat "/outputt_*/p*" > main_out.txt
# hdfs dfs -rm -r "$HDFS_TEMP_DIR"
# hdfs dfs -rm -r "$HDFS_INPUT_DIR"