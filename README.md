# ConcertBot
ConcertBot, with rasa

1.Make sure you have Rasa 2.8.1 installed with Rasa-sdk:2.8.1. 


2.Make sure you have installed latest Mysql and created a database named rasa and created table concert_order by typing “create table concert_order(id_order int NOT NULL AUTO_INCREMENT, name varchar(64),email varchar(64),concert_name varchar(64),ticket_type enum(‘first’,’second’,’third’),PRIMARY KEY(id_order))”


3.Run “rasa shell” in one terminal, and run “rasa run actions&” in the other one or other commands you like.


