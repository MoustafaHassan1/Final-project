# Yes or No

#### Video Demo: <https://www.youtube.com/watch?v=SlxJB4qdkpk>

#### Description: This is a choose your own adventure type of game made in flask you are only given the choice to say yes or no and the game has multiple endings some of which are unexpected deaths and some are happy endings. you only need to enter a hero name to start playing the game and then you are off on an adventure to slay a dragon to rescue a princess and become the next king in line will you use an unbreakable weapon or will you use the power of friendship to save the day maybe you don't need any help to win or maybe the dragon will be eating some barbecue tonight. the requirements are very minimal being Flask and Flask-Session. I used bootstrap for styling as it was a very convenient way to structure the HTML layout and give a slick and responsive feel. for the templates, I used only 5 files a layout on which to base the others on, an index file that has the main game screen, a new_hero file that's used to start the game or continue where you left off, an ending file to display any ending the player may have gotten and an apology file that's the same as CS50 pset9 finance. the static folder contains three icons taken from <https://icon-icons.com/icon/mar-dragon/38125>, <https://icon-icons.com/icon/coin-dollar-finance/125510>, and <https://icon-icons.com/icon/game-steal-sword-tools-weapon/112708>. for the app.py file, I also took two functions from finance which are login_required and apology the rest is all my work. I made this project in flask for the ease of making multiple pages from a template and relative flexibility. this project was made as a final project for CS50 2022 and I made it a choose your own adventure game because I enjoy those types of games. I debated using a SQLite database for this project but found it unnecessary because the game is so short I had also made a js file and a CSS file at the beginning but found them unnecessary. I had also thought of using just Js CSS and HTML for this project but ended up at the end with flask because I am more familiar with it. the game has about fourteen endings most of which are bad endings or deaths with some neutral endings and happy endings that are the minority. after being done with this I realized that it could be done in other ways much more efficiently than using flask. the app doesn't use signed cookies instead it uses the file system. another thing to touch on is that if I had used a SQLite database I would probably have had an easier time making multiple routes for the story and making more conditions for events to trigger which would have been better for a longer game. that all being said I am glad to have used python for its easy syntax instead of using JS to do everything in the browser making it harder for someone to just trigger any ending they want unless they have reached the requirement necessary.
