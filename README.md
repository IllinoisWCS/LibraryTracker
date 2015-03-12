WCS Library Tracker 
=============

This is a 2014-2015 Tech Team Project. 
The goal is to create a useful library tracker web app for both members and officers. Members should be able to view available books online and request new materials. Officers should be able to be able to have an admin page where they can check in and out copies of books, see the status of the library overall with analytics, and have useful features such as click-to-email students with overdue books. Ideally we can connect to a database but also to APIs to pull down book information from the web for auto-fill. 

==== Setup Instructions ====

Before you begin please make sure you have mysql, python 2.7 and virtualenv installed on your machine.

1. Create and activate your virtual environment
2. Install all of the requirements using the following command:
pip install -r requirements.txt
3. Run the server using the following command:
python routes.py

If you add or remove packages please remember to use the following command so that it's reflected when other people pull:
pip freeze > requirements.txt

==== First Step ====

After you are able to run the code and see it in your local browser,
you should make sure you can contribute code via version control. 
The first task is to add your name to the contributor's list. 
Once done, commit the simple text change back to be merged into the master brance. 

1. On the github website, fork the master LibraryTracker directory. You should now have yourusername/LibraryTracker
2. Now git clone your version of LibraryTracker to your machine and then use a text editor (sublime or vim) to add your name to the README.md file
3. git add . 
4. git commit -m "meaningful commit message here"
5. git push

=== Next Steps ====

Sign up for a feature or task to contribute to the project.

High Priority: 

- Admin login for WCS officers (Brittany Kane, Jenny Cheng, Alec Mori)
- Click to email students with overdue book reminders 
- Automatically email students with books due in x days (Angela Lin Ding, Karunya Tota)
- Request a Book (Robin Sturm) (April Xu) (Vaishali Khandelwal)
- Pulling Book Data via Google API for auto-fill (Han Chen)[DONE]
- Click to see who has checked out a book (Ranran Li, Menglin Tian)
- Styling the entire web page with a theme that matches WCS
- Functionality to put a book on hold 
- Hooking up the book stats (Claire Miller, Chenying He)
- Reservation and update overdue (Violet Zou) [DONE]

Low Priority: 
- Solvin the problem of unique copies of the same book 
- Enter a NetID and see First and Last name pulled from the Illinois Directory (Han Chen)[DONE]

==== Update ====

If you want to get the latest version: 

  git remote add upstream https://github.com/IllinoisWCS/LibraryTracker.git

  git pull upstream master
  
==== Contributors ====

- Emily Tran (etran5)
- Emily Chao (elchao2)
- Xue Zou (xuezou3)
- Angela Lin Ding (alding2)
- Eva Shih (eshih3)
- Robin Sturm (rsturm2)
- Ranran Li (rli17)
- Menglin Tian (mtian6)
- Chenying He (che12)
- Jenny Cheng (jrcheng3)
- Karunya Tota (tota2)
- April Xu (aprilxu2)
- Brittany Kane (blkane2)
- Lily Sellers (lseller2)
- Nathan Handler (nhandle2)
- Vaishali Khandelwal (vkhande2)
- Han Chen (hanchen2)
- Claire Miller (ctmille2)
- Alec Mori (ajmori2)

