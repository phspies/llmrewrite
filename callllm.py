from litellm import completion


class CallLLM:
    def __init__(self, model):
        self.model = model
    
    def completion(self, question):
        response = completion(
                        model=self.model,
                        messages=[{ "content": f"{question}","role": "user"}]
                    )
        return response.choices[0].message.content



		