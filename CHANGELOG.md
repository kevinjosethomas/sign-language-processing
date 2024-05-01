# Changelog
This document is a log of my daily progress in this project. I log my work on a "best-effort" basis, and this document still lacks some of my attempts and discoveries. Regardless, it will still serve as a good starting point for anyone interested in understanding the process of this project's development. Feel free to contact me if you have any questions!

# Log

## Tuesday, April 30th
- Added ThreeJS rendering of a 3D model (Teslabot!)
- This will eventually adopt to sign actual ASL words
<img width="1822" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/b806872c-8df9-4219-8d10-0fe72096301f">


## Monday, April 29th
- Migrated from WebRTC architecture to flask + websockets
- Cleaned up code and modularized structure further
- Added new interface for ASL fingerspell recognition, as well as speech-to-text

<img width="1822" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/8e9219a2-ab11-47a8-b074-4c1c5d680d5c">

- Imported rigged hand model and tried to manipulate it
https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/e83b6ed9-f054-4f51-ae04-fd65ea7a8a96



## Sunday, April 28th
- I trained the model for 100 epochs with a Learning Rate of 0.0005. Here are the results:

<img height="287" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/c29a7ac8-56b2-4a54-82a4-b24db7a7acda">
<img height="287" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/bbc2d932-f3ae-4872-b784-1dda5f4b8550">

- I believe it is noticeably more accurate, at least when I test out all alphabets
- However, there is still a random spike in the validation loss and a sudden drop in validation accuracy. I'm not sure if I made a mistake in my dataset. The loss is still always about 135 which is an issue as well
- Create more diagrams that explain the processes involved in ASL Translation
  1. Describes normal 4-step communication process
  2. Describes 4-step communication process with an interpreter/translator
  3. Describes ASL communication process with a translation tool
  4. Describes the benefit of my current ASL translation tool 

<img height="226.4" alt="Communication Diagram" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/dad4548b-4d09-4092-9169-a0ec14807ced">
<img height="226.4" alt="Communication with Interpreter" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/e1412e67-f601-4708-83f6-e9601f68d559">
<img width="2460" alt="ASL Communication with Translation Tool" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/1e5edcf1-4b6c-462b-87a0-fa177378d299">
<img width="2460" alt="My Current Solution" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/de5166ff-567f-41fc-9cfb-fcffe2aaed87">

- Spent 7 hours trying to get WebRTC working
- Got WebRTC working
- Realized WebRTC was kinda mid
- Went back to using 5 lines of code to iframe a flask webpage that streamed the user's webcam


## Saturday, April 29th
- Created two UML diagrams
  - One that represents the Training process of the PointNet model
  - One that represents the Inference and Transcription process of the entire program

<img width="1620" alt="Training" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/c2b1dbd6-7a46-4d8e-9ed3-151fbb73facf">
<img width="1986" alt="ASL Recognition UML" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/2a2d4998-4f64-4053-a4c9-1645fa2287db">


