import os
import subprocess
import json
import tempfile

# Paths to executable and model
biocheck_console_path = r"C:\Program Files (x86)\BMA\BioCheckConsole.exe.config"  # Update if needed

model_path = r"C:\Users\bancu\Downloads\CancerSignalling.json"

# Temporary folder for KO models and results
output_folder = tempfile.mkdtemp()

def extract_variables_from_model(model_path):
    """Extracts variable names and IDs from the model."""
    with open(model_path, "r") as file:
        model_data = json.load(file)
    return [{"Name": var["Name"], "Id": var["Id"]} for var in model_data["Model"]["Variables"]]

def create_ko_model(original_model_path, variable_id, output_folder):
    """Creates a modified model with a specific variable knocked out."""
    with open(original_model_path, "r") as file:
        model_data = json.load(file)

    # Set the variable's formula to 0 to simulate knockout
    for variable in model_data["Model"]["Variables"]:
        if variable["Id"] == variable_id:
            variable["RangeFrom"] = 0  # Set RangeFrom to 0
            variable["RangeTo"] = 0    # Set RangeTo to 0
            variable["Formula"] = 0  # Knockout by forcing the value to 0

    # Save the modified model
    modified_model_path = os.path.join(output_folder, f"KO_{variable_id}.json")
    with open(modified_model_path, "w") as file:
        json.dump(model_data, file, indent=4)
    return modified_model_path

def run_biocheck(modified_model_path, result_path):
    """Runs BioCheckConsole with the modified model."""
    command = f'"{biocheck_console_path}" -model "{modified_model_path}" -engine VMCAI -prove "{result_path}"'
    #subprocess.run(command, shell=True, check=True)
    subprocess.run(["BioCheckConsole.exe", "-engine VMCAI -prove"])

    # Print the contents of the output JSON file
    if os.path.exists(result_path):
        with open(result_path, "r") as file:
            output_data = json.load(file)
            print(f"Contents of {result_path}:")
            print(json.dumps(output_data, indent=4))  # Pretty-print the JSON content
    else:
        print(f"Error: Output file {result_path} was not created.")

def main():
    # Extract variables from the original model
    variables = extract_variables_from_model(model_path)
    print("Variables in the model:", [var["Name"] for var in variables])

    # Process each variable for knockout
    for var in variables:
        print(f"Knocking out variable: {var['Name']} (Id: {var['Id']})")

        # Create KO model
        modified_model_path = create_ko_model(model_path, var["Id"], output_folder)

        # Define result path
        result_path = os.path.join(output_folder, f"KO_{var['Id']}_output.json")

        # Run the command
        try:
            run_biocheck(modified_model_path, result_path)
            print(f"Result saved to: {result_path}")

        except subprocess.CalledProcessError as e:
            print(f"Error running BioCheckConsole for {var['Name']}: {e}")

    print(f"All knockouts processed. Results are stored in: {output_folder}")

if __name__ == "__main__":
    main()
