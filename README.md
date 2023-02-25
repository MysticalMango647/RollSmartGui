# RollSmartGui

### Thank you for viewing the GUI application. Just a couple notes if you wanted to run it.

1. **main.py** contains code for the actual rollsmart code for the the GUI that's under development.
2. **AdminUserCreation.py** contains code for the admin creation application. 

..*    The AdminUserCreation.py is relatively finished, adjustmest that are needed for this are more front end or tweaking it to make it more appealing(Ideally, at the end I jsut want to make it one long vertical oreinted form that can be scrolled upon, where at the end of the form the user can hit submit, also add error trapping + password requirement)

..*    The AdminUserCreation.py code is good to go for it. When the submit button is pressed, it will automatically connect to firebase database, create a new user account. send an activation email to the user and create firebase entry for both the loginTable and collectedData table in firebase. Note: it will initialize the user data with blank entries for each sensor value with null and a timestamp of when the data was created.

### Couples tips to run this code, just to make it eaiser, since theres a couple libraries that are a little cluster "mess" due to backward compatibility
1. I recommend using the ide "PyCharm", VsCode along with others could work. But PyCharm makes it relatively straight forward, specially installing libraries without needing to pip them.
2. For python, **USE VERSION 3.8**, version 3.11 doesn't work, and versions inbetween those are unstable due to the GUI library just being very picky.
3. If you have version 3.8 installed, and set as the current interpreter for python, then installing **PyQt5** library shouldn't be an issue.
4. For the **Pyrebase** Library. Install **_Pyrebase4_, Not Pyrebase** For some reason the original Pyrebase is appears to be avaliable on *PyPi* but when installing it, there will be issues, that make it appear to be a pip issue. Which is not the case, but rather the library importing another library that is not supporter properly(I believe it's, PyCryptoDome). If you have it installed already, I recommend uninstalling it as it can cause interference with Pyrebase4.
5. These are just the big issues I had, and had to experiment with to get it to compile, and suspect these are some errors you may encounter if you are using the latest version of python.
