## Introduction
<img src="https://raw.githubusercontent.com/AdelNoroozi/Buybulm/main/resources/banner.jpg" width="400" >
This is a music platform containing two parts:
- A music bot that can be used for streaming musics and conains all kind of information about artists, albums and songs
- A music store for buying albums and gaining access to the songs of that album
This project uses PostgreSQL for storing data.

# Tools
<img src="https://raw.githubusercontent.com/AdelNoroozi/Buybulm/main/resources/python-icon.png" heigth="32" >
<img src="https://raw.githubusercontent.com/AdelNoroozi/Buybulm/main/resources/django-icon.png" heigth="32" >
<img src="https://raw.githubusercontent.com/AdelNoroozi/Buybulm/main/resources/django-rest-icon.png" heigth="32" >
<img src="https://raw.githubusercontent.com/AdelNoroozi/Buybulm/main/resources/postgresql-icon.png" heigth="31" >
<img src="https://raw.githubusercontent.com/AdelNoroozi/Buybulm/main/resources/jwt-icon.png" heigth="31" >

# Description
Users:

  Authentication
  
  ● Can register
  
  ● See their own information
  
  ● Change their password
  
  ● Change ther information
  
  ● Login (get JWT token)
  
  Bot
  
  ● Get a list of artists
  
  ● Get each artists information
  
  ● Search artists by their name or descriptions
  
  ● Get a list of albums
  
  ● Get each albums information
  
  has bought the album
  
  ● Search the albums by their title, description or artists name
  
  ● Order albums by their release date
  
  ● Filter albums by their price or artist
  
  ● Get a list of songs
  
  ● Get each songs information
  
  ● Get access to songs of each album if the album is public or if the user
  
  has bought the album
  
  ● Search the songs by their title, description, artists name, albums title
  
  or lyrics
  
  ● Order albums by their release date or number of plays
  
  ● Filter albums by their album or artist
  
  Store
  
  ● Buy albums
  
  ● Each user has access to his/her own payments
  
Admins:
  
  Authentication
  
  ● Change their password
 
  ● Login (get jwt token)
  
  Managing Users (admin must be in user section)
  
  ● View users information
  
  ● Activate or deactivate users accounts
  
  Managing bot (admin must be in bot section)
  
  ● Add artists
  
  ● Edit artists informations
  
  ● Add albums
  
  ● Edit albums informations
  
  ● Add songs
  
  ● Edit songs informations
  
  Managing store (admin must be in store section)
  
  ● Admin has access to all payments inforamtions
  
  ● Admin can filter payments by their user, album, time, price or status
  
  ● Admin can order payments by their time or price
