# Quickredirect [(Capstone)](https://cs50.harvard.edu/web/2020/projects/final/capstone/)

Quickredirect is URL shortener app. When shorten URLs is open, it collects data that can be used for fingerprinting purposes (IP, language, screen resolution, user agent, date and time). Beside that it also keeps track of the number of URL openings.

Users can become a premium user. Premium users have two features:
 - Use custom redirect ID (E.g. quickredirect&#46;com/customID):
   - Not required (If empty, random id will be assigned)
   - Must be 3-15 alphanumeric characters
   - No spaces or special characters allowed
 - No ads displayed on dashboard page

# Distinctiveness and Complexity

This isn't just a URL shortener app. Besides that it also uses JavaScript to collect data when someone opens that shorten URL.

One piece of data that is stored is installed fonts on the web browser. To effectively store that data, the app will hash a list of non installed fonts and store it as a numeric value. So it can be easily stored and compare to the other data entries.

Dashboard page has ad placeholders, so that in production version you can implement ads to generate some revenue. Users can archive Premium status by paying $10 for it (one time). Premium users will not see any ads.

Premium users also can create redirects with custom ID. That means that they can have a redirect URL like this: *domain&#46;com*/**customID**. Custom ID is not required, so if left empty app will assign random (6 digits) ID as it would for non-Premium user.

JavaScript is used to transform 'auth' form from sign up to sign in and vice versa. It also checks data to make sure that fields are not empty, email address is valid and if re-entered password match the password (only on the sign up form). If all data is valid request is sent else the error message will be displayed.

A list  of  the  redirects  on  dashboard  page  will  be  10  redirects  long  at  most,  after  which  you  will  have  to  go  to  the  second  page.  (Pagination)

The whole web site is mobile responsive, if the table that displays data for the redirect is too wide, scroll bar will appear at the bottom of the table.

**Data safety and privacy: All collected data is stored locally. Nothing is sent to any 3rd party!**

# How to run

Install dependencies:

    pip install -r requirements.txt

Run server:

    python manage.py runserver

# Inside files

## Static
**authorize.js:** Switching between 'Sign In' and 'Sign Up' prompt on authorize page.
**dashboard.js:** Click the redirect URL to copy it.
**profile.js:** Make dynamic popup for editing username, password, email address.
**style.css:** Simple CSS file.

## Templates
**layout.html:** Navigation bar for every page.
**index.html:** Landing page.
**dashboard.html:** Dashboard page.
**profile.html:** Profile page.
**authorize.html:** Authorize (Sign Up/Sign In) page.
**redirect.html:** JS code for sending data from the user and redirecting after that.

## Templatetags
**group_manager.py:** Template filter for checking if the user is in the given group.

## Other
**helper&#46;py:**
 - **get_client_ip:** Gets users IP from request.
 - **generate_id:** Generate six random alphanumeric digits.
 - **is_valid_id:** Checks if user given custom id is alphanumeric, 3-15 characters long and no spaces or special characters.
 - **is_valid_email:** Using regex to check for the valid email addresses.
