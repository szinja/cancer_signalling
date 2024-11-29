import os
import json
import pandas as pd

# Path to the directory containing the output JSON files
output_dir = r"C:\Users\bancu\Downloads\outputs"  # Update to your path

def summarize_variable_changes(output_dir):
    """Summarizes variable changes across all output files in numerical order."""
    # List and sort files numerically by extracting the number from the filename
    files = sorted(
        [f for f in os.listdir(output_dir) if f.startswith("output_") and f.endswith(".json")],
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )
    variable_states = {}

    for file in files:
        file_path = os.path.join(output_dir, file)
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # Get variable states from the last tick
        if "Ticks" in data:
            last_tick = data["Ticks"][-1]
            for var in last_tick["Variables"]:
                var_id = var["Id"]
                if var_id not in variable_states:
                    variable_states[var_id] = {}
                variable_states[var_id][file] = (var["Lo"], var["Hi"])
    
    # Convert to a DataFrame for better visualization
    df = pd.DataFrame(variable_states).T
    df.index.name = "Variable ID"
    return df

if __name__ == "__main__":
    summary = summarize_variable_changes(output_dir)
    print(summary)
    # Save to a CSV file for detailed analysis
    summary.to_csv(os.path.join(output_dir, "variable_changes_summary1.csv"))
    print("Summary saved to variable_changes_summary.csv")
