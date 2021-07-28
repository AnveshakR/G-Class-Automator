# G-Class-Automator
Tool to auto-launch google meets from google classrooms because I'm too lazy to do all the clicking by myself.

You'll need Chromedriver to make this work, download link [here](https://chromedriver.chromium.org/downloads).
(Download the correct version according to the version of Chrome you're using righjt now that you can check in the Control Panel)
Extract the chromedriver.exe file to a suitable place and add the absolute path to the chrome_path variable in the code.

Side note: If you're using a different Chrome profile for your college stuff, you can change the program to use that profile only by changing the path from "Default" to however it is stored on your computer. To see what it is stored as, write **chrome://version/** in the URL of that particular profile and look for the **Profile Path**. Note the end folder name like "Profile 1" and replace it with default.

https://github.com/AnveshakR/G-Class-Automator/blob/faf2011c76d7fccf5e0a2eb14a579b4a5156aa2b/class.py#L24

## Using the Excel Sheet
The program runs on the attached Excel sheet now. Fill in your timetable in the appropriate table with the lecture name abbreviations, with the lecture start times in the first column in 24-hour format like 12:34:56 or 21:00:00. 

In the table to the right, put the abbreviations (case-sensitive) with the corresponding classroom links in the column next to it.

It should look something like this:

![](https://github.com/AnveshakR/G-Class-Automator/blob/master/images/sheetexample.png)
