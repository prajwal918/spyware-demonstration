# Setup Instructions for Python Keylogger

## Step 1: Install Python

### Option 1: Download from python.org (Recommended)
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.11.x" (latest stable version)
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Complete the installation

### Option 2: Using Microsoft Store
1. Open Microsoft Store
2. Search for "Python 3.11"
3. Click Install

## Step 2: Verify Python Installation
Open a new PowerShell window and run:
```powershell
python --version
```

## Step 3: Install Required Libraries
Once Python is installed, navigate to your Downloads folder and run:

```powershell
cd "C:\Users\PRAJWAL JOGI\Downloads"
python -m pip install -r requirements.txt
```

## Step 4: Alternative Manual Installation
If the requirements.txt method doesn't work, install each library individually:

```powershell
python -m pip install pywin32==306
python -m pip install sounddevice==0.4.6
python -m pip install scipy==1.11.4
python -m pip install pyscreenshot==3.1
python -m pip install opencv-python==4.8.1.78
python -m pip install pynput==1.7.6
python -m pip install psutil==5.9.6
```

## Step 5: Test the Installation
Run your Python script:
```powershell
python kiran.py
```

## Troubleshooting

### If "python is not recognized":
1. Restart PowerShell after Python installation
2. Check if Python was added to PATH
3. Try using `py` instead of `python`

### If pip installation fails:
1. Update pip: `python -m pip install --upgrade pip`
2. Try installing with `--user` flag: `python -m pip install --user package_name`

### If specific packages fail:
- Some packages may require Visual C++ build tools
- Try installing pre-compiled wheels when available

## Note
This code appears to be a keylogger application. Please ensure you have proper authorization before using it on any system, as unauthorized keylogging may be illegal in many jurisdictions.