## Thursday, April 25th
- Cleaned up the visualization of live transcription (now shows up on the bottom of the screen)
- Fixed the bug where text was deleted when sent to OpenAI for correction
- Created a [demo video](https://www.youtube.com/watch?v=MAavd4ZODxU) to demonstrate all the progress so far


## Wednesday, April 24th
- I continued to dedicate some time to get the transcription part working, now that the recognition part was decent enough
- I developed a transcription procedure that inserted spaces when no hand was detected and didn't allow more than two consecutive repetitions of the same letter
- I ended up with a decent procedure that effectively placed spaces and got relatiely correct letter placements
- I attemped to fix any remaining inaccuracies and typoes by using llama2 to fix any errors in the transcription
- Llama2 did not live up to the expectations so I tried Llama3 7B, but still failed to receive the results I wanted
- I recorded an [update video](https://www.youtube.com/watch?v=SQE21gRKCHs) to demonstrate the current progress of the project as of right now (without AI translation)
- Finally, I downloaded Llama3 70B... only to realize by M2 Air cannot handle it 💀
- I decided to move to use OpenAIs APIs... and I settled with a decent prompt using GPT-4-Turbo
- The code stores a raw transcription and an AI transcription. It only feeds OpenAI with the raw transcription and only shows the user the AI transcription
- This allows GPT-4 to entirely change sentences as the raw input changes, as it can make better decisions with longer input
- However, this also leads to the transcription changing entirely when the user uses it, but this is okay as it tends to become more correct over time
- I spent 8 hours coding and atleast 2 more hours browsing and learning for this project today. I am now about 2 weeks behind for AP Physics prep, 1 week behind for AP Precalc prep, my AP Seminar Individual Media Presentation is in 2 days (I don't have a final script yet) and I haven't started preparing for AP Computer Science Principles yet. I think its time to focus on school....

![image](https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/29508886-6f8c-4040-9fd5-22475e46816f)


## Tuesday, April 23rd

- So.... turns out I wasn't actually saving the numpy arrays into files when I parsed the 200,000 image dataset. Which is why I still only had 20,000 files after converting the images into vectors 💀
- So I'm in ASL class and I'm augmenting all three image datasets into points once again. This time I'm not separating them between left and right hands.

<img width="400" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/7f8cbb97-3638-4dc2-82a2-11156a146d5c">
<img width="400" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/d8aba9b7-111f-4449-a7a9-d75cb6186ed0">

- With the new 150,000 point dataset, I trained the PointNet model. However, I was getting absurd validation loss, beyond the billions.
- I tried again with a batch size of 128 instead of 256, and the validation loss was significantly better, albeit still a little too high

<img width="1651" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/1dcf5a4c-1e40-4672-b320-c80795344180">

- I tried again with a batch size of 64, and the validation loss was even better, although still a little too high
- This 20 Epoch, 64 Batch Size, 0.001 LR model is the most accurate model I have trained so far

<img width="1651" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/0a9be99e-5ac1-4b2f-9baa-06284e755d5e">


## Monday, April 22nd

- Reworked the MediaPipe integration to be more seamless, fixed the prior issues of it not detecting all people
- Made the hand landmarks more visible
- Separated datasets into left/right folders for two separate models
- Downloaded two more datasets and added them to the data: [First](https://www.kaggle.com/datasets/danrasband/asl-alphabet-test) [Second](https://www.kaggle.com/datasets/debashishsau/aslamerican-sign-language-aplhabet-dataset)

<img width="400" alt="Converting Signs to Points 2" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/04ea130b-e20e-469f-8d1d-663fdb97136c">
<img width="400" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/6a3a5291-5ef0-46ca-9e53-b751fa6b0bef">

- Then, I trained two separate models for the left and right hand respectively. I trained them both over 20 epochs with a learning rate of 0.001. For some reason, there seems to be an issue with the validation accuracy. Maybe there was too less test data considering I put all the new datasets into training data. Also, for some reason there were only around 20,000 files in my final dataset although it should be over 200,000 files. The new models are pretty inaccurate as well. Unsure what went wrong!

<img width="503" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/3293ec61-eb12-44bf-8064-f3bde286cd72">
<img width="503" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/d642424b-72e9-41fa-af36-55031e4ed7ce">


## Friday, April 19th

- Watched several videos on the different layers of neural networks. Learned about neurons and reviewed the basics of weights and activation functions.
- Added probability of predictions to overlay on the webcam stream
- Demoed the prototype to my ASL teacher, received the following feedback:
  - Most ASL translation efforts in the past have been focused on translating English to ASL, not the other way around.
  - No translation tool that only enables communication for a single party is a truly viable solution. Therefore, the tool must enable communication between both parties.
  - The prototype is a good start, allowing signers to use fingerspelling to communicate with hearing individuals. The next step would be to allow hearing individuals to communicate with ASL signers (basic speech-to-text).
  - Fingerspelling is an essential part of ASL and it is a good start. However, it still requires ASL signers to process their words into English, convert them into English alphabet, and then sign them. The ultimate goal is to create a platform that enables Deaf individuals to communicate WITHOUT translating to English. ASL is not built on top of English, it is processed as a separate language in the brain, and translating to English is a confusing and limiting obstacle for Deaf individuals.
  - The ultimate goal would be: Deaf individuals sign -> their signs are translated to English and spoken out loud for hearing individuals -> hearing individuals speak -> their speech is translated to visual ASL signs for Deaf individuals.
  - ASL is a nuanced language: facial expressions, body language, different grammar, and many other non-manual signals are important aspects of translation.
  - The main thing is to keep working towards making it better. It will never be perfect and there will always be shortcomings, but as long as I keep working on it, it will get better.
- My notes based on the above:
  - The model has only been trained on a small sample of alphabets so far (about 23,000 images) and it gets many signs confused (A-S-T-M-N, C-E, G-H, V-W, etc.).
  - Many of these issues are because the model is trained on both left and right handed images. It might be a good idea to separate my datasets and make two separate models: one for the left hand and one for the right hand. MediaPipe classifies hands into left and right which should make this possible. By doing this, when the model sees a hand, I can use MediaPipe to identify which hand it is, and then use the corresponding model to predict the sign.
  - Furthermore, I can also add more training data for the model to be more accurate. I can combine a few Kaggle datasets to get a larger dataset.
  - I also made the mistake of not testing the model on many other people before demoing to my ASL teacher. While the MediaPipe hand landmark detection has always worked immediately for me, it often struggled for my ASL teacher and some of the other students in the class. My local version of MediaPipe also doesn't identify the crossed fingers when I sign the letter R, but the online MediaPipe Studio version does. There must be a difference in the models that I need to investigate.
  - Next steps are as follows:
    - Download more datasets and import them into the model
    - Separate the dataset into left and right hands, and train two separate models
    - Once the model is sufficiently accurate, figure out how to make it transcribe letters instead of just detecting letters
    - Connect the transcription to a text-to-speech interface


## Thursday, April 18th

- I watched many videos about layers in neural networks and how the Adam optimization function worked (English class was boring)
- Started documenting the development process and pushed most of the code to GitHub
- Developed new plots of the three different models I tested earlier (CNN, ResNet, PointNet) for future documentation and reference.
- Demoed the prototype to my CS teacher, received the following feedback:
  - I should work more closely with BCSD and ASL teachers in my school as I continue on this project
  - I should also find a mentor and look into grants to help continue this project


## Wednesday, April 17th

- During ASL and Chem class, I converted the entire dataset into numpy arrays of the hand landmarks in ASL and Chem class. I standardized every hand landmark to ensure that each point was relative to the leftmost, topmost, rightmost, and bottommost points of the hand. This ensures that the distance from the camera doesn't have too much of an effect on the model. Essentially, if a hand is far from the camera (which leads to a smaller hand landmark), it will be treated the same as a hand that is right in front of the camera. However, varying sizes of hands will still be an issue. (I notice this later when I demo this project to my ASL teacher and it struggles to detect the hands of many other students)

<img width="400" alt="Converting Signs to Points 2" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/c054850b-9f48-4d4d-be4a-d202fc9aded1">

- However, even after converting the dataset to points, I still had no idea how to train PointNet on the new dataset
- Eventually, after school, I stumbled across this article about [Point Cloud Classification with PointNet](https://keras.io/examples/vision/pointnet/)
- I used a similar approach to train the data on the numpy arrays of ASL alphabet hand landmarks. However, still being new to how most of this works, I decided that the shuffling step was unnecessary and decided to skip it 💀 This was a mistake, as the model was not learning anything and had an accuracy of 0 the entire time.
- Not knowing what the issue was, I went back to trying to create an image classification model of the hand landmarks instead of using PointNet. When implementing this, I realized the importance of shuffling and went back to the PointNet model to try again. It worked!
- I trained the model on the ASL dataset for 20 epochs with a learning rate of 0.001. It worked pretty well when I tested it on some individual images.
- I setup a local live webcam stream with MediaPipe and the PointNet model to test the model on live data. It worked really really well! However, the model was still not perfect. It got many signs confused (A-S-T-M-N, C-E, G-H, V-W, etc.).
- I left it training for 100 epochs with a learning rate of 0.0001 overnight.


## Tuesday, April 16th

- My initial plan was to use MediaPipe on the entire training dataset and generate new IMAGES of just the landmarks of each hand. I would then train an image classification model of just these images. To recognize signs in realtime, I would use MediaPipe and generate a new image of just the hand landmarks of the individual and feed it into the CNN model.
- I augmented all the training data to only be visualizations of the landmarks, and was getting ready to train an image classification model on them

<img width="1651" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/b38ee17c-aa14-4a3b-bf7b-b912b7bc19a1">

- After further research, I realized an image classification model was probably not the most efficient way to do live translation in the first place. I would probably have to create new images of hand landmarks for every frame in a realtime sample, and classify each frame in realtime. This would be incredibly resource intensive and laggy, and most likely not work accurately as well. Until now I had only looked into classifying one image at a time, but MediaPipe made it so live translation would be possible. Regardless, if I couldn't figure out a better solution, I would settle with image classification of the landmarks so I could at least develop a model that was better than the current dysfunctional models.
- After further research, I learned about PointNet. By simply dealing with the coordinates of the landmarks, I could create a translator that works very effectively in a realtime setting. And since it only works with three-dimensional arrays of 21 points, it would be much more efficient.


## Monday, April 15th

- Although it was trained on a dataset with varying backgrounds and had over 95%+ accuracy, it failed to detect most of the alphabets I showed it
- After lots of testing during math club and my badminton team's practice session, I realized I had messed up the process of taking and compressing pictures on Google Colab. However, the model was still pretty inaccurate after I fixed the issues
- The issue is most likely because the model was trained on a dataset where the skin tone was primarily lighter, and the lighting was more consistent. It is also highly likely that the model is overfit as well, because it works very well on all validation images. I need to find a way to make the model more robust. Maybe a larger dataset will help.
- I discovered MediaPipe later in the night before going to bed


## Saturday, April 13th

- Once again, I looked through existing notebooks and developed a better understanding of how image classification and convolutional neural networks worked
- After hours of training, the first model was complete
  - Optimizer: Adam
  - Loss: Sparse Categorical Crossentropy
  - Parameters: 23,830,555
- Here are the results after 20 epochs:

<img width="1651" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/336d72e3-4c48-4b5f-955c-d162c58865aa">

```
              precision    recall  f1-score   support

           A       0.94      0.93      0.93       100
           B       0.90      0.93      0.92       100
       Blank       0.99      0.98      0.98       100
           C       0.96      0.95      0.95       100
           D       0.89      0.89      0.89       100
           E       0.86      0.81      0.84       100
           F       0.95      0.88      0.91       100
           G       0.92      0.93      0.93       100
           H       0.97      0.95      0.96       100
           I       0.89      0.87      0.88       100
           J       0.86      0.96      0.91       100
           K       0.80      0.93      0.86       100
           L       0.95      0.94      0.94       100
           M       0.71      0.77      0.74       100
           N       0.75      0.79      0.77       100
           O       0.89      0.93      0.91       100
           P       0.95      0.98      0.97       100
           Q       0.99      0.85      0.91       100
           R       0.85      0.93      0.89       100
           S       0.87      0.86      0.86       100
           T       0.99      0.89      0.94       100
           U       0.89      0.90      0.90       100
           V       0.75      0.78      0.76       100
           W       0.91      0.75      0.82       100
           X       0.90      0.92      0.91       100
           Y       0.98      0.95      0.96       100
           Z       0.93      0.90      0.91       100

    accuracy                           0.89      2700
   macro avg       0.90      0.89      0.89      2700
weighted avg       0.90      0.89      0.89      2700
```

- Here are the results after 30 epochs:

<img width="503" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/a75a5c66-5cc6-47d5-a5c2-6ab1094c5248">
<img width="503" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/acf76f32-429b-43e1-9e6c-b724e07ab4d4">

```

              precision    recall  f1-score   support

           A       0.93      0.95      0.94       100
           B       1.00      0.90      0.95       100
       Blank       0.99      0.99      0.99       100
           C       0.95      0.96      0.96       100
           D       0.90      0.89      0.89       100
           E       0.88      0.91      0.89       100
           F       0.96      0.92      0.94       100
           G       0.93      0.94      0.94       100
           H       0.97      0.96      0.96       100
           I       0.89      0.89      0.89       100
           J       0.88      0.98      0.93       100
           K       0.85      0.92      0.88       100
           L       0.97      0.96      0.96       100
           M       0.82      0.78      0.80       100
           N       0.79      0.84      0.81       100
           O       0.93      0.92      0.92       100
           P       0.99      0.99      0.99       100
           Q       0.99      0.90      0.94       100
           R       0.90      0.91      0.91       100
           S       0.87      0.87      0.87       100
           T       0.98      0.92      0.95       100
           U       0.82      0.94      0.88       100
           V       0.78      0.83      0.81       100
           W       0.89      0.80      0.84       100
           X       0.90      0.92      0.91       100
           Y       0.99      0.96      0.97       100
           Z       0.95      0.89      0.92       100

    accuracy                           0.91      2700
   macro avg       0.91      0.91      0.91      2700
weighted avg       0.91      0.91      0.91      2700
```

- I tested the model in real-life circumstances once again, however, the model was still pretty inaccurate


## Sunday, April 7th

- On Sunday, I hopped on a call with my friend who is experienced in image segmentation and neural network research to get some advice regarding projects I should take up. While going through Kaggle datasets, I stumbled upon [a collection of ASL alphabets](https://www.kaggle.com/datasets/grassknoted/asl-alphabet). Since I started taking ASL in Grade 9, I have always been interested in developing accessibility technology for Deaf students in my school.
- Looking into it further, I realized it would be the perfect opportunity to look through existing research and learn more about image classification and neural networks
- I looked through existing Kaggle notebooks and could see all the theory I learned from 3b1b videos in practice. I gained a better understanding of layers, epochs and batches. I learned a lot of fundamental concepts like training, validation and testing.
- Later that evening, I finished training my first image classification model on the same ASL dataset:
  - Optimizer: Adam
  - Loss: Categorical Crossentropy
  - Parameters: 893,085

```
              precision    recall  f1-score   support

           A       1.00      1.00      1.00       300
           B       1.00      0.99      0.99       300
           C       1.00      1.00      1.00       300
           D       1.00      1.00      1.00       300
           E       0.99      1.00      1.00       300
           F       1.00      1.00      1.00       300
           G       1.00      1.00      1.00       300
           H       1.00      1.00      1.00       300
           I       1.00      1.00      1.00       300
           J       1.00      1.00      1.00       300
           K       1.00      0.97      0.98       300
           L       1.00      1.00      1.00       300
           M       0.99      1.00      1.00       300
           N       1.00      0.99      1.00       300
           O       1.00      1.00      1.00       300
           P       1.00      1.00      1.00       300
           Q       1.00      1.00      1.00       300
           R       1.00      1.00      1.00       300
           S       1.00      1.00      1.00       300
           T       1.00      1.00      1.00       300
           U       1.00      1.00      1.00       300
           V       0.98      1.00      0.99       300
           W       1.00      1.00      1.00       300
           X       1.00      1.00      1.00       300
           Y       1.00      1.00      1.00       300
           Z       1.00      1.00      1.00       300
         del       1.00      1.00      1.00       300
     nothing       1.00      1.00      1.00       300
       space       1.00      1.00      1.00       300

    accuracy                           1.00      8700
   macro avg       1.00      1.00      1.00      8700
weighted avg       1.00      1.00      1.00      8700
```

<img width="600" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/684b751b-e3be-424b-ad04-c90fa4b1b7ab">

<img width="600" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/575ec914-01bd-4ec8-b7a8-648dd2cc94a2">

- Although having great validation accuracy, it barely worked for 10% of the trials of my own hands
- Potential issues could be bias in the dataset, overfitting on training, or compression and issues in the image-capture process.
- After looking into it further, I realized the dataset was just 80,000 images that were extremely similar; there were minor changes from picture to picture, but it lacked varying backgrounds, skin tones, and hand sizes.

<img width="400" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/5acb72b9-f1d6-46ea-b0b9-b31ea63ab7fd">

- I found an [alternative dataset](https://www.kaggle.com/datasets/lexset/synthetic-asl-alphabet) on Kaggle that had varying backgrounds, albeit it was smaller, This was my new default dataset.


## Saturday, April 6th

- After a few days of watching 3blue1brown videos about neural networks and LLMs, I was looking for avenues where I could try out some existing models and practice my learnings in real life
- I analyzed dozens of Kaggle datasets to try to identify a topic that I was passionate about. I looked into everything: [finding correlations between social media mentions of tickers and their stock prices](https://www.kaggle.com/datasets/justinmiller/reddit-pennystock-data) (a similar idea to a freelance project I took up years ago), [finding correlations between tweet locations and results in the 2020 elections](https://www.kaggle.com/datasets/manchunhui/us-election-2020-tweets), [image segmentation of satellite images of cities to determine building density](https://www.kaggle.com/datasets/aletbm/urban-segmentation-isprs) (related to my AP Seminar IRR), and even [segmentation of images of feet](https://www.kaggle.com/datasets/tapakah68/legs-segmentation)!

