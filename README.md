#NOT FINISHED!!!!!

# AlexaTV
A little background about me and this project. I recently got an alexa and I wanted to see how to develop a skill for alexa. I came up with the idea of controlling my TV with my voice. This is my first time using python so my python coding it pretty sub par but bare with me. I also liked this project because I use AWS IOT for the first time which I found out is a pretty useful product.

This readme will be a quick overview of how to use Alexa, AWS Lambda, AWS IOT, and a raspberry pi to control your TV. My assumption is that most people are fimilar with these products so I won't go into to much depth. If you get stuck, just google search a beginner guide. This project doesn't require that much knowledge into this products

##Alexa Skill
Log into the AWS Developer portal and select Alexa at the top of the screen. Select Add a new skill and select a name for your skill. The invocation name is what will activate this skill with Alexa. In my project, I choose "The TV" so I can say "Alexa, ask The TV..."

Go to the interaction model and paste the model from the project into it. This will dictate what the different intents of the skill. For this project we have TVOn and TVOFf. Place the utterance files into the sample utterance. This is how alexa can tell what phrases should invocate what intents for the skill.

Go to the configuration tab and select AWS lambda ARN. Later on we will create a AWS Lambda and we will paste that ARN here. 

##AWS IOT
Go to AWS and then navagiate to AWS IOT. Then select to register a thing and name this thing. Go back to the main AWS IOT and select security and create a policy 

##AWS Lambda


##Raspberry Pi
Load the the RPi.py file with the certificate files into a folder on your pi. Run the script and sit back. The script will keep on loop looking for messages from the lambda function. When it receives a message, it will run the subroutine and depending on the topic, turn the TV on or off
