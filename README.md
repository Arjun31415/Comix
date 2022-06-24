# Comix

Qt Application to view your comics on desktop.

# Contents:

- [Features](#features)
- [ScreenShots](#screenshots)
- [Installation](#installation)
- [Customization](#customization)
- [Known Issues](#known-issues)

## Features

- Currently supports [xkcd](https://xkcd.com/) and [Dilbert](https://dilbert.com/)
- Appears in a floating window in window managers such as i3 and bspwm.
- Double click on comic will open it in web browser.
- Scrollable area for image.

## ScreenShots

![image](https://user-images.githubusercontent.com/72289243/175564605-6704930e-101e-44df-83cb-012d40141187.png)

![image](https://user-images.githubusercontent.com/72289243/175564681-60e6e300-900a-4f73-862e-dd783196f8da.png)

## Installation

1. Clone the repository to a suitable directory
2. Create a `virtualenv` with python
3. Using pipenv install the requirements
   ```sh
   pipenv install
   ```
4. Activate the virtualenv and run `src/main.py` file
   ```sh
   python src/main.py
   ```

## Customization

You can change the loading gif by modifying `assets/pics/loading.gif`
The entire application styles can be modified by changing `src/styles.qss` file.

## Known Issues

- Inital loadtime is a bit slow
