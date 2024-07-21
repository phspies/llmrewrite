from litellm import completion


class CallLLM:
    def __init__(self, model):
        self.model = model
        print("Clearing chat session history")
        self.completion("/clear")
        
    def completion(self, question):
        response = completion(
                        model=self.model,
                        system="You are a software engineer working on a project to convert rubyonrails code to python using the dhango framework",
                        messages=[{ "content": f"{question}","role": "user"}],
                        temperature=0.5,
                        stream=False
                    )
        return response.choices[0].message.content



		