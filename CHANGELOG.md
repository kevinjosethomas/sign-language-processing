## Sunday, April 7th

- Finished training my first image classification model on the ASL dataset.
- Although having a great validation accuracy, it barely worked for 10% of the images I tested it on in real time.
- Potential issues could be bias in the dataset, overfitting on training, or compression and issues in the image taking process.
- After looking into it further, I realized the dataset was just 80,000 images that were extremely similar: minor changes from picture to picture, and it lacked varying backgrounds, skin tones, and hand sizes.
- Found an alternative dataset on Kaggle that had varying backgrounds, albeit it was smaller, This was my new default dataset.

## Saturday, April 13th

- After hours of training, I tested the ASL ResNet model on individual webcam images
- The model was still pretty inaccurate.

## Monday, April 15th

- Although it was trained on a dataset with varying backgrounds and had over 95+ accuracy, it failed to detect most of the alphabets I showed it
- I realized I was messing up on the process of taking and compressing pictures on Google Colab before feeding it into the model, but the model was still pretty innaccurate after I made the changes
- The issue is most likely due to the fact that the model was trained on a dataset where the skin tone was primarily lighter, and the lighting was more consistent. Its possible that the model is overfit as well, because it works very well on all validation images. I need to find a way to make the model more robust. Maybe a larger dataset will help.
- Discovered MediaPipe later in the night before going to bed

## Tuesday, April 16th

- My initial plan was to use MediaPipe on the entire training dataset and generate new IMAGES of just the landmarks of each hand
- After further research, I realized an image classification model was probably not the most efficient way to do live translation in the first place. Until now I had only looked into classifying one image at a time, but MediaPipe made it so live translation would be possible.
- By simply dealing with the coordinates of the landmarks, I could create a translator that works very effectively in a realtime setting.
- After further research, I learned about PointNet.

## Wednesday, April 17th

- I converted the entire dataset into numpy arrays of the hand landmarks in ASL and Chem class (morning half). I standardized every handlandmark to ensure that each point was relative to the leftmost, topmost, rightmost, and bottommost points of the hand. This ensures that the distance from the camera doesn't have too much of an effect on the model. Sizes of hands will still be an issue though.
- However, I still had no idea how to train PointNet on the new dataset
- Eventually, after school, I stumbled across this article about [Point Cloud Classification with PointNet](https://keras.io/examples/vision/pointnet/)
- I used a similar approach to train the data on the numpy arrays of ASL alphabet hand landmarks. However, still being new to how most of this works, I decided that the shuffling step was unnecessary and decided to skip it. This was a mistake, as the model was not learning anything and had an accuracy of 0 the entire time.
- Not knowing what to do, I went back to creating a hand landmark image version of the dataset so I could use an image classification model instead of PointNet. When implementing this, I realized the importance of shuffling and went back to the PointNet model to try again. It worked!
- I trained the model on the ASL dataset for 20 epochs with a learning rate of 0.001. It worked pretty well when I tested it on some individual images.
- I setup a local live webcam stream with MediaPipe and the PointNet model to test the model on live data. It worked really really well! However, the model was still not perfect. It got many signs confused (A-S-T-M-N, C-E, G-H, V-W, etc.).
- I left it training for 100 epochs with a learning rate of 0.0001 overnight.

## Thursday, April 18th

- Watched many videos about layers in neural networks and how the Adam optimization function worked.
- Started documenting the development process and pushed most of the code to GitHub.
- Developed new plots of the three different models I tested (CNN, ResNet, PointNet) for future documentation and reference.
- Demoed the project to my CS teacher:
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
