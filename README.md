https://github.com/kevinjosethomas/sign-language-translation/assets/46242684/8d3778e4-661b-45a5-a3f0-06d28fdde9b4

# ✌️ ASL ⭤ English Translation with MediaPipe, PointNet, ThreeJS and Semantic Search

American Sign Language (ASL) is a complete, natural language that exhibits the same linguistic complexities as spoken languages, including its own syntax, morphology, and grammar that significantly differ from English. Most existing tools that aim to bridge ASL and English often prioritize the needs of hearing individuals, simply offering Text-to-Speech (TTS) and Speech-to-Text capabilities (STT), developed under the misconception that ASL is an identical language to English.

> [!NOTE]
> As a hearing student with limited ASL proficiency, I recognize that my perspective as a hearing person is extremely limited. My role has been to listen carefully and integrate feedback from the Deaf community, and I have done my best to approach this project with a mindset of learning and understanding, rather than assuming. This project would not have been possible without the active involvement and advice of Deaf individuals and ASL experts who have generously shared their insights.

This project is a prototype that enables translation between American Sign Language (ASL) and English, facilitating communication between ASL signers and individuals who do not understand ASL. It is still far from accurately translating the nuances of visual language, but it is designed to respect and preserve ASL as the primary language. The interface provides two main functionalities:

<table style="width: 100%">
  <tr>
    <th style="width: 50%">ASL Fingerspelling → English Translation</th>
    <th style="width: 50%">English → ASL Sign Translation</th>
  </tr>
  <tr>
    <td>Translates ASL fingerspelling into written English, which is then spoken aloud. Removes the need for Deaf individuals to translate their thoughts into English, and then write them out.</td>
    <td>Translates spoken English into ASL signs, which are then signed by a moving avatar. Removes the need for Deaf individuals to read written English and translate it into visual ASL signs.</td>
  </tr>
</table>

### Motivation

For over eight years, I tried learning multiple languages, from Sanskrit and Spanish to Hindi and French, yet I could barely maintain a fluent conversation in any of them. When I moved to Vancouver in 2021, I joined Burnaby South Secondary School, which shares its campus with the British Columbia Secondary School for the Deaf (BCSD). This gave me the unique opportunity to study a new kind of language – a visual language – in high school.

ASL wasn't like any of the other languages I had attempted to learn before: It wasn't just about words or pronunciation, but rather learning how to fully express yourself without the tools you typically use. While I still definitely wasn't the best ASL learner, our curriculum also included important aspects of Deaf culture. Over the last three years, our ASL class has shown me how I take communication for granted and also helped me notice the many hurdles that are faced by the Deaf community in our hearing-centric society. From my first week at Burnaby South to simply volunteering at our graduation ceremony, I have had a few experiences that suddenly remind me of the things I learn in ASL class and the reasons our ASL teacher teaches them. The [mission](#mission) below is ultimately what I hope to achieve with this project.

### Mission

My goal for this project has changed as I have progressed, and my vision for it has grown over time. When I initially started working on simply recognizing individual ASL alphabets, I did not expect to get very far, let alone develop something capable of sustaining two-way communication between ASL and English. Regardless, I had one main goal for the project:
- Once this project is sufficiently capable, I want to set up a desk/TV somewhere between the BCSD and Burnaby South hallways, or maybe even at the main entrance to our school. With the interface running on this device, I hope that students from BCSD and Burnaby South stop by to talk to each other without a human interpreter assisting the conversation. While this project is far from properly capturing all expressive aspects of ASL, I hope that the novelty of the fingerspell recognition and avatar visualization will bring some students together.

Now, since the project is far more capable than it previously was, my vision for it has also grown:
- I want to run an instance that is publicly accessible, so anyone in the world can just open a website and mess around with it. Ideally, it will draw more attention to ASL translation itself and people take the technology further. I also hope it encourages at least a few hearing individuals to look into ASL and consider learning the language. Maybe the platform will provide people with a fun and interactive method to learn the language.
- I also want to modularize the code and make both the receptive and expressive aspects of the project function by themselves. While this project is mostly a proof of concept, I see many potential tools arising from this concept of ASL translation, and I want to work on developing some of them. Hopefully, it will also encourage more people to develop viable accessibility technology. If you happen to be interested in developing such technology, here are some of the potential projects that I have thought of during the development process:
  - **ASL Interpreter Webcam Client:** A lightweight modular application that adds an ASL interpreter avatar to the top right of a user's webcam. It will sign all input from the microphone. This will allow people to join meetings or make YouTube videos with live English → ASL translation at no cost. This is already possible for more tech-savvy individuals, i.e. I implement it by adding an OBS Browser Source and serving a Virtual Camera.
  - **ASL YouTube Captions:** A browser extension that adds an ASL option for YouTube captions, essentially adding a 2d avatar to the top right that simply signs everything the YouTube video says. This will allow Deaf individuals to better experience YouTube videos if they prefer signs over captions.

## Language

### Translation

### American Sign Language

## Technology

### Receptive

### Expressive

## Usage

### Installation

### Execution

### Goals

### Contributing

## Future Work

## Acknowledgements
