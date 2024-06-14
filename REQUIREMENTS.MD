# **ALIEN MATCHMAKING APP**

Welcoma to AMA (aka the alien matchmaking app).

There is a whole world of aliens on planet Pythonica.
They have recently discovered smartphone technology and mobile applications.
One of the Pythonica engineers has contacted Earth looking for a fellow Engineer to lead the design of a prototype matchmaking service.

Luckily, you have discovered the message before anyone else.
The requirements for the prototype are below. If you have an internet connection, Python and an IDE, then you are ready to start.

**GOOD LUCK!**

## **Functional reqs**

- Create profiles (set for life until profile deletion) for the Pythonica users
- Set user preferences (set for life until profile deletion)
- There’s no swiping, so there’s no need to design a recommendation algorithm. If an alien meets another alien’s eye **AND** job preferences, then it’s an instant match
- If an alien matches, a message is printed to show the match and the users' email addresses
- This prototype only runs locally
- Assume that it is the end of the simulated day when your programme has finished matchmaking its current batch
- At the end of each day, an aggregational algorithm is run to collate what happened and store it in a tabular format (i.e. mimicking an rdb)
- There can only be 5 eye colours and 5 eye colours only. Aliens’ eyes are one colour and one colour only. The colours are purple, grey, red, brown and green
- There can only be 7 professions and 7 professions only. Aliens can be gainfully employed in one of these professions and one of these professions only: entertainer, healer, warrior, farmer, spiritual guide, lawmaker and engineer
- User can only choose one eye colour and one profession in their preferences
- At the end of the simulation, return a total of how many matches there were

## **Non functional reqs**

- Deciding in the script how many aliens will be generated at the start or leaving it to the script executioner
- Create a certain number of new profiles every simulated day (mimicking people joining the app after day 1)
- Delete a certain number of profiles every simulated day (mimicking people pausing or leaving the app) e.g. 20%
- Giving the aliens names or usernames in their profiles
- Feel free to generate additional analysis about the simulation

## **Constraints**

- These aliens are all the same apart from their eye colour and their jobs (maybe name too)
- There are unlimited names (randomly generated)
- There are two genders: male and female. It is assumed males want to match with females and vice versa. 
- No need to worry about geolocation because all aliens live on one small island on the planet
- User executing the simulation decides how many days the app runs for with a max of 5
- No need to worry about fairness (i.e. some users getting significantly more matches than others) or user activity level