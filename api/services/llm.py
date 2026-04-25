"""
CodebaseGPT - LLM Service
Supports: MiniMax, OpenAI, Anthropic
"""
import httpx
import json
from typing import Optional, Literal
from api.config import settings


class LLMService:
    """Multi-provider LLM service"""
    
    def __init__(self, provider: Literal["minimax", "openai", "anthropic"] = "minimax"):
        self.provider = provider
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4000,
        temperature: float = 0.3,
        thinking: bool = True
    ) -> dict:
        """Generate content using the configured LLM"""
        
        if self.provider == "minimax":
            return await self._generate_minimax(prompt, system, max_tokens, temperature, thinking)
        elif self.provider == "openai":
            return await self._generate_openai(prompt, system, max_tokens, temperature)
        elif self.provider == "anthropic":
            return await self._generate_anthropic(prompt, system, max_tokens, temperature, thinking)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    async def _generate_minimax(
        self,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float,
        thinking: bool
    ) -> dict:
        """Generate using MiniMax (Anthropic-compatible API)"""
        
        messages = []
        if system:
            messages.append({"role": "user", "content": f"[System: {system}]"})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": settings.minimax_model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
        }
        
        if thinking:
            payload["thinking"] = {
                "type": "enabled",
                "budget_tokens": min(max_tokens // 2, 10000)
            }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.minimax_base_url}/v1/messages",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": settings.minimax_api_key,
                    "anthropic-version": "2023-06-01"
                },
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"LLM API error: {response.status_code} - {response.text}")
            
            return response.json()
    
    async def _generate_openai(
        self,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> dict:
        """Generate using OpenAI"""
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.openai_api_key}"
                },
                json={
                    "model": settings.openai_model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenAI API error: {response.status_code}")
            
            data = response.json()
            return {
                "content": [{"type": "text", "text": data["choices"][0]["message"]["content"]}]
            }
    
    async def _generate_anthropic(
        self,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float,
        thinking: bool
    ) -> dict:
        """Generate using Anthropic"""
        
        messages = []
        if system:
            messages.append({"role": "user", "content": f"[System: {system}]"})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": settings.anthropic_model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
        }
        
        if thinking:
            payload["thinking"] = {
                "type": "enabled",
                "budget_tokens": min(max_tokens // 2, 10000)
            }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": settings.anthropic_api_key,
                    "anthropic-version": "2023-06-01"
                },
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"Anthropic API error: {response.status_code}")
            
            return response.json()
    
    def extract_text(self, response: dict) -> str:
        """Extract text from LLM response"""
        text_parts = []
        for block in response.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
        return "\n".join(text_parts)
    
    def extract_thinking(self, response: dict) -> Optional[str]:
        """Extract thinking from LLM response"""
        for block in response.get("content", []):
            if block.get("type") == "thinking":
                return block.get("thinking", "")
        return None


# Global instances
llm = LLMService(provider="minimax")
