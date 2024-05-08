# commerce

### An auctions web app.
This is a web application built with Django, allowing users to create and browse auction listings, place bids, and interact with listings through comments and watchlists.

#### Features
- **Models:** The application includes models for users, auction listings, bids, and comments.
- **Create Listing:** Users can create new auction listings.
- **Active Listings Page:** The default route displays all currently active auction listings.
- **Listing Page:** Clicking on a listing displays detailed information, including current price.
- **Watchlist:** Signed-in users can view and manage their watchlist.
- **Categories:** Users can browse listings by category, with each category displaying all active listings within it.
- **Django Admin Interface:** Site administrators have full CRUD functionality for listings, comments, and bids via the Django admin interface.

#### Live Demo
Check out the live version of this project [here](https://piyushupadhyay1.pythonanywhere.com/).

#### Want to run this locally?
1. Get the code in your local machine.
2. Make sure you've python3 installed.
3. Also install django via command **_pip install django_** or run **_pip install -r requirements.txt_**
4. Apply migrations: **_python manage.py migrate_**
5. Now inside the parent commerce directory run **_python manage.py runserver_**
6. Hurrah! this project is now running on your localhost.
