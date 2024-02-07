### Deploying the `magpie.py` Script: A User Manual

== Notice: This manual was written by GPT-4 ==

This manual provides step-by-step instructions for deploying the `magpie.py` Python script on both Windows and MacOS. This script requires Python 3 and specific libraries to run correctly. The ZIP file you've received contains the script itself, a configuration file (`config.yaml`), and placeholder folders for inputs and outputs.

#### General Preparation
Before diving into platform-specific instructions, ensure you've downloaded the ZIP file containing `magpie.py`, `config.yaml`, and the folders `Inputs` and `Outputs`.

---

### Windows Users

#### 1. Install Python 3
- Visit the [official Python website](https://www.python.org/downloads/) and download the latest version of Python 3 for Windows.
- Run the installer. Ensure to check the box that says **Add Python 3.x to PATH** before clicking **Install Now**.

#### 2. Install Required Libraries
- Open Command Prompt.
- Install the necessary libraries by running the following command:
  ```
  python3 -m pip install Pillow yaml
  ```
  Note: `os` and `random` are part of the standard library, so you don't need to install them separately.

#### 3. Unzip the Script Files
- Navigate to the location of the downloaded ZIP file.
- Right-click the ZIP file and select **Extract All...**.
- Choose the destination for the extracted files and click **Extract**.

#### 4. Customize Configuration (Optional)
- Navigate to the extracted folder.
- Find `config.yaml` and right-click it.
- Choose **Open with** and select a text editor (e.g., Notepad) to edit your preferences.

#### 5. Prepare Your Input Images
- Place any images you wish to process in the `Inputs` folder within the extracted folder.

#### 6. Run the Script
- Shift-right-click the folder where `magpie.py` is located and select **Open PowerShell window here**.
- Run the script by typing:
  ```
  python3 magpie.py
  ```

---

### MacOS Users

#### 1. Install Python 3
- Visit the [official Python website](https://www.python.org/downloads/) and download the latest version of Python 3 for MacOS.
- Open the downloaded `.pkg` file and follow the installation instructions.

#### 2. Install Required Libraries
- Open Terminal.
- Install the necessary libraries by running the following command:
  ```
  python3 -m pip install Pillow yaml
  ```
  Note: `os` and `random` are part of the standard library, so you don't need to install them separately.

#### 3. Unzip the Script Files
- Locate the downloaded ZIP file in Finder.
- Double-click the ZIP file to extract its contents to a new folder.

#### 4. Customize Configuration (Optional)
- Navigate to the extracted folder using Finder.
- Right-click `config.yaml` and choose **Open With > TextEdit** (or your preferred text editor) to edit your preferences.

#### 5. Prepare Your Input Images
- Place any images you wish to process in the `Inputs` folder within the extracted folder.

#### 6. Run the Script
- In Finder, navigate to the folder where `magpie.py` is located.
- Right-click (or Ctrl + click) on the folder and select **New Terminal at Folder** from the context menu. This opens a Terminal window already set to the folder's path.
- In the Terminal window that opens, run the script by typing:
  ```
  python3 magpie.py
  ```

---

### Conclusion
After following these steps, your script should be up and running. If you encounter any issues, ensure Python 3 and all required libraries are correctly installed, and the script and configuration files are in the correct folders.
