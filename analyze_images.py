from cleanvision import Imagelab


def analyze_images(upload_folder):
    imagelab = Imagelab(data_path=upload_folder)
    imagelab.find_issues()
    issues_data = imagelab.issues.__deepcopy__()
    issues_data["path"] = imagelab.issues.index
    return issues_data
