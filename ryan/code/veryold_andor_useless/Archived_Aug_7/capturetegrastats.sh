#!/bin/bash

output_file="tegdata.json"
interval=5  # Adjust the interval as needed

# Check if output file exists, if not, create it with an empty array
if [ ! -f "$output_file" ]; then
    echo "[]" > "$output_file"
fi

# Function to capture and append tegrastats data to JSON file
append_tegrastats_to_json() {
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    tegrastats_data=$(tegrastats | head -n 1)

    if [ -z "$tegrastats_data" ]; then
        echo "Error: tegrastats command failed to fetch data."
        return 1
    fi

    # Parse raw tegrastats data into structured JSON
    ram=$(echo "$tegrastats_data" | grep -o 'RAM [0-9/]*MB' | cut -d' ' -f2)
    swap=$(echo "$tegrastats_data" | grep -o 'SWAP [0-9/]*MB' | cut -d' ' -f2)
    cpu=$(echo "$tegrastats_data" | grep -o 'CPU \[.*\]' | sed 's/CPU \[\(.*\)\]/\1/')
    emc_freq=$(echo "$tegrastats_data" | grep -o 'EMC_FREQ [0-9]*%' | cut -d' ' -f2 | tr -d '%')
    gr3d_freq=$(echo "$tegrastats_data" | grep -o 'GR3D_FREQ [0-9]*%' | cut -d' ' -f2 | tr -d '%')
    ao_temp=$(echo "$tegrastats_data" | grep -o 'AO@[0-9.]*C' | cut -d'@' -f2 | cut -d'C' -f1)
    gpu_temp=$(echo "$tegrastats_data" | grep -o 'GPU@[0-9.]*C' | cut -d'@' -f2 | cut -d'C' -f1)
    iwlwifi_temp=$(echo "$tegrastats_data" | grep -o 'iwlwifi@[0-9.]*C' | cut -d'@' -f2 | cut -d'C' -f1)
    pmic_temp=$(echo "$tegrastats_data" | grep -o 'PMIC@[0-9.]*C' | cut -d'@' -f2 | cut -d'C' -f1)
    aux_temp=$(echo "$tegrastats_data" | grep -o 'AUX@[0-9.]*C' | cut -d'@' -f2 | cut -d'C' -f1)
    cpu_temp=$(echo "$tegrastats_data" | grep -o 'CPU@[0-9.]*C' | cut -d'@' -f2 | cut -d'C' -f1)
    thermal_temp=$(echo "$tegrastats_data" | grep -o 'thermal@[0-9.]*C' | cut -d'@' -f2 | cut -d'C' -f1)
    vdd_in=$(echo "$tegrastats_data" | grep -o 'VDD_IN [0-9/]*/[0-9]*' | cut -d' ' -f2)
    vdd_cpu_gpu_cv=$(echo "$tegrastats_data" | grep -o 'VDD_CPU_GPU_CV [0-9/]*/[0-9]*' | cut -d' ' -f2)
    vdd_soc=$(echo "$tegrastats_data" | grep -o 'VDD_SOC [0-9/]*/[0-9]*' | cut -d' ' -f2)

    # Construct JSON object
    json_data='{
        "timestamp": "'"$timestamp"'",
        "RAM": "'"$ram"'",
        "SWAP": "'"$swap"'",
        "CPU": "'"$cpu"'",
        "EMC_FREQ": "'"$emc_freq"'%",
        "GR3D_FREQ": "'"$gr3d_freq"'%",
        "AO_TEMP": "'"$ao_temp"'C",
        "GPU_TEMP": "'"$gpu_temp"'C",
        "IWIFI_TEMP": "'"$iwlwifi_temp"'C",
        "PMIC_TEMP": "'"$pmic_temp"'C",
        "AUX_TEMP": "'"$aux_temp"'C",
        "CPU_TEMP": "'"$cpu_temp"'C",
        "THERMAL_TEMP": "'"$thermal_temp"'C",
        "VDD_IN": "'"$vdd_in"'",
        "VDD_CPU_GPU_CV": "'"$vdd_cpu_gpu_cv"'",
        "VDD_SOC": "'"$vdd_soc"'"
    }'

    # Append to JSON file
    echo "$(jq --argjson new_data "$json_data" '. += [$new_data]' "$output_file")" > "$output_file"

    # Print debug message
    echo "Captured tegrastats data at $timestamp and appended to $output_file"
}

# Debugging message for script start
echo "Script started"

# Run append_tegrastats_to_json function once initially
append_tegrastats_to_json

# Continuously capture and append tegrastats data at intervals
while true; do
    sleep "$interval"
    append_tegrastats_to_json
done

