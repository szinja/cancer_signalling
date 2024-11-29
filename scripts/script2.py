import os
import subprocess
import json

# Paths to BioCheckConsole executable and KO files directory
biocheck_console_path = r"C:\Program Files (x86)\BMA\BioCheckConsole.exe"  # Update to correct path
ko_files_dir = r"C:\Users\bancu\AppData\Local\Temp\tmprb6q7iqe"  # Update to the directory containing KO files
output_dir = r"C:\Users\bancu\Downloads\outputs"  # Directory to save the output files

def run_biocheck_for_kos():
    """Run BioCheckConsole for each KO file and save the outputs."""
    # Get all KO files in the directory
    ko_files = [f for f in os.listdir(ko_files_dir) if f.startswith("KO_") and f.endswith(".json")]
    
    for ko_file in ko_files:
        # Construct the full paths for the KO file and the output file
        ko_file_path = os.path.join(ko_files_dir, ko_file)
        output_file_name = f"output_{ko_file.split('_')[1].split('.')[0]}.json"
        output_file_path = os.path.join(output_dir, output_file_name)
        
        # Build the command
        command = [
            biocheck_console_path,
            "-model", ko_file_path,
            "-engine", "VMCAI",
            "-prove", output_file_path
        ]
        
        # Run the command
        try:
            print(f"Running command for {ko_file}:")
            print(" ".join(command))  # Print command for debugging
            subprocess.run(command, check=True)
            print(f"Output saved to: {output_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error running BioCheckConsole for {ko_file}: {e}")
        
if __name__ == "__main__":
    run_biocheck_for_kos()
