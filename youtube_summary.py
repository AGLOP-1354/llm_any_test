import os
import ssl, certifi
import urllib.error

from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from prompt_template import youtube_summary_prompt_template

# HTTPS 호출에 certifi 인증서 사용
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=openai_api_key,
    base_url="https://api.upstage.ai/v1"
)


def get_script(url, language="en", add_video_info=True):
    loader = YoutubeLoader.from_youtube_url(
        "https://www.youtube.com/watch?v=TKCMw0utiak",
        add_video_info=True,
        transcript_format=TranscriptFormat.CHUNKS,
        chunk_size_seconds=30,
    )
    print("\n\n".join(map(repr, loader.load())))
    # loader = YoutubeLoader.from_youtube_url(
    #     url,
    #     add_video_info=add_video_info,
    #     # language=["en", "ko", "ja", "zh-Hans", "zh-Hant"],
    # )
    # try:
    #     return loader.load()
    # except urllib.error.HTTPError as e:
    #     print(f"[ERROR] HTTP {e.code} when fetching {url}: {e.reason}")
    #     return []
    # except Exception as e:
    #     print(f"[ERROR] Unexpected error: {e}")
    #     return []


def get_youtube_contents():
    url = "https://www.youtube.com/watch?v=6SsVuhZpaQk&list=PLraYM6paW-C1ezcpLtYaIgaij0f28rgso"
    scripts = get_script(url, "ko")
    youtube_contents = ""
    if scripts:
        youtube_contents = scripts[0].page_content
    else:
        print("스크립트를 가져올 수 없습니다.")

    return youtube_contents

youtube_contents = get_youtube_contents()
print(youtube_contents)

# prompt = """
# 아래 유튜브 컨텐츠를 요약 및 정리해주세요.
#
# {youtube_contents}
# """
#
# stream = client.chat.completions.create(
#     model="solar-pro",
#     messages=[
#         {
#             "role": "user",
#             "content": youtube_summary_prompt_template.format(youtube_contents=youtube_contents)
#         }
#     ],
#     stream=True,
#     temperature=0.0
# )
#
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")