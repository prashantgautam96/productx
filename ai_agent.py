"""
AI Agent for ResumeOS
=====================
Provides AI-powered enhancements:
- Bullet rewriting with strict constraints
- Enhanced keyword extraction
- Smart gap analysis and recommendations
- Role-specific optimization

Supports: OpenAI (GPT-4) and Anthropic (Claude)
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class AIConfig:
    """Configuration for AI agent"""
    provider: str = "openai"  # "openai" or "anthropic"
    model: str = "gpt-4o-mini"  # or "claude-3-haiku-20240307"
    api_key: Optional[str] = None
    enabled: bool = True
    max_tokens: int = 200
    temperature: float = 0.3  # Low temperature for consistent, factual output


class AIAgent:
    """
    AI Agent for ResumeOS Compiler
    
    Provides AI-powered enhancements while maintaining truth boundaries
    """
    
    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        
        # Load API key from environment if not provided
        if not self.config.api_key:
            if self.config.provider == "openai":
                self.config.api_key = os.getenv("OPENAI_API_KEY")
            elif self.config.provider == "anthropic":
                self.config.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        self.enabled = self.config.enabled and self.config.api_key is not None
        
        if self.enabled:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the AI client based on provider"""
        try:
            if self.config.provider == "openai":
                try:
                    import openai
                    self.client = openai.OpenAI(api_key=self.config.api_key)
                    self._call_ai = self._call_openai
                except ImportError:
                    logger.warning("openai package not installed. Install with: pip install openai")
                    self.enabled = False
            
            elif self.config.provider == "anthropic":
                try:
                    import anthropic
                    self.client = anthropic.Anthropic(api_key=self.config.api_key)
                    self._call_ai = self._call_anthropic
                except ImportError:
                    logger.warning("anthropic package not installed. Install with: pip install anthropic")
                    self.enabled = False
            else:
                raise ValueError(f"Unknown provider: {self.config.provider}")
        
        except Exception as e:
            logger.warning(f"AI agent initialization failed: {e}. Falling back to rule-based rewriting.")
            self.enabled = False
    
    def rewrite_bullet(
        self,
        original_bullet: str,
        target_role: str,
        rewrite_style: str,
        matched_keywords: List[str],
        target_keywords: List[str],
        original_technologies: List[str] = None
    ) -> str:
        """
        Rewrite a bullet point for better role alignment
        
        Args:
            original_bullet: The original bullet text
            target_role: Target role (e.g., "ai_engineer")
            rewrite_style: Style preference (e.g., "research + model building focused")
            matched_keywords: Keywords already in the bullet
            target_keywords: Keywords to emphasize
            original_technologies: Technologies mentioned in original (for validation)
        
        Returns:
            Rewritten bullet text
        """
        if not self.enabled:
            # Fallback to simple rule-based rewrite
            return self._rule_based_rewrite(original_bullet, target_role, target_keywords)
        
        prompt = self._build_rewrite_prompt(
            original_bullet,
            target_role,
            rewrite_style,
            matched_keywords,
            target_keywords,
            original_technologies or []
        )
        
        try:
            response = self._call_ai(prompt)
            rewritten = self._validate_rewrite(response, original_bullet, original_technologies or [])
            return rewritten
        except Exception as e:
            logger.warning(f"AI rewrite failed: {e}. Using rule-based fallback.")
            return self._rule_based_rewrite(original_bullet, target_role, target_keywords)
    
    def _build_rewrite_prompt(
        self,
        original_bullet: str,
        target_role: str,
        rewrite_style: str,
        matched_keywords: List[str],
        target_keywords: List[str],
        original_technologies: List[str]
    ) -> str:
        """Build the rewrite prompt with strict constraints"""
        
        # Add role-specific context for better rewriting
        role_context = {
            'ai_engineer': """For AI Engineer roles, emphasize:
- Scalable systems and infrastructure that could support ML/AI workloads
- Data processing, algorithms, and efficient computation
- System design patterns relevant to ML pipelines (e.g., event-driven architectures for data streaming)
- Performance optimization and low-latency systems (critical for ML inference)
- Distributed systems and microservices (ML systems are distributed)
- API design for ML model serving
- Database optimization for large-scale data (ML training data)
- Real-time systems and streaming (ML inference pipelines)
- Transferable skills: REST APIs → ML API design, Microservices → ML microservices, Event-driven → ML data pipelines""",
            'backend_engineer': 'Emphasize API development, system architecture, scalability, and performance optimization.',
            'devops_engineer': 'Highlight infrastructure, automation, deployment, monitoring, and reliability aspects.',
            'data_engineer': 'Focus on data pipelines, ETL processes, data quality, and scalable data systems.',
            'full_stack': 'Emphasize end-to-end development, full system ownership, and cross-functional impact.'
        }
        
        context = role_context.get(target_role.lower(), 'Emphasize technical depth and impact.')
        
        # Special instructions for AI Engineer role
        ai_specific_instructions = ""
        if target_role.lower() == 'ai_engineer':
            ai_specific_instructions = """
SPECIAL INSTRUCTIONS FOR AI ENGINEER ROLE:
- If the bullet mentions "REST APIs" or "APIs", emphasize "API design" or "service interfaces" (relevant to ML model serving)
- If the bullet mentions "microservices" or "distributed systems", emphasize how this relates to scalable ML infrastructure
- If the bullet mentions "event-driven" or "streaming", connect to "real-time data processing" (ML inference pipelines)
- If the bullet mentions "database optimization" or "query performance", emphasize "large-scale data processing" (ML training data)
- If the bullet mentions "scalable systems", add context like "scalable systems architecture" or "high-throughput systems" (ML systems need scale)
- If the bullet mentions "performance" or "latency", emphasize "low-latency systems" or "high-performance computing" (ML inference needs speed)
- Use terms like "data processing", "algorithmic efficiency", "computational systems", "scalable infrastructure" when appropriate
- Connect backend experience to ML/AI by emphasizing system design, scalability, and performance aspects
"""
        
        return f"""You are a professional resume writer specializing in ATS-optimized resumes for {target_role.replace('_', ' ').title()} roles.

TASK: Rewrite this resume bullet point to better align with a {target_role.replace('_', ' ').title()} role while maintaining truth.

ORIGINAL BULLET:
{original_bullet}

TARGET ROLE: {target_role.replace('_', ' ').title()}
ROLE CONTEXT: {context}
{ai_specific_instructions}
REWRITE STYLE: {rewrite_style}

KEYWORDS TO EMPHASIZE: {', '.join(target_keywords[:8])}
KEYWORDS ALREADY PRESENT: {', '.join(matched_keywords[:5]) if matched_keywords else 'None'}

TECHNOLOGIES IN ORIGINAL: {', '.join(original_technologies) if original_technologies else 'None specified'}

CRITICAL CONSTRAINTS (MUST FOLLOW):
1. DO NOT add any technologies, tools, or frameworks NOT in the original bullet
2. DO NOT add metrics, numbers, or achievements NOT in the original
3. DO NOT fabricate or invent any information
4. DO NOT change the core meaning or accomplishment
5. ONLY rephrase to emphasize relevance to {target_role.replace('_', ' ').title()}
6. Keep the same level of detail and specificity
7. Use active voice and strong action verbs
8. Naturally incorporate target keywords ONLY if they relate to what's already there
9. Maintain professional tone and ATS-friendly language
10. For AI Engineer: Emphasize transferable skills - backend systems → ML infrastructure, APIs → ML APIs, scalability → ML scale, performance → ML inference speed

OUTPUT REQUIREMENTS:
- Single bullet point (one line, 15-30 words)
- No bullet symbol or numbering
- Start with strong action verb
- Focus on impact and relevance to {target_role.replace('_', ' ').title()}
- Make it compelling for ATS systems
- For AI Engineer: Use terms that resonate with ML/AI work (data processing, scalable systems, high-performance, algorithmic, computational)

OUTPUT ONLY THE REWRITTEN BULLET (nothing else):"""
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": "You are a professional resume writer. Always follow the constraints exactly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        return response.choices[0].message.content.strip()
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system="You are a professional resume writer. Always follow the constraints exactly.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip()
    
    def _validate_rewrite(
        self,
        rewritten: str,
        original: str,
        original_technologies: List[str]
    ) -> str:
        """
        Validate that rewrite doesn't fabricate information
        
        Returns original if validation fails
        """
        rewritten_lower = rewritten.lower()
        original_lower = original.lower()
        
        # Check for common fabrication patterns
        fabrication_keywords = [
            "increased by", "reduced by", "improved by", "achieved",
            "led to", "resulted in", "generated", "saved"
        ]
        
        # If rewrite adds metrics not in original, reject it
        for keyword in fabrication_keywords:
            if keyword in rewritten_lower and keyword not in original_lower:
                # Check if it's followed by a number
                idx = rewritten_lower.find(keyword)
                snippet = rewritten_lower[idx:idx+30]
                if any(char.isdigit() for char in snippet):
                    # Likely fabricated metric
                    logger.warning("Potential fabrication detected. Using original.")
                    return original
        
        # Check for technology fabrication
        if original_technologies:
            tech_in_rewrite = []
            for tech in original_technologies:
                if tech.lower() in rewritten_lower and tech.lower() not in original_lower:
                    tech_in_rewrite.append(tech)
            
            # If new technologies appear, reject
            if tech_in_rewrite:
                logger.warning("New technologies detected. Using original.")
                return original
        
        # If rewrite is too different (less than 30% similarity), reject
        # Simple word overlap check
        original_words = set(original_lower.split())
        rewritten_words = set(rewritten_lower.split())
        overlap = len(original_words & rewritten_words) / max(len(original_words), 1)
        
        if overlap < 0.3:
            logger.warning("Rewrite too different from original. Using original.")
            return original
        
        return rewritten
    
    def _rule_based_rewrite(
        self,
        bullet: str,
        target_role: str,
        target_keywords: List[str]
    ) -> str:
        """Fallback rule-based rewrite"""
        # Simple keyword emphasis
        bullet_lower = bullet.lower()
        for keyword in target_keywords[:3]:
            if keyword.lower() in bullet_lower:
                # Already has keyword, return as-is
                return bullet
        
        # If no keywords match, return original
        # (Rule-based can't safely add keywords)
        return bullet
    
    def enhance_keyword_extraction(
        self,
        job_description: str,
        extracted_keywords: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Use AI to enhance keyword extraction
        
        Can identify synonyms, related terms, and context
        """
        if not self.enabled:
            return extracted_keywords
        
        try:
            prompt = f"""Extract and enhance keywords from this job description for ATS matching.

JOB DESCRIPTION:
{job_description[:1000]}

CURRENTLY EXTRACTED:
Required Skills: {', '.join(extracted_keywords.get('required_skills', [])[:10])}
Tools: {', '.join(extracted_keywords.get('tools', [])[:10])}

TASK:
1. Identify any missing critical skills or tools
2. Suggest synonyms or related terms for existing keywords
3. Identify domain-specific terminology
4. List technologies mentioned in context

OUTPUT JSON format:
{{
  "additional_required_skills": ["skill1", "skill2"],
  "synonyms": {{"original": "synonym"}},
  "domain_terms": ["term1", "term2"],
  "technologies": ["tech1", "tech2"]
}}

OUTPUT ONLY VALID JSON:"""
            
            response = self._call_ai(prompt)
            
            # Parse JSON response
            try:
                enhanced = json.loads(response)
                
                # Merge enhancements
                if enhanced.get("additional_required_skills"):
                    extracted_keywords["required_skills"].extend(
                        enhanced["additional_required_skills"]
                    )
                
                if enhanced.get("technologies"):
                    extracted_keywords["tools"].extend(enhanced["technologies"])
                
            except json.JSONDecodeError:
                # If AI doesn't return valid JSON, return original
                pass
        
        except Exception as e:
            logger.warning(f"AI keyword enhancement failed: {e}")
        
        return extracted_keywords
    
    def generate_smart_recommendations(
        self,
        master_resume: Dict[str, Any],
        job_description: str,
        gap_analysis: Dict[str, Any]
    ) -> List[str]:
        """
        Generate AI-powered recommendations for improving match score
        """
        if not self.enabled:
            return gap_analysis.get("recommendations", [])
        
        try:
            prompt = f"""Analyze this resume gap analysis and provide actionable recommendations.

JOB DESCRIPTION (excerpt):
{job_description[:500]}

CURRENT RESUME SKILLS:
{', '.join([s.get('name', '') for s in master_resume.get('skills', [])[:15]])}

MISSING REQUIRED SKILLS:
{', '.join(gap_analysis.get('missing_required_skills', [])[:10])}

MATCH SCORE: {gap_analysis.get('match_score', 0) * 100:.1f}%

TASK: Provide 3-5 specific, actionable recommendations to improve the match score.

Focus on:
1. Skills that can be added based on existing experience
2. How to reframe existing experience to highlight relevant skills
3. Projects or experiences that could be emphasized differently
4. Keywords to naturally incorporate

OUTPUT: JSON array of recommendation strings
["recommendation 1", "recommendation 2", ...]

OUTPUT ONLY VALID JSON ARRAY:"""
            
            response = self._call_ai(prompt)
            
            try:
                recommendations = json.loads(response)
                if isinstance(recommendations, list):
                    return recommendations[:5]  # Limit to 5
            except json.JSONDecodeError:
                pass
        
        except Exception as e:
            logger.error(f"AI recommendations failed: {e}", exc_info=True)
        
        # Fallback to existing recommendations
        return gap_analysis.get("recommendations", [])


# ========== CONVENIENCE FUNCTIONS ==========

def create_ai_agent(
    provider: str = "openai",
    api_key: Optional[str] = None,
    enabled: bool = True
) -> AIAgent:
    """
    Create an AI agent with default configuration
    
    Usage:
        agent = create_ai_agent(provider="openai", api_key="sk-...")
        rewritten = agent.rewrite_bullet(...)
    """
    config = AIConfig(
        provider=provider,
        api_key=api_key,
        enabled=enabled
    )
    return AIAgent(config)
