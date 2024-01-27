# ImageLabelingPipeline

## Overview
This repository contains the ImageLabelingPipeline project, developed for an MLOps class at our university. The project consists of an application designed to help in labeling images in a dataset for machine learning.

## Object Detection
Due to resource constraints, the project's focus is the manual labeling of data and creation of utilities to support machine learning operations rather than training a complex model.

## Installation
Prerequisites:
- Python 3.x
- Flask
- cleanvision package

Clone the repository and navigate to the project directory. Install the required packages using the requirements.txt file provided:
```bash
pip install -r requirements.txt
```

## Usage
1. Start the Flask app:
```bash
python app.py
```
2. Access the application through your web browser at `localhost:5001`.
3. Use the web interface to upload images for annotation.
4. Run `clean_analysis.py` to analyze the uploads for any unsuitable images using CleanVision.

## Tools Utilized
- **CleanVision**: for dataset analysis and image selection.
- **DVC**: for data version control (not integrated in the given code).

## Project Structure
- `app.py`: The Flask application's main entry point.
- `static/`: Contains CSS and JS files for the front-end.
- `templates/`: HTML templates for rendering the web interface.
- `clean_analysis.py`: A script to analyze and report issues in the uploaded images.

## Contribution
Contributions to the project are welcome. Please ensure proper testing and documentation for any submitted features or bug fixes.

## License
The project is open-sourced under the MIT license.
