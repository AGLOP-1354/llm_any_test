import os

from dotenv import load_dotenv
from openai import OpenAI
from prompt_template import prompt_template

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=openai_api_key,
    base_url="https://api.upstage.ai/v1"
)

stream = client.chat.completions.create(
    model="solar-pro",
    messages=[
        {
            "role": "user",
            "content": prompt_template.format(url="https://www.magicaiprompts.com/docs/rag/vector-stores-llm-performance-improvement")
            # "content": """
            #     아래 사이트를 정확히 분석해서 메타 정보의 제목과 설명, 메타 정보의 이미지 url을 알려주세요. 없는 정보를 만들어내지 마세요.
            #
            #     https://www.magicaiprompts.com/docs/rag/vector-stores-llm-performance-improvement
            # """
        }
    ],
    stream=True,
    temperature=0.0
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

# Use with stream=False
# print(stream.choices[0].message.content)
# https://www.youtube.com/watch?v=wyN27QpglGE&list=RDGMEMCMFH2exzjBeE_zAHHJOdxgVMUtK0pvm1S9g&index=16
# https://www.coupang.com/vp/products/7936791669?vendorItemId=88945551412&sourceType=sdp_bottom_promotion&searchId=feed-d09c6ed1151940b8af96b0cf9c47141c-gw_promotion&isAddedCart=
# https://www.magicaiprompts.com/docs/rag/vector-stores-llm-performance-improvement