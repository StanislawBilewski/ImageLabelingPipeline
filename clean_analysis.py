import subprocess
import os
from analyze_images import analyze_images


UPLOAD_FOLDER = "uploads"


# Initialize DVC repository if not already done
def init_dvc():
    if not os.path.isdir('.dvc'):
        subprocess.run(["dvc", "init"], check=True)
        subprocess.run(["git", "commit", "-m", "Initialize DVC"], check=True)


def remove_images_and_dvc_commit(data_frame):
    issues_columns = [col for col in data_frame.columns if "issue" in col]
    removed_files = []
    
    for index, row in data_frame.iterrows():
        if any(row[issues_column] for issues_column in issues_columns):
            file_path = row["path"]
            if os.path.exists(file_path):
                os.remove(file_path)
                removed_files.append(file_path)

    if removed_files:
        try:
            subprocess.run(["dvc", "add", UPLOAD_FOLDER], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print("Output:", e.output)
            print("Error :", e.stderr)

        subprocess.run(["git", "add",  "uploads.dvc"], check=True) #UPLOAD_FOLDER +

        commit_message = f"Removed {len(removed_files)} unwanted images"
        try:
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
        except subprocess.CalledProcessError as e:
            print("Output:", e.output)
            print("Error :", e.stderr)

        # Pushing to remote DVC storage is not mandatory in local testing
        # subprocess.run(["dvc", "push"], check=True)

    return removed_files


if __name__ == "__main__":
    init_dvc()  # Ensure DVC repository is initialized
    issues_data_frame = analyze_images(UPLOAD_FOLDER)
    if not issues_data_frame.empty:
        removed_files = remove_images_and_dvc_commit(issues_data_frame)
        print("Removed files:", removed_files)
    else:
        print("No issues found. No files removed.")
