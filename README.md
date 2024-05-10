https://github.com/kevinjosethomas/sign-language-translation/assets/46242684/8d3778e4-661b-45a5-a3f0-06d28fdde9b4

# ✌️ ASL ⭤ English Translation with MediaPipe, PointNet, ThreeJS and Semantic Search

American Sign Language (ASL) is a complete, natural language that exhibits the same linguistic complexities as spoken languages, including its own syntax, morphology, and grammar that significantly differ from English. Most existing tools that aim to bridge ASL and English often prioritize the needs of hearing individuals, simply offering Text-to-Speech (TTS) and Speech-to-Text capabilities (STT), developed under the misconception that ASL is an identical language to English. When Deafness is viewed as a "disability", most of these *translation* tools are developed to assist with the inability to hear, but not to assist with the actual translation process. See the [language section](#language) below.

This project is a prototype that enables translation between American Sign Language (ASL) and English, facilitating communication between ASL signers and individuals who do not understand ASL. It is still far from fully translating the nuances of visual language, but it is designed to respect and preserve ASL as the primary language. The interface provides two main functionalities:

<table style="width: 100%">
  <tr>
    <th style="width: 50%">ASL Fingerspelling → English Translation</th>
    <th style="width: 50%">English → ASL Sign Translation</th>
  </tr>
  <tr>
    <td>Translates ASL fingerspelling into written English, which is then spoken aloud. Removes the need for Deaf individuals to translate their thoughts into English, and then write them out.</td>
    <td>Translates spoken English into ASL signs, which are then signed by a moving avatar. Removes the need for Deaf individuals to read written English, and then translate it into visual language.</td>
  </tr>
</table>

> [!NOTE]
> As a hearing student with limited ASL proficiency, I recognize that my perspective as a hearing person is limited. This project would not have been possible without the active involvement and advice of Deaf individuals and ASL experts who have generously shared their insights. My role has been to listen carefully and integrate feedback from the Deaf community, and I have done my best to approach this project with a mindset of learning and understanding, rather than assuming. 

### Motivation

For over eight years, I tried learning multiple languages, from Sanskrit and Spanish to Hindi and French, yet I could barely maintain a fluent conversation in any of them. When I moved to Vancouver in 2021, I joined Burnaby South Secondary School, which shares its campus with the British Columbia Secondary School for the Deaf (BCSD). This gave me the unique opportunity to study a new kind of language – a visual language – in high school.

ASL wasn't like any of the other languages I had attempted to learn before: It wasn't just about words or pronunciation, but rather learning how to fully express yourself without the tools you typically use. While I still definitely wasn't the best ASL learner, our curriculum also included important aspects of Deaf culture. Over the last three years, our ASL class has shown me how I take communication for granted and also helped me notice the many hurdles that are faced by the Deaf community in our hearing-centric society. From my very first week at Burnaby South, I have had a few experiences that suddenly remind me of the things I learn in ASL class and the reasons our ASL teacher teaches them. The [mission](#mission) below is ultimately what I hope to achieve with this project.

### Mission

My goal for this project has changed as I have progressed, and my vision for it has grown over time. When I initially started working on simply recognizing individual ASL alphabets, I did not expect to get very far, let alone develop something capable of sustaining two-way communication between ASL and English. Regardless, I had one main goal for the project:
- Once this project is sufficiently capable, I want to set up a desk/TV somewhere between the BCSD and Burnaby South hallways, or maybe even at the main entrance to our school. With the interface running on this device, I hope that students from BCSD and Burnaby South stop by to talk to each other without a human interpreter assisting the conversation. While this project is far from properly capturing all expressive aspects of ASL, I hope that the novelty of the fingerspell recognition and avatar visualization will bring some students together.

Now, since the project is far more capable than it previously was, my vision for it has also grown:
- I want to run an instance that is publicly accessible, so anyone in the world can just open a website and mess around with it. Ideally, it will draw more attention to ASL translation itself and people take the technology further. I also hope it encourages at least a few hearing individuals to look into ASL and consider learning the language. Maybe the platform will provide people with a fun and interactive method to learn the language.
- I also want to modularize the code and make both the receptive and expressive aspects of the project function by themselves. While this project is mostly a proof of concept, I see many potential tools arising from this concept of ASL translation, and I want to work on developing some of them. Hopefully, it will also encourage more people to develop viable accessibility technology. If you happen to be interested in developing such technology, here are some of the potential projects that I have thought of during the development process:
  - **ASL Interpreter Webcam Client:** A lightweight modular application that adds an ASL interpreter avatar to the top right of a user's webcam. It will sign all input from the microphone. This will allow people to join meetings or make YouTube videos with live English → ASL translation at no cost. This is already possible for more tech-savvy individuals, i.e. I implement it by adding an OBS Browser Source and serving a Virtual Camera.
  - **ASL YouTube Captions:** A browser extension that adds an ASL option for YouTube captions, essentially adding a 2d avatar to the top right that simply signs everything the YouTube video says. This will allow Deaf individuals to better experience YouTube videos if they prefer signs over captions.

## Language

Below, on the left is the typical flow of conversation between two people speaking the same language. On the right is the typical flow of a conversation between two individuals who speak different languages. In between them, is either a tool that can translate between the two languages (Google Translate) or a person who knows both languages and serves as a translator. This is also the role an ASL interpreter plays in a typical conversation between a Deaf and hearing individual.

<img height="204" src="https://github.com/kevinjosethomas/sign-language-translation/assets/46242684/17ae9b66-0005-4f37-95f4-dddd168d582f" />
<img height="204" src="https://github.com/kevinjosethomas/sign-language-translation/assets/46242684/43a07102-7a0b-4115-b75d-3b6131d44a7b" />
&ensp;

In contrast, below is the typical flow of conversation between a Deaf and hearing individual when an interpreter is not present. The most commonly utilized process is writing/typing to communicate, or using a TTS/STT tool that assists the hearing individual.

<img src="https://github.com/kevinjosethomas/sign-language-translation/assets/46242684/966b5fb3-9ba5-47ee-b6b9-db977c3bf2d9" />
&ensp;

The idea that ASL is merely a visual representation of English is a widespread misconception. In reality, ASL is a distinct language with its own syntax, grammar, and cultural nuances that differ significantly from spoken English. Most existing direct translation tools, similar to the writing/typing translation process I visualized above, are built with this understanding, failing to capture the depth of ASL communication. Furthermore, these tools put an even larger burden on the Deaf individual, requiring them to accommodate and adapt to meet the needs of the hearing individual.

Imagine speaking English and not being able to hear what you say. While some ASL signers do have a grasp of English, it is not their first language, and it is often incredibly hard to constantly translate thoughts from ASL into English, and vice-versa. Essentially, most of these translation tools simply transcribe text, and don't serve any real "translation" purpose. They are built to assist deafness as a disability, but not as a culture or as a language. 

On the left, I added a visual of the 5 fundamental parameters that define ASL, as well as some examples of each (there are hundreds!). On the right, I added an example of the grammatical difference between the same sentence in English and in ASL. I would recommend reading about ASL parameters [here](https://www.handspeak.com/learn/397/), and also about [ASL Gloss](https://www.handspeak.com/learn/3/) and [Grammar](https://www.handspeak.com/learn/37/).

<img height="365" src="https://github.com/kevinjosethomas/sign-language-translation/assets/46242684/ad00cf3c-9690-4f1d-8cd5-c6f0ae645b0b" />

<img height="365" src="https://github.com/kevinjosethomas/sign-language-translation/assets/46242684/fe4514ae-879d-4cb9-80c6-65ec6955eb22" />
&ensp;

The goal of this project has been to slowly eliminate the extra steps that Deaf people have to take because of how hearing-centric our society is. From the 4 extra steps visualized above, our tool eliminates three 3 steps to a sufficient degree. Here is the corresponding flow below:

<img src="https://github.com/kevinjosethomas/sign-language-translation/assets/46242684/b459cabf-850e-449b-9e0a-8c6086be7ba3" />

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
