import openai

# 秘钥
openai.api_key = "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"


# 测试代码
def test_engines():
    print("Testing engines...")
    prompt = "What is the definition of a chatbot?"
    print("Prompt: " + prompt)
    completion_davinci = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("\nText-davinci-003: " + completion_davinci.choices[0].text)
    completion_gpt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("\nGPT-3.5-turbo: \n\n" + completion_gpt.choices[0].message.content)


def test_temperature():
    print("Testing temperature...")
    prompt = "What is the definition of a chatbot?"
    print("Prompt: " + prompt)
    completion_0 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.0,
    )
    print("\nTemperature 0.0: " + completion_0.choices[0].text)
    completion_05 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("\nTemperature 0.5: " + completion_05.choices[0].text)
    completion_1 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=1.0,
    )
    print("\nTemperature 1.0: " + completion_1.choices[0].text)


def test_tokens():
    print("Testing tokens...")
    prompt = "What is the definition of a chatbot?"
    print("Prompt: " + prompt)
    completion_25 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=25,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("\nTokens 25: " + completion_25.choices[0].text)
    completion_50 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("\nTokens 50: " + completion_50.choices[0].text)


def test_n():
    print("Testing n...")
    prompt = "What is the definition of a chatbot?"
    print("Prompt: " + prompt)
    completion_1 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("\nn=1: ")
    print("Answer1: " + completion_1.choices[0].text)
    completion_2 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=2,
        stop=None,
        temperature=0.5,
    )
    print("\nn=2: ")
    print("Answer1: " + completion_2.choices[0].text)
    print("\nAnswer2: " + completion_2.choices[1].text)


# test_engines()
# test_temperature()
# test_tokens()
test_n()
