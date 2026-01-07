from pathlib import Path
from threading import Lock
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnableLambda
import re
import json
from peft import PeftModel
import torch

system_prompt = """
    Jesteś asystentem smart home.
    Twoim zadaniem jest analiza poleceń użytkownika w języku polskim i zwrócenie WYŁĄCZNIE poprawnej listy JSON-a.
    Dozwolone intencje to: {intents}.
    Jeśli polecenie nie pasuje do żadnej z obsługiwanych akcji, użyj intentu NONE.
    Zawsze zwracaj listę obiektów JSON.
    Nie dodawaj żadnego tekstu poza JSON.
    Nie dodawaj żadnego tekstu ani słów, nawet do pola prompt.
    Formatuj odpowiedź:[{{"intent": ... "prompt": ...}},...]
"""


def extract_json(text: str):
    match = re.search(r"(\[\s*\{.*\}\s*\])", text, re.S)
    if not match:
        raise ValueError("Model didn't return JSON.")
    return json.loads(match.group(1))


class IntentModel:
    _instance = None
    _lock = Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        base_model_id = "Qwen/Qwen2.5-0.5B-Instruct"
        adapter_path = Path(__file__).resolve().parent / "models/qwen_intent"
        adapter_path_str = str(adapter_path)

        print(f"Loading base model: {base_model_id}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_id,
            local_files_only=True,
            trust_remote_code=True,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            local_files_only=True,
            trust_remote_code=True,
            token=None,
            dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        )

        print(f"Loading LoRA adapter: {adapter_path_str}")
        self.model = PeftModel.from_pretrained(self.model, adapter_path_str)
        print("LoRA adapter loaded")

        self.system_prompt = system_prompt
        print("Creating pipeline...")
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            return_full_text=False,
            device="cpu",
        )
        self.llm = HuggingFacePipeline(pipeline=self.pipe)
        self.system_prompt = system_prompt
        self.chain = RunnableLambda(self.qwen_intent_chain) | RunnableLambda(
            extract_json
        )

    def qwen_intent_chain(self, inputs: dict) -> str:
        input_text = inputs["input_text"]
        available_intents = inputs["available_intents"]
        system_content = system_prompt.format(intents=", ".join(available_intents))
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": input_text},
        ]
        formatted_prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        output = self.llm.invoke(formatted_prompt)
        return output.strip()

    def run(self, intents: list[str], prompt: str) -> dict:
        response = self.chain.invoke(
            {"input_text": prompt, "available_intents": intents}
        )
        return response
