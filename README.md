# Readme Generator

---
## Description
A readme generator using Textual, Rich and PyInquirer. It utilises wizards to create settings and templates that can be reused. These are parsed by the template generator to prompt the user to provide values for all merge tags found.

---
## Installation Instructions
This requires python 3.9 due to PyInquirer not being updated for several years.

On Windows (CMD):
```
py -3.9 -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

On MacOS/Linux:
```bash
python3.9 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

---
## Usage Instructions

```
python main.py
```

Follow instructions on screen to generate the reusable settings and template then generate a readme.

---
## License
MIT

---
## Author
Fraser Elliott

---
## Contact Information
http://fraserdev.uk/