
## Saturday, April 6th
- After a few days of watching 3blue1brown videos about neural networks and LLMs, I was looking for avenues where I could try out some existing models and practice my learnings in real life
- I analyzed dozens of Kaggle datasets to try to identify a topic that I was passionate about. I looked into everything: [finding correlations between social media mentions of tickers and their stock prices](https://www.kaggle.com/datasets/justinmiller/reddit-pennystock-data) (a similar idea to a freelance project I took up years ago), [finding correlations between tweet locations and results in the 2020 elections](https://www.kaggle.com/datasets/manchunhui/us-election-2020-tweets), [image segmentation of satellite images of cities to determine building density](https://www.kaggle.com/datasets/aletbm/urban-segmentation-isprs) (related to my AP Seminar IRR), and even [segmentation of images of feet](https://www.kaggle.com/datasets/tapakah68/legs-segmentation)!
<img width="300" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/88af08bf-36a3-4a69-a803-ef9d63ac89fb">


## Sunday, April 7th

- On Sunday, I hopped on a call with my friend who is experienced in image segmentation and neural network research to get some advice regarding projects I should take up. While going through Kaggle datasets, I stumbled upon [a collection of ASL alphabets](https://www.kaggle.com/datasets/grassknoted/asl-alphabet). Since I started taking ASL in Grade 9, I have always been interested in developing accessibility technology for Deaf students in my school.
- Looking into it further, I realized it would be the perfect opportunity to look through existing research and learn more about image classification and neural networks
- I looked through existing Kaggle notebooks and could see all the theory I learned from 3b1b videos in practice. I gained a better understanding of layers, epochs and batches. I learned a lot of fundamental concepts like training, validation and testing.
- Later that evening, I finished training my first image classification model on the same ASL dataset
- Although having great validation accuracy, it barely worked for 10% of the trials of my own hands
- Potential issues could be bias in the dataset, overfitting on training, or compression and issues in the image-capture process.
- After looking into it further, I realized the dataset was just 80,000 images that were extremely similar; there were minor changes from picture to picture, but it lacked varying backgrounds, skin tones, and hand sizes.
<img width="300" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/5acb72b9-f1d6-46ea-b0b9-b31ea63ab7fd">

- I found an [alternative dataset](https://www.kaggle.com/datasets/lexset/synthetic-asl-alphabet) on Kaggle that had varying backgrounds, albeit it was smaller, This was my new default dataset.


## Saturday, April 13th

- Once again, I looked through existing notebooks and developed a better understanding of how image classification and convolutional neural networks worked
- After hours of training, the first model was complete, and I tested it once again. However, the model was still pretty inaccurate

## Monday, April 15th

- Although it was trained on a dataset with varying backgrounds and had over 95%+ accuracy, it failed to detect most of the alphabets I showed it
- After lots of testing during math club and my badminton team's practice session, I realized I had messed up the process of taking and compressing pictures on Google Colab. However, the model was still pretty inaccurate after I fixed the issues
- The issue is most likely because the model was trained on a dataset where the skin tone was primarily lighter, and the lighting was more consistent. It is also highly likely that the model is overfit as well, because it works very well on all validation images. I need to find a way to make the model more robust. Maybe a larger dataset will help.
- I discovered MediaPipe later in the night before going to bed

## Tuesday, April 16th

- My initial plan was to use MediaPipe on the entire training dataset and generate new IMAGES of just the landmarks of each hand. I would then train an image classification model of just these images. To recognize signs in realtime, I would use MediaPipe and generate a new image of just the hand landmarks of the individual and feed it into the CNN model.
- I augmented all the training data to only be visualizations of the landmarks, and was getting ready to train an image classification model on them
<img width="1651" alt="image" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/b38ee17c-aa14-4a3b-bf7b-b912b7bc19a1">

- After further research, I realized an image classification model was probably not the most efficient way to do live translation in the first place. I would probably have to create new images of hand landmarks for every frame in a realtime sample, and classify each frame in realtime. This would be incredibly resource intensive and laggy, and most likely not work accurately as well. Until now I had only looked into classifying one image at a time, but MediaPipe made it so live translation would be possible. Regardless, if I couldn't figure out a better solution, I would settle with image classification of the landmarks so I could at least develop a model that was better than the current dysfunctional models.
- After further research, I learned about PointNet. By simply dealing with the coordinates of the landmarks, I could create a translator that works very effectively in a realtime setting. And since it only works with three-dimensional arrays of 21 points, it would be much more efficient.

## Wednesday, April 17th

- During ASL and Chem class, I converted the entire dataset into numpy arrays of the hand landmarks in ASL and Chem class. I standardized every hand landmark to ensure that each point was relative to the leftmost, topmost, rightmost, and bottommost points of the hand. This ensures that the distance from the camera doesn't have too much of an effect on the model. Essentially, if a hand is far from the camera (which leads to a smaller hand landmark), it will be treated the same as a hand that is right in front of the camera. However, varying sizes of hands will still be an issue. (I notice this later when I demo this project to my ASL teacher and it struggles to detect the hands of many other students)
<img width="300" alt="Converting Signs to Points 2" src="https://github.com/kevinjosethomas/sign-language-recognition/assets/46242684/c054850b-9f48-4d4d-be4a-d202fc9aded1">

- However, even after converting the dataset to points, I still had no idea how to train PointNet on the new dataset
- Eventually, after school, I stumbled across this article about [Point Cloud Classification with PointNet](https://keras.io/examples/vision/pointnet/)
- I used a similar approach to train the data on the numpy arrays of ASL alphabet hand landmarks. However, still being new to how most of this works, I decided that the shuffling step was unnecessary and decided to skip it 💀 This was a mistake, as the model was not learning anything and had an accuracy of 0 the entire time.
- Not knowing what the issue was, I went back to trying to create an image classification model of the hand landmarks instead of using PointNet. When implementing this, I realized the importance of shuffling and went back to the PointNet model to try again. It worked!
- I trained the model on the ASL dataset for 20 epochs with a learning rate of 0.001. It worked pretty well when I tested it on some individual images.
- I setup a local live webcam stream with MediaPipe and the PointNet model to test the model on live data. It worked really really well! However, the model was still not perfect. It got many signs confused (A-S-T-M-N, C-E, G-H, V-W, etc.).
- I left it training for 100 epochs with a learning rate of 0.0001 overnight.

## Thursday, April 18th

- I watched many videos about layers in neural networks and how the Adam optimization function worked (English class was boring)
- Started documenting the development process and pushed most of the code to GitHub
- Developed new plots of the three different models I tested earlier (CNN, ResNet, PointNet) for future documentation and reference.
- Demoed the prototype to my CS teacher, received the following feedback:
  - I should work more closely with BCSD and ASL teachers in my school as I continue on this project
  - I should also find a mentor and look into grants to help continue this project

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
