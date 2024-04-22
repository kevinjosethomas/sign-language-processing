# ✌️ ASL Fingerspell Recognition with MediaPipe, Keras and Pointnet

## Table of Contents

## Motivation

Throughout elementary and middle school, I attempted to learn 4 different languages (Hindi, Spanish, Sanskrit and French), but despite investing years into each, I was never able to develop working proficiency in any of them. However, when I moved to Greater Vancouver in 2021, I was provided with the unique opportunity to study a new kind of language — a visual language — in my high school. Over the last three years, learning ASL and studying in the same building as BC's Secondary School for the Deaf has been an insightful experience, introducing me to a new perspective on language and lifestyle.

Initially, back in Grade 9, I was introduced to the basics of ASL, learning the alphabet, numbers, and basic phrases. At this time, I was interested in developing some kind of ASL-related technology, primarily focusing on creating visual and vibratory experiences for music; however, I never got myself to build anything viable.

## Attempt 1: Image Classification (CNN)

- Optimizer: Adam
- Loss: Categorical Crossentropy
- Parameters: 893,085

[![](https://github.com/kevinjosethomas/sign-language-recognition/blob/main/docs/Image%20Classification%20Model%201/Accuracy%20and%20Loss%20-%20Training%20and%20Validation.png)]()

## Attempt 2: Keras ResNet

- Optimizer: Adam
- Loss: Sparse Categorical Crossentropy
- Parameters: 23,830,555

### 20 Epochs

[![](https://github.com/kevinjosethomas/sign-language-recognition/blob/main/docs/Image%20Classification%20Model%202/20%20Epochs/Accuracy%20and%20Loss%20-%20Training%20and%20Validation.jpg?raw=true)]()

### 30 Epochs

[![](https://github.com/kevinjosethomas/sign-language-recognition/blob/main/docs/Image%20Classification%20Model%202/30%20Epochs/Last%2010%20Epochs%20-%20Accuracy%20and%20Loss%20-%20Training%20and%20Validation.jpg?raw=true)]()
[![](https://github.com/kevinjosethomas/sign-language-recognition/blob/main/docs/Image%20Classification%20Model%202/30%20Epochs/All%2030%20Epochs%20-%20Accuracy%20and%20Loss%20-%20Training%20and%20Validation.jpg?raw=true)]()

## Attempt 3: PointNet

- Optimizer: Adam
- Loss: Sparse Categorical Crossentropy
- Parameters: 751,043

### 20 Epochs

[![](https://github.com/kevinjosethomas/sign-language-recognition/blob/main/docs/Pointnet%20Classification/20%20Epochs%20-%200.001%20LR/Training%20Validation%20Accuracy%20Loss.png?raw=true)]()

### 100 Epochs
