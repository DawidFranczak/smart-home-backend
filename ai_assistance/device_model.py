from pathlib import Path
from threading import Lock
import torch
from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnableLambda
import json

system_prompt = """
    Jesteś asystentem smart home.
    Analizuj polecenia użytkownika w języku polskim i zwracaj WYŁĄCZNIE poprawny JSON.

    Dla każdego polecenia wyodrębnij:
        room: lista nazw pomieszczeń z {rooms} (dokładne dopasowanie, bez zgadywania)
        device: dopasowana para z listy {devices} w formacie "device_name device_type"
            - device_name: nazwa urządzenia (pierwsza część pary)
            - device_type: typ urządzenia (druga część pary)
            - jeśli polecenie nie pasuje → device_name = "NONE", device_type = "NONE"

    Zasady:
    - Dopasowuj wyłącznie elementy z podanych list
    - Brak pomieszczenia → room = []
    - Brak dopasowania urządzenia → device_type = "NONE"
    - Brak nazwy urządzenia → device_name = "NONE"

    Zwracaj listę z dokładnie jednym obiektem JSON lub pustą listę [].
    Nie dodawaj żadnego innego tekstu ani kluczy.
"""


def extract_json(text: str):
    dicts = []
    start = 0
    end = len(text)
    for idx, char in enumerate(text):
        if char == "{":
            start = idx
        if char == "}":
            end = idx
            if 0 < start < end:
                dicts.append(text[start : end + 1])

    return [json.loads(d) for d in dicts]


class DeviceModel:
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
        adapter_path = Path(__file__).resolve().parent / "models/qwen_device"
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
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            return_full_text=False,
            device="cpu",
        )
        self.llm = HuggingFacePipeline(pipeline=self.pipeline)
        self.chain = RunnableLambda(self.qwen_device_chain) | RunnableLambda(
            extract_json
        )

    def qwen_device_chain(self, inputs: dict) -> str:
        system_content = self.system_prompt.format(
            rooms=inputs["rooms"], devices=inputs["devices"]
        )
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": inputs["input"]},
        ]
        formatted_prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        output = self.llm.invoke(formatted_prompt)
        return output.strip()

    def run(self, rooms: list[str], devices: list[str], prompt: str) -> dict:
        input_data = {
            "rooms": ",".join(rooms),
            "devices": ", ".join(devices),
            "input": prompt,
        }
        response = self.chain.invoke(input_data)
        return response[0]
