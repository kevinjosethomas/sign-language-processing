## Friday, April 19th

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
