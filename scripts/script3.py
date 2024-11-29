import os
import json

# Path to the directory containing the output JSON files
output_dir = r"C:\Users\bancu\Downloads\outputs"  # Update to your path

def check_stabilization_and_compare(output_dir):
    """Checks stabilization and compares variable values across output files."""
    files = [f for f in os.listdir(output_dir) if f.endswith(".json")]
    stabilization_status = {}
    variable_states = {}

    for file in files:
        file_path = os.path.join(output_dir, file)
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # Check stabilization status
        status = data.get("Status", "Unknown")
        stabilization_status[file] = status

        # Get variable states from the last tick
        if "Ticks" in data:
            last_tick = data["Ticks"][-1]  # Get the last tick
            variables = {var["Id"]: (var["Lo"], var["Hi"]) for var in last_tick["Variables"]}
            variable_states[file] = variables
    
    # Print stabilization statuses
    print("\nStabilization Statuses:")
    for file, status in stabilization_status.items():
        print(f"{file}: {status}")

    # Compare variable states across files
    print("\nVariable Differences Across Files:")
    all_ids = set().union(*[vars.keys() for vars in variable_states.values()])
    for var_id in all_ids:
        values = {file: vars.get(var_id, "Missing") for file, vars in variable_states.items()}
        unique_values = set(values.values())
        if len(unique_values) > 1:  # If there's a difference
            print(f"Variable {var_id}:")
            for file, value in values.items():
                print(f"  {file}: {value}")

if __name__ == "__main__":
    check_stabilization_and_compare(output_dir)
