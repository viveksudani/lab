from openai import OpenAI


OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"

MODEL = "llama3.2"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

messages = []

while True:

    print("")
    print("User:")

    user_input = input("Your message:")

    if user_input == "":
        print("exited")
        break

    print(user_input)
    print("")

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    print("AI:")
    stream = ollama.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
    )

    ai_response = ""
    for chunk in stream:
        new_part = chunk.choices[0].delta.content or ""
        ai_response += new_part
        print(new_part, end="", flush=True)

    print("")

    messages.append(
        {
            "role": "assistant",
            "content": ai_response,
        }
    )


"""
Actual output on local machine using llama3.2 model via ollama:

User:
hi

AI:
How can I assist you today?

User:
Yes, I want some health tips for IT professionals, in 5 bullet points

AI:
Here are 5 health tips specifically tailored for IT professionals:

• **Regular Eye Exams**: Staring at screens for long periods can lead to Eye Strain and Dry Eyes. Regular eye exams (every 1-2 years) can help detect any vision problems early on, reducing the risk of chronic eye conditions.

• **Stay Hydrated**: Dehydration is common among IT professionals due to prolonged sitting and water intake neglect. Drink at least 8-10 glasses of water a day, and avoid sugary drinks that can dehydrate you further.

• **Exercise Regularly**: Sitting for long hours can lead to sedentary behavior, increasing the risk of obesity, diabetes, and cardiovascular disease. Aim for at least 30 minutes of moderate-intensity exercise (e.g., walking, jogging, or cycling) per day, and consider incorporating strength training to combat muscle fatigue.

• **Prioritize Sleep**: Sleeping is essential for physical and mental well-being. Most adults need 7-9 hours of sleep each night. Establish a consistent bedtime routine, avoid screens before bed, and create a relaxing sleep environment to improve the quality of your rest.

• **Take Breaks from Screens**: Follow the 20-20-20 rule: every 20 minutes, look away from your screen and focus on something 20 feet away for 20 seconds. This can help reduce eye strain, prevent headaches, and promote overall visibility.

I hope these tips are helpful! Do you have any specific questions about these points?

User:
Great, Thanks

AI:
I hope you find these health tips helpful in maintaining a healthy work-life balance for IT professionals. If you need anything else, feel free to ask. Have a great day!

User:
This tips are really helpful. do I need to prefer gym or yoga?

AI:
Both gym and yoga can be beneficial for IT professionals, but the choice between the two depends on your personal preferences, goals, and fitness level. Here's a brief comparison:

**Gym:**

* More intense workouts to improve cardiovascular health, strength, and muscle mass
* Can help with weight management and improving overall physical fitness
* May include high-intensity interval training (HIIT) for quick results

**Yoga:**

* Focuses on flexibility, balance, and coordination
* Can help improve posture, reduce stress, and enhance overall well-being
* Often incorporates mindfulness and breathing techniques to promote relaxation and mental calmness

Consider the following questions to help you decide between gym and yoga:

1. Do you prefer high-intensity workouts or lower-key movements?
2. Are you looking to improve your flexibility, balance, or coordination?
3. How much time do you have available for exercise? Gym sessions can be longer, while yoga classes are generally shorter.
4. Are you interested in incorporating mindfulness and relaxation techniques into your routine?

If you're new to exercise or haven't been active in a while, starting with yoga might be a great option. Yoga can help you build a stronger foundation for fitness and reduce the risk of injury. Once you're more comfortable, you can transition to gym workouts if you prefer.

Ultimately, you can also consider combining both gym and yoga to create a balanced exercise routine that suits your lifestyle and goals. Many gyms now offer yoga classes or incorporate yoga-inspired exercises into their workouts.

Which one do you think you might be interested in trying first?

User:
thanks, what about diet? explain me in 3 lines

AI:
As an IT professional, a balanced diet rich in fruits, vegetables, whole grains, and lean proteins can help maintain energy levels and focus. Limiting sugary drinks, processed snacks, and high-sodium foods can also reduce the risk of chronic diseases like obesity, diabetes, and cardiovascular disease. Aim for 3-5 main meals and 2-3 snacks per day to keep your energy levels stable throughout the workday.

User:
exited

"""