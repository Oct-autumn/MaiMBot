import os
import requests
import aiohttp
from typing import Tuple, Union
from nonebot import get_driver

driver = get_driver()
config = driver.config

class LLMModel:
    # def __init__(self, model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", **kwargs):
    def __init__(self, model_name="Pro/deepseek-ai/DeepSeek-R1",api_using=None, **kwargs):
        if api_using == "deepseek":
            self.api_key = config.deep_seek_key
            self.base_url = config.deep_seek_base_url
            if model_name != "Pro/deepseek-ai/DeepSeek-R1":
                self.model_name = model_name
            else:
                self.model_name = "deepseek-reasoner"
        else:
            self.api_key = config.siliconflow_key
            self.base_url = config.siliconflow_base_url
            self.model_name = model_name
        self.params = kwargs

    async def generate_response(self, prompt: str) -> Tuple[str, str]:
        """根据输入的提示生成模型的响应"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建请求体
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
            **self.params
        }
        
        # 发送请求到完整的chat/completions端点
        api_url = f"{self.base_url.rstrip('/')}/chat/completions"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=data) as response:
                    response.raise_for_status()  # 检查响应状态
                    
                    result = await response.json()
                    if "choices" in result and len(result["choices"]) > 0:
                        content = result["choices"][0]["message"]["content"]
                        reasoning_content = result["choices"][0]["message"].get("reasoning_content", "")
                        return content, reasoning_content  # 返回内容和推理内容
                    return "没有返回结果", ""  # 返回两个值
                    
        except Exception as e:
            return f"请求失败: {str(e)}", ""  # 返回错误信息和空字符串

# 示例用法
if __name__ == "__main__":
    model = LLMModel()  # 默认使用 DeepSeek-V3 模型
    prompt = "你好，你喜欢我吗？"
    result, reasoning = model.generate_response(prompt)
    print("回复内容:", result)
    print("推理内容:", reasoning)