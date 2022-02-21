# Study Buddy

**Study Buddy** is a web application that consists of activities designed to help students absorb information on computer science.

## Features

A user may
* create an account
* log in with their username and password
* see all available activities, take the quizzes, and get feedback
* see statistics on their performance
* post questions
* answer other users' questions
* like other users' answers
* delete their own questions and answers
* log out

An administrator may additionally
* add and delete quizzes
* delete any questions and answers
* see statistics on the use of the app, e.g. how many users, how many times a quiz has been taken
* delete a user account


## Ideas for the Activities
Quizzes on
* different acronyms related to computer science
* CS consepts and their explanations (in brief)
* translating CS vocabulary (English/Finnish)
* binary/hexadecimal/decimal values


## Development Update 6.2.2022
At the moment, it is possible to
* test the app in Heroku
* create a user account
* log in and out
* navigate the pages

Unfortunately, any other features are not yet available but I have done some preparations for the quizzes, chat, and stats, so please, check the code files and templates, too.

## Development Update 20.2.2022
The app can be tested in [Heroku](https://tsoha-study-buddy.herokuapp.com/).

Now, a user ("buddy") can
* create a user account
* log in and out
* navigate the pages
* take quizzes
* send questions to a question forum
* see and answer questions
* delete their own questions and answers
* follow their progress

An administrator can additionally
* create new quizzes
* delete quizzes
* see some statistics on the use of the app

To test the administration options:
* Username: Admin
* Password: TheBossBuddy
* Note! There isn't any function for bringing deleted quizzes back yet, so if you try deleting a quiz, please, create one first. :)

I have also tried to improve usability by
* showing error messages on the same page that causes the error instead of a separate page
* adding a logout link to every page and locating it better
* making the text darker so that it is more distinct from the background
