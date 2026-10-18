#!/usr/bin/env python3
"""
Streaming NLG - 流式输出和自然语言生成模块
"""

import logging
import json
from typing import Generator, Optional, Dict, Any

logger = logging.getLogger(__name__)


class StreamingNLG:
    """
    流式NLG生成器

    功能：
    1. 流式输出LLM响应
    2. 自然语言答案生成
    3. 友好性回复
    """

    def __init__(self, api_url: str, api_key: str):
        """
        初始化

        Args:
            api_url: API地址
            api_key: API密钥
        """
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        logger.info("✅ StreamingNLG initialized")

    def generate_streaming(self, prompt: str) -> Generator[str, None, None]:
        """
        生成流式响应

        Args:
            prompt: 提示词

        Yields:
            文本片段
        """
        import requests

        # Type check must come first: a non-string has no .strip()
        if not isinstance(prompt, str):
            logger.warning(f"Non-string prompt provided: {type(prompt)}")
            yield "[Error: Invalid prompt type]"
            return
        if not prompt.strip():
            logger.warning("Empty prompt provided to generate_streaming")
            yield "[Error: Empty prompt]"
            return

        payload = {
            "model": "deepseek-v3.2-think",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "stream": True,
            "web_search": {"enable": False}
        }

        response = None
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=60
            )
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=False):
                if not line:
                    continue

                if isinstance(line, bytes):
                    line = line.decode('utf-8', errors='replace')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str == '[DONE]':
                        break

                    try:
                        data = json.loads(data_str)
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                yield content

                    except json.JSONDecodeError:
                        logger.debug(f"Skipping non-JSON line: {data_str[:50]}...")
                        continue

        except requests.exceptions.RequestException as e:
            logger.error(f"Streaming error: {e}", exc_info=True)
            yield f"[Error: {str(e)}]"
        except Exception as e:
            logger.error(f"Unexpected streaming error: {e}", exc_info=True)
            yield f"[Error: Unexpected error: {str(e)}]"
        finally:
            # Ensure the response is closed to release the connection
            if response is not None:
                response.close()

    def generate_answer(self, query: str, data: Dict[str, Any]) -> str:
        """
        从查询结果生成自然语言答案

        Args:
            query: 用户query
            data: 查询结果数据

        Returns:
            自然语言答案
        """
        import requests

        # Validate input data
        if not data or not isinstance(data, dict):
            logger.warning(f"Invalid data for NLG: {data}")
            return "抱歉，查询结果为空或格式不正确。"

        if not query or not isinstance(query, str) or not query.strip():
            logger.warning(f"Empty or invalid query provided to NLG: {type(query)}")
            return "抱歉，查询内容为空。"

        # Truncate data to prevent overly large prompts
        max_data_chars = 5000
        data_str = json.dumps(data, ensure_ascii=False, default=str)
        if len(data_str) > max_data_chars:
            data_str = data_str[:max_data_chars] + "... (truncated)"
            logger.info(f"Data truncated to {max_data_chars} chars for NLG prompt")

        nlg_prompt = f"""# Role: Financial Data Analyst

Based on the query result, provide a clear and professional answer.

Query: {query}
Result: {data_str}

Provide a concise answer (under 100 words) that:
1. Directly answers the question
2. Includes key data points
3. Is professional and friendly

Answer:"""

        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": nlg_prompt}],
            "temperature": 0.7,
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            response_json = response.json()
            if "choices" not in response_json or len(response_json["choices"]) == 0:
                logger.error("NLG response missing choices")
                return f"Based on the data, {query}"
            return response_json["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"NLG generation error: {e}")
            return f"Based on the data, {query}"