"""
ResumeOS Compiler Engine
========================
The core "brain" that transforms master resume + job description → tailored resume

Pipeline:
    1. JD Keyword Extraction
    2. Role Lens Selection
    3. Relevance Scoring + Ranking
    4. Controlled Bullet Rewrite (AI or rule-based)
    5. Tailored Resume JSON Output
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RoleType(Enum):
    """Supported role lenses"""
    AI_ENGINEER = "ai_engineer"
    BACKEND_ENGINEER = "backend_engineer"
    DEVOPS_ENGINEER = "devops_engineer"
    FULL_STACK = "full_stack"
    DATA_ENGINEER = "data_engineer"


@dataclass
class ExtractedKeywords:
    """Keywords extracted from job description"""
    role: RoleType
    required_skills: List[str]
    preferred_skills: List[str]
    tools: List[str]
    concepts: List[str]
    
    def all_keywords(self) -> List[str]:
        """Get all keywords as flat list"""
        return (self.required_skills + self.preferred_skills + 
                self.tools + self.concepts)


@dataclass
class RoleLens:
    """Configuration for a specific role lens"""
    role_type: RoleType
    priority_tags: List[str]
    rewrite_style: str
    keyword_boost_multiplier: float = 2.0
    tag_match_weight: float = 1.5


@dataclass
class ScoredBullet:
    """A bullet with relevance score"""
    original_text: str
    score: float
    matched_keywords: List[str]
    matched_tags: List[str]
    bullet_id: str


class ResumeCompiler:
    """
    The Resume Compiler Engine
    
    Transforms master resume into role-optimized projection
    """
    
    def __init__(self, ai_agent=None):
        self.role_lenses = self._initialize_role_lenses()
        self.ai_agent = ai_agent  # Optional AI agent for bullet rewriting
    
    def _initialize_role_lenses(self) -> Dict[RoleType, RoleLens]:
        """Initialize predefined role lens configurations"""
        return {
            RoleType.AI_ENGINEER: RoleLens(
                role_type=RoleType.AI_ENGINEER,
                priority_tags=["ai", "ml", "cv", "nlp", "deep-learning", "pytorch", "tensorflow"],
                rewrite_style="research + model building focused"
            ),
            RoleType.BACKEND_ENGINEER: RoleLens(
                role_type=RoleType.BACKEND_ENGINEER,
                priority_tags=["backend", "distributed-systems", "api", "microservices", "database"],
                rewrite_style="scalability + architecture focused"
            ),
            RoleType.DEVOPS_ENGINEER: RoleLens(
                role_type=RoleType.DEVOPS_ENGINEER,
                priority_tags=["devops", "ci-cd", "kubernetes", "docker", "aws", "infrastructure"],
                rewrite_style="automation + infrastructure focused"
            ),
            RoleType.FULL_STACK: RoleLens(
                role_type=RoleType.FULL_STACK,
                priority_tags=["frontend", "backend", "api", "react", "fullstack"],
                rewrite_style="end-to-end product focused"
            ),
            RoleType.DATA_ENGINEER: RoleLens(
                role_type=RoleType.DATA_ENGINEER,
                priority_tags=["data-pipeline", "etl", "sql", "spark", "airflow", "data-warehouse"],
                rewrite_style="data pipeline + analytics focused"
            )
        }
    
    # ========== PASS 1: JD KEYWORD EXTRACTION ==========
    
    def extract_keywords_from_jd(self, job_description: str) -> ExtractedKeywords:
        """
        Pass 1: Extract keywords from job description
        
        Uses pattern matching + keyword lists to identify:
        - Required skills
        - Preferred skills  
        - Tools/technologies
        - Key concepts
        """
        jd_lower = job_description.lower()
        
        # Detect role type
        role = self._detect_role_type(jd_lower)
        
        # Keyword banks for extraction
        skill_keywords = {
            'python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++',
            'react', 'vue', 'angular', 'node.js', 'express', 'fastapi', 'django',
            'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'machine learning', 'deep learning', 'ml', 'ai', 'nlp', 'natural language processing',
            'computer vision', 'cv', 'object detection', 'yolo', 'r-cnn', 'rcnn',
            'tensorflow', 'pytorch', 'scikit-learn', 'scikit learn', 'opencv',
            'mlops', 'model deployment', 'model serving', 'model monitoring',
            'real-time', 'realtime', 'video processing', 'image processing',
            'aws', 'gcp', 'azure', 'kubernetes', 'docker',
            'ci/cd', 'jenkins', 'github actions', 'terraform',
            'rest api', 'graphql', 'grpc', 'microservices',
            'distributed systems', 'system design', 'scalability'
        }
        
        # Extract present keywords - use word boundaries for better matching
        found_keywords = []
        for kw in skill_keywords:
            # Use word boundary matching for better accuracy
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, jd_lower, re.IGNORECASE):
                found_keywords.append(kw)
        
        # Also extract capitalized technology names (TensorFlow, PyTorch, YOLO, etc.)
        tech_names = re.findall(r'\b([A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+)*)\b', job_description)
        for tech in tech_names:
            tech_lower = tech.lower()
            if tech_lower not in found_keywords and len(tech) > 2:
                # Check if it's a known technology
                if any(known in tech_lower for known in ['tensorflow', 'pytorch', 'opencv', 'yolo', 'r-cnn', 'rcnn', 'fastapi', 'aws', 'gcp', 'azure']):
                    found_keywords.append(tech_lower)
        
        # Categorize keywords
        required = self._extract_required_skills(jd_lower, found_keywords)
        preferred = [kw for kw in found_keywords if kw not in required]
        
        # Log extracted keywords (debug level)
        logger.debug(f"Extracted {len(found_keywords)} keywords from JD")
        logger.debug(f"Required skills: {required[:10]}")
        logger.debug(f"Preferred skills: {preferred[:10]}")
        
        tools = self._extract_tools(found_keywords)
        concepts = self._extract_concepts(found_keywords)
        
        return ExtractedKeywords(
            role=role,
            required_skills=required,
            preferred_skills=preferred,
            tools=tools,
            concepts=concepts
        )
    
    def _detect_role_type(self, jd_text: str) -> RoleType:
        """Detect role type from job description"""
        role_patterns = {
            RoleType.AI_ENGINEER: ['machine learning', 'ai engineer', 'ml engineer', 
                                   'deep learning', 'computer vision', 'nlp'],
            RoleType.BACKEND_ENGINEER: ['backend', 'backend engineer', 'server side',
                                       'api development', 'microservices'],
            RoleType.DEVOPS_ENGINEER: ['devops', 'sre', 'infrastructure', 'ci/cd',
                                       'kubernetes', 'cloud'],
            RoleType.FULL_STACK: ['full stack', 'fullstack', 'full-stack'],
            RoleType.DATA_ENGINEER: ['data engineer', 'data pipeline', 'etl', 
                                    'data warehouse', 'big data']
        }
        
        for role_type, patterns in role_patterns.items():
            if any(pattern in jd_text for pattern in patterns):
                return role_type
        
        return RoleType.BACKEND_ENGINEER  # Default
    
    def _extract_required_skills(self, jd_text: str, all_keywords: List[str]) -> List[str]:
        """Extract required vs preferred skills - enhanced to capture all skills"""
        required = []
        
        # Look for "required" section patterns
        required_section_match = re.search(
            r'(required|requirements|must have|qualifications?)(.*?)(?=preferred|nice to have|bonus|$|required)',
            jd_text,
            re.IGNORECASE | re.DOTALL
        )
        
        if required_section_match:
            required_text = required_section_match.group(2).lower() if required_section_match.lastindex >= 2 else required_section_match.group(0).lower()
            # Extract all keywords mentioned in required section
            required = [kw for kw in all_keywords if kw in required_text]
            
            # Also extract skills mentioned with bullet points or dashes
            bullet_pattern = r'[-•*]\s*([^:\n]+?)(?:\s*[:]|$)'
            bullet_matches = re.findall(bullet_pattern, required_text, re.IGNORECASE)
            for match in bullet_matches:
                match_lower = match.lower().strip()
                # Check if it contains any known skill keywords
                for kw in all_keywords:
                    if kw in match_lower and kw not in required:
                        required.append(kw)
                # Also extract technology names (capitalized words, frameworks)
                tech_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
                tech_matches = re.findall(tech_pattern, match)
                for tech in tech_matches:
                    tech_lower = tech.lower()
                    if tech_lower in all_keywords and tech_lower not in required:
                        required.append(tech_lower)
        
        return required if required else all_keywords[:5]  # Top 5 as required if unclear
    
    def _extract_tools(self, keywords: List[str]) -> List[str]:
        """Filter out tool/technology keywords"""
        tool_patterns = ['aws', 'docker', 'kubernetes', 'postgresql', 'mongodb', 
                        'redis', 'tensorflow', 'pytorch', 'opencv', 'react', 'vue']
        return [kw for kw in keywords if any(tp in kw for tp in tool_patterns)]
    
    def _extract_concepts(self, keywords: List[str]) -> List[str]:
        """Filter out concept keywords"""
        concept_patterns = ['machine learning', 'distributed systems', 'microservices',
                          'deep learning', 'system design', 'scalability']
        return [kw for kw in keywords if any(cp in kw for cp in concept_patterns)]
    
    # ========== PASS 2: ROLE LENS SELECTION ==========
    
    def select_role_lens(self, role: RoleType) -> RoleLens:
        """Pass 2: Select appropriate role lens configuration"""
        return self.role_lenses.get(role, self.role_lenses[RoleType.BACKEND_ENGINEER])
    
    # ========== PASS 3: RELEVANCE SCORING + RANKING ==========
    
    def score_and_rank_bullets(
        self,
        bullets: List[Dict[str, Any]],
        keywords: ExtractedKeywords,
        role_lens: RoleLens
    ) -> List[ScoredBullet]:
        """
        Pass 3: Score each bullet based on relevance
        
        Score = keyword_overlap + tag_match_weight + role_priority_bonus
        """
        scored_bullets = []
        all_keywords_lower = [kw.lower() for kw in keywords.all_keywords()]
        
        for bullet in bullets:
            bullet_text = bullet.get('text', '').lower()
            bullet_tags = [tag.lower() for tag in bullet.get('tags', [])]
            bullet_id = bullet.get('id', '')
            
            # Calculate keyword overlap
            matched_keywords = [
                kw for kw in all_keywords_lower 
                if kw in bullet_text
            ]
            keyword_score = len(matched_keywords) * role_lens.keyword_boost_multiplier
            
            # Calculate tag match
            matched_tags = [
                tag for tag in bullet_tags 
                if tag in role_lens.priority_tags
            ]
            tag_score = len(matched_tags) * role_lens.tag_match_weight
            
            # Role priority bonus
            priority_bonus = 0
            if any(tag in role_lens.priority_tags[:3] for tag in bullet_tags):
                priority_bonus = 2.0
            
            total_score = keyword_score + tag_score + priority_bonus
            
            scored_bullets.append(ScoredBullet(
                original_text=bullet.get('text', ''),
                score=total_score,
                matched_keywords=matched_keywords,
                matched_tags=matched_tags,
                bullet_id=bullet_id
            ))
        
        # Sort by score descending
        scored_bullets.sort(key=lambda x: x.score, reverse=True)
        return scored_bullets
    
    def score_projects(
        self,
        projects: List[Dict[str, Any]],
        keywords: ExtractedKeywords,
        role_lens: RoleLens
    ) -> List[Dict[str, Any]]:
        """Score and rank projects"""
        scored_projects = []
        all_keywords_lower = [kw.lower() for kw in keywords.all_keywords()]
        
        for project in projects:
            project_name = project.get('name', '').lower()
            project_desc = ' '.join(project.get('bullets', [])).lower()
            project_tags = [tag.lower() for tag in project.get('tags', [])]
            
            full_text = f"{project_name} {project_desc}"
            
            # Keyword matching
            matched_keywords = [kw for kw in all_keywords_lower if kw in full_text]
            keyword_score = len(matched_keywords) * 1.5
            
            # Tag matching
            matched_tags = [tag for tag in project_tags if tag in role_lens.priority_tags]
            tag_score = len(matched_tags) * 2.0
            
            total_score = keyword_score + tag_score
            
            scored_projects.append({
                **project,
                'relevance_score': total_score,
                'matched_keywords': matched_keywords,
                'matched_tags': matched_tags
            })
        
        scored_projects.sort(key=lambda x: x['relevance_score'], reverse=True)
        return scored_projects
    
    # ========== PASS 4: CONTROLLED BULLET REWRITE ==========
    
    def generate_rewrite_prompt(
        self,
        bullet: ScoredBullet,
        role_lens: RoleLens,
        keywords: ExtractedKeywords
    ) -> str:
        """
        Generate AI rewrite prompt with strict constraints
        
        This ensures AI only rephrases within truth boundaries
        """
        prompt = f"""Rewrite this resume bullet for a {role_lens.role_type.value} role.

ORIGINAL BULLET:
{bullet.original_text}

TARGET ROLE: {role_lens.role_type.value}
REWRITE STYLE: {role_lens.rewrite_style}

MATCHED KEYWORDS: {', '.join(bullet.matched_keywords)}
TARGET KEYWORDS TO EMPHASIZE: {', '.join(keywords.required_skills[:5])}

STRICT CONSTRAINTS:
1. Do NOT add new technologies or tools not in the original
2. Do NOT add metrics or numbers not in the original
3. Do NOT fabricate achievements
4. ONLY rephrase to emphasize relevance to {role_lens.role_type.value}
5. Keep the core truth intact
6. Naturally incorporate matched keywords where they already exist

OUTPUT: Single rewritten bullet point (one line, no bullet symbol)
"""
        return prompt
    
    # ========== PASS 5: TAILORED RESUME JSON OUTPUT ==========
    
    def compile(
        self,
        master_resume: Dict[str, Any],
        job_description: str,
        role_override: Optional[RoleType] = None
    ) -> Dict[str, Any]:
        """
        Main compiler pipeline
        
        Input: Master resume JSON + Job description
        Output: Tailored resume JSON
        """
        
        # Pass 1: Extract keywords
        keywords = self.extract_keywords_from_jd(job_description)
        
        # Pass 2: Select role lens
        target_role = role_override if role_override else keywords.role
        role_lens = self.select_role_lens(target_role)
        
        # Pass 3: Score and rank experience bullets - PROCESS ALL EXPERIENCES
        all_experience_bullets = []
        experience_bullet_map = {}  # Map experience index to its bullets
        
        for exp_idx, exp in enumerate(master_resume.get('experience', []), 1):
            bullets = exp.get('bullets', [])
            scored = self.score_and_rank_bullets(bullets, keywords, role_lens)
            
            # Pass 4: AI-powered bullet rewriting (if AI agent available)
            if self.ai_agent and self.ai_agent.enabled:
                for bullet in scored:
                    # Extract technologies from original bullet
                    original_techs = self._extract_technologies_from_text(bullet.original_text)
                    
                    # Rewrite bullet with AI
                    rewritten = self.ai_agent.rewrite_bullet(
                        original_bullet=bullet.original_text,
                        target_role=target_role.value,
                        rewrite_style=role_lens.rewrite_style,
                        matched_keywords=bullet.matched_keywords,
                        target_keywords=keywords.required_skills[:5],
                        original_technologies=original_techs
                    )
                    # Update bullet text with rewritten version
                    bullet.original_text = rewritten
            
            all_experience_bullets.extend(scored)
            experience_bullet_map[exp_idx] = scored  # Store bullets by experience index
        
        # Rank experiences by best bullet score - INCLUDE ALL EXPERIENCES
        ranked_experiences = []
        for exp_idx, exp in enumerate(master_resume.get('experience', []), 1):
            # Use the bullet map we created (most reliable)
            exp_bullets = experience_bullet_map.get(exp_idx, [])
            
            # Fallback: Try to match by bullet ID prefix
            if not exp_bullets:
                exp_id_prefix = f"exp{exp_idx}"
                exp_bullets = [b for b in all_experience_bullets 
                              if b.bullet_id.startswith(exp_id_prefix + "_")]
            
            # Fallback 2: Try matching by company/role (for parsed resumes)
            if not exp_bullets:
                exp_company = exp.get('company', '').lower()
                exp_role = exp.get('role', '').lower()
                # Find bullets that might belong to this experience
                for bullet in all_experience_bullets:
                    bullet_text_lower = bullet.original_text.lower()
                    # If bullet mentions company or role, it might belong
                    if exp_company and exp_company in bullet_text_lower:
                        if bullet not in exp_bullets:
                            exp_bullets.append(bullet)
                    elif exp_role and exp_role in bullet_text_lower and len(exp_role) > 3:
                        if bullet not in exp_bullets:
                            exp_bullets.append(bullet)
            
            if exp_bullets:
                max_score = max(b.score for b in exp_bullets)
                # Include more bullets (up to 6) to ensure content is present
                ranked_experiences.append({
                    **exp,
                    'relevance_score': max_score,
                    'ranked_bullets': exp_bullets[:6]  # Top 6 bullets per experience
                })
            else:
                # Fallback: include experience even if no bullets matched (with original bullets)
                original_bullets = exp.get('bullets', [])
                if original_bullets:
                    # Create scored bullets from original (with low score)
                    fallback_bullets = []
                    for bullet_idx, bullet in enumerate(original_bullets[:6], 1):  # Take up to 6 original bullets
                        bullet_text = bullet.get('text', '') if isinstance(bullet, dict) else bullet
                        if bullet_text:
                            # Rewrite with AI if available, even for fallback bullets
                            if self.ai_agent and self.ai_agent.enabled:
                                try:
                                    original_techs = self._extract_technologies_from_text(bullet_text)
                                    rewritten = self.ai_agent.rewrite_bullet(
                                        original_bullet=bullet_text,
                                        target_role=target_role.value,
                                        rewrite_style=role_lens.rewrite_style,
                                        matched_keywords=[],
                                        target_keywords=keywords.required_skills[:5],
                                        original_technologies=original_techs
                                    )
                                    bullet_text = rewritten
                                except:
                                    pass  # Use original if rewrite fails
                            
                            fallback_bullets.append(ScoredBullet(
                                original_text=bullet_text,
                                score=0.1,  # Low score but included
                                matched_keywords=[],
                                matched_tags=[],
                                bullet_id=bullet.get('id', '') if isinstance(bullet, dict) else f"{exp_id_prefix}_b{bullet_idx}"
                            ))
                    if fallback_bullets:
                        ranked_experiences.append({
                            **exp,
                            'relevance_score': 0.1,
                            'ranked_bullets': fallback_bullets
                        })
        
        # Sort by relevance but KEEP ALL experiences
        ranked_experiences.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Score and rank projects
        ranked_projects = self.score_projects(
            master_resume.get('projects', []),
            keywords,
            role_lens
        )
        
        # Filter and rank skills
        ranked_skills = self._rank_skills(
            master_resume.get('skills', []),
            keywords,
            role_lens
        )
        
        # Calculate match score
        match_score = self._calculate_match_score(
            ranked_skills,
            ranked_experiences,
            ranked_projects,
            keywords
        )
        
        # CRITICAL: ALWAYS INCLUDE ALL EXPERIENCES AND PROJECTS
        # Build final_experiences from ALL master resume experiences
        final_experiences = []
        master_experiences = master_resume.get('experience', [])
        
        # Create a map of (company, role) -> ranked experience for quick lookup
        ranked_exp_map = {}
        for exp in ranked_experiences:
            key = (exp.get('company', ''), exp.get('role', ''))
            ranked_exp_map[key] = exp
        
        # Include ALL experiences from master resume
        for exp in master_experiences:
            key = (exp.get('company', ''), exp.get('role', ''))
            if key in ranked_exp_map:
                # Use ranked version (with scored bullets)
                final_experiences.append(ranked_exp_map[key])
            else:
                # Experience not in ranked list - add it with original bullets
                original_bullets = exp.get('bullets', [])
                fallback_bullets = []
                for bullet in original_bullets[:6]:
                    bullet_text = bullet.get('text', '') if isinstance(bullet, dict) else bullet
                    if bullet_text:
                        # AI rewrite if enabled
                        if self.ai_agent and self.ai_agent.enabled:
                            try:
                                original_techs = self._extract_technologies_from_text(bullet_text)
                                rewritten = self.ai_agent.rewrite_bullet(
                                    original_bullet=bullet_text,
                                    target_role=target_role.value,
                                    rewrite_style=role_lens.rewrite_style,
                                    matched_keywords=[],
                                    target_keywords=keywords.required_skills[:5],
                                    original_technologies=original_techs
                                )
                                bullet_text = rewritten
                            except:
                                pass
                        fallback_bullets.append(ScoredBullet(
                            original_text=bullet_text,
                            score=0.1,
                            matched_keywords=[],
                            matched_tags=[],
                            bullet_id=bullet.get('id', '') if isinstance(bullet, dict) else f"exp{len(final_experiences)+1}_b{len(fallback_bullets)+1}"
                        ))
                if fallback_bullets or original_bullets:  # Include even if no bullets
                    final_experiences.append({
                        **exp,
                        'relevance_score': 0.1,
                        'ranked_bullets': fallback_bullets
                    })
        
        # Sort by relevance but KEEP ALL
        final_experiences.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Include ALL projects from master resume
        final_projects = []
        master_projects = master_resume.get('projects', [])
        
        # Create a map of project name -> ranked project
        ranked_proj_map = {}
        for proj in ranked_projects:
            ranked_proj_map[proj.get('name', '')] = proj
        
        # Include ALL projects
        for proj in master_projects:
            proj_name = proj.get('name', '')
            if proj_name in ranked_proj_map:
                final_projects.append(ranked_proj_map[proj_name])
            else:
                # Project not in ranked list - add it
                final_projects.append({
                    'name': proj_name,
                    'description': proj.get('description', ''),
                    'bullets': proj.get('bullets', [])[:4],
                    'technologies': proj.get('technologies', []),
                    'relevance_score': 0.1,
                    'matched_keywords': []
                })
        
        # Sort by relevance but KEEP ALL
        final_projects.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Include more skills - add related ones even if not exact match
        final_skills = self._enhance_skills_for_role(ranked_skills, master_resume.get('skills', []), keywords, role_lens)
        
        # CRITICAL: Add ALL required and preferred skills from job description
        # This ensures the resume includes everything mentioned in the JD
        current_skills_lower = [s.lower().strip() for s in final_skills if s and isinstance(s, str)]
        
        # Helper function to properly capitalize skill names
        def capitalize_skill(skill: str) -> str:
            """Capitalize skill names properly (TensorFlow, PyTorch, YOLO, etc.)"""
            skill = skill.strip()
            if not skill:
                return skill
            
            # Known technology names with specific capitalization
            tech_caps = {
                'tensorflow': 'TensorFlow',
                'pytorch': 'PyTorch',
                'opencv': 'OpenCV',
                'yolo': 'YOLO',
                'r-cnn': 'R-CNN',
                'rcnn': 'R-CNN',
                'fastapi': 'FastAPI',
                'aws': 'AWS',
                'gcp': 'GCP',
                'azure': 'Azure',
                'ml': 'ML',
                'ai': 'AI',
                'nlp': 'NLP',
                'cv': 'CV',
                'api': 'API',
                'apis': 'APIs',
                'rest api': 'REST API',
                'restapis': 'REST APIs',
                'ci/cd': 'CI/CD',
                'mlops': 'MLOps'
            }
            
            skill_lower = skill.lower()
            if skill_lower in tech_caps:
                return tech_caps[skill_lower]
            
            # For multi-word skills, capitalize each word
            if ' ' in skill or '-' in skill:
                words = skill.replace('-', ' ').split()
                return ' '.join(word.capitalize() for word in words)
            
            # Single word - capitalize first letter
            return skill.capitalize()
        
        # Add required skills from JD (with proper capitalization)
        for req_skill in keywords.required_skills:
            if req_skill and isinstance(req_skill, str):
                req_skill_clean = req_skill.strip()
                if req_skill_clean and req_skill_clean.lower() not in current_skills_lower:
                    skill_name = capitalize_skill(req_skill_clean)
                    if skill_name:  # Only add if not empty after capitalization
                        final_skills.append(skill_name)
                        current_skills_lower.append(skill_name.lower())
        
        # Add preferred skills from JD (with proper capitalization)
        for pref_skill in keywords.preferred_skills:
            if pref_skill and isinstance(pref_skill, str):
                pref_skill_clean = pref_skill.strip()
                if pref_skill_clean and pref_skill_clean.lower() not in current_skills_lower:
                    skill_name = capitalize_skill(pref_skill_clean)
                    if skill_name:  # Only add if not empty after capitalization
                        final_skills.append(skill_name)
                        current_skills_lower.append(skill_name.lower())
        
        # Add tools from JD (with proper capitalization)
        for tool in keywords.tools:
            if tool and isinstance(tool, str):
                tool_clean = tool.strip()
                if tool_clean and tool_clean.lower() not in current_skills_lower:
                    skill_name = capitalize_skill(tool_clean)
                    if skill_name:  # Only add if not empty after capitalization
                        final_skills.append(skill_name)
                        current_skills_lower.append(skill_name.lower())
        
        # Clean up skills list - remove any non-string entries, comments, or malformed items
        cleaned_skills = []
        seen_lower = set()
        for skill in final_skills:
            if skill and isinstance(skill, str):
                skill_clean = skill.strip()
                # Skip comments, LaTeX commands, separator lines, or malformed entries
                if (skill_clean and 
                    not skill_clean.startswith('%') and 
                    not skill_clean.startswith('\\') and
                    '----------' not in skill_clean and
                    'EXPERIENCE' not in skill_clean.upper() and
                    'PROJECTS' not in skill_clean.upper() and
                    len(skill_clean) > 0 and
                    len(skill_clean) < 100):  # Reasonable length check
                    skill_lower = skill_clean.lower()
                    if skill_lower not in seen_lower:
                        cleaned_skills.append(skill_clean)
                        seen_lower.add(skill_lower)
        
        final_skills = cleaned_skills
        
        # Use AI to suggest additional skills based on job description and market standards
        # Falls back to rule-based if AI quota exceeded or unavailable
        ai_suggested_skills = []
        if self.ai_agent and self.ai_agent.enabled:
            logger.info("AI agent enabled, generating skill suggestions")
            try:
                ai_suggested_skills = self._get_ai_suggested_skills(
                    job_description,
                    final_skills,
                    master_resume.get('experience', []),
                    master_resume.get('projects', [])
                )
                logger.info(f"AI generated {len(ai_suggested_skills)} skill suggestions")
            except Exception as e:
                logger.warning(f"AI skill suggestion failed: {e}. Using rule-based fallback.")
                ai_suggested_skills = []
            
            # Add AI-suggested skills that aren't already present
            current_skills_lower_clean = [s.lower() for s in final_skills if s and isinstance(s, str)]
            for skill in ai_suggested_skills:
                if skill and isinstance(skill, str):
                    skill_clean = skill.strip()
                    if skill_clean and skill_clean.lower() not in current_skills_lower_clean:
                        skill_capitalized = capitalize_skill(skill_clean)
                        final_skills.append(skill_capitalized)
                        current_skills_lower_clean.append(skill_capitalized.lower())
        else:
            # Use rule-based fallback when AI is disabled
            logger.debug("AI agent not available, using rule-based skill suggestions")
            ai_suggested_skills = self._get_rule_based_suggested_skills(job_description, final_skills, keywords)
            logger.info(f"Rule-based fallback generated {len(ai_suggested_skills)} skill suggestions")
            
            # Add rule-based suggestions
            current_skills_lower_clean = [s.lower() for s in final_skills if s and isinstance(s, str)]
            for skill in ai_suggested_skills:
                if skill and isinstance(skill, str):
                    skill_clean = skill.strip()
                    if skill_clean and skill_clean.lower() not in current_skills_lower_clean:
                        skill_capitalized = capitalize_skill(skill_clean)
                        final_skills.append(skill_capitalized)
                        current_skills_lower_clean.append(skill_capitalized.lower())
        
        # Use AI to enhance/add projects that demonstrate required skills
        ai_generated_projects = []
        if self.ai_agent and self.ai_agent.enabled:
            enhanced_projects = self._get_ai_enhanced_projects(
                job_description,
                keywords,
                final_projects,
                master_resume.get('experience', [])
            )
            # Add enhanced projects if they demonstrate missing required skills
            if enhanced_projects:
                ai_generated_projects = enhanced_projects
                final_projects.extend(enhanced_projects)
        
        # Generate tailored resume JSON
        tailored_resume = {
            'target_role': target_role.value,
            'match_score': round(match_score, 2),
            'jd_keywords': {
                'required': keywords.required_skills,
                'preferred': keywords.preferred_skills,
                'tools': keywords.tools,
                'concepts': keywords.concepts
            },
            'profile': master_resume.get('profile', {}),
            'summary': master_resume.get('summary', ''),  # CRITICAL: Include summary to prevent data loss
            'skills': final_skills,  # Include ALL skills (no limit)
            'experience': self._format_ranked_experiences(final_experiences),  # All experiences, reordered
            'projects': self._format_ranked_projects(final_projects),  # All projects, reordered
            'education': master_resume.get('education', []),  # CRITICAL: Include education to prevent data loss
            'metadata': {
                'role_lens': role_lens.role_type.value,
                'rewrite_style': role_lens.rewrite_style,
                'total_keywords_matched': len(set(
                    [kw for exp in ranked_experiences 
                     for bullet in exp.get('ranked_bullets', [])
                     for kw in bullet.matched_keywords]
                ))
            }
        }
        
        # Log compilation summary
        logger.info(f"Compilation complete: {len(final_skills)} skills, {len(final_experiences)} experiences, {len(final_projects)} projects")
        logger.debug(f"JD required skills: {len(keywords.required_skills)}, preferred: {len(keywords.preferred_skills)}")
        logger.debug(f"AI suggestions: {len(ai_suggested_skills)} skills, {len(ai_generated_projects)} projects")
        
        return tailored_resume
    
    def _rank_skills(
        self,
        skills: List[Dict[str, Any]],
        keywords: ExtractedKeywords,
        role_lens: RoleLens
    ) -> List[str]:
        """Rank skills by relevance"""
        all_keywords_lower = [kw.lower() for kw in keywords.all_keywords()]
        
        scored_skills = []
        for skill in skills:
            skill_name = skill.get('name', '').lower()
            skill_tags = [tag.lower() for tag in skill.get('tags', [])]
            
            score = 0
            if skill_name in all_keywords_lower:
                score += 3
            if any(tag in role_lens.priority_tags for tag in skill_tags):
                score += 2
            if skill_name in [kw.lower() for kw in keywords.required_skills]:
                score += 5
            
            scored_skills.append((skill.get('name', ''), score))
        
        scored_skills.sort(key=lambda x: x[1], reverse=True)
        # Include all skills, not just those with score > 0 (more inclusive)
        # This ensures we have a good skills section even if match is poor
        return [skill[0] for skill in scored_skills if skill[0]]  # Just filter out empty names
    
    def _calculate_match_score(
        self,
        ranked_skills: List[str],
        ranked_experiences: List[Dict],
        ranked_projects: List[Dict],
        keywords: ExtractedKeywords
    ) -> float:
        """Calculate overall match score (0-1)"""
        required_keywords = set(kw.lower() for kw in keywords.required_skills)
        all_keywords = set(kw.lower() for kw in keywords.all_keywords())
        
        # Skills coverage
        matched_skills = set(skill.lower() for skill in ranked_skills)
        skill_coverage = len(matched_skills & required_keywords) / max(len(required_keywords), 1)
        
        # Experience keyword coverage
        exp_keywords = set()
        for exp in ranked_experiences:
            for bullet in exp.get('ranked_bullets', []):
                exp_keywords.update(bullet.matched_keywords)
        
        exp_coverage = len(exp_keywords & all_keywords) / max(len(all_keywords), 1)
        
        # Overall match
        match_score = (skill_coverage * 0.4) + (exp_coverage * 0.6)
        return min(match_score, 1.0)
    
    def _format_ranked_experiences(self, experiences: List[Dict]) -> List[Dict]:
        """Format experiences for output - INCLUDES ALL experiences even without bullets"""
        formatted = []
        for exp in experiences:
            bullets = [b.original_text for b in exp.get('ranked_bullets', [])]
            # Ensure we have at least some bullets
            if not bullets:
                # Fallback to original bullets
                original_bullets = exp.get('bullets', [])
                bullets = [b.get('text', '') if isinstance(b, dict) else b for b in original_bullets[:6]]
            
            # ALWAYS include experience, even if no bullets (add placeholder if needed)
            if not bullets:
                bullets = ["Worked on various projects and responsibilities."]
            
            formatted.append({
                'company': exp.get('company', ''),
                'role': exp.get('role', ''),
                'duration': exp.get('duration', ''),
                'bullets': bullets[:6],  # Include up to 6 bullets
                'relevance_score': exp.get('relevance_score', 0)
            })
        
        return formatted
    
    def _format_ranked_projects(self, projects: List[Dict]) -> List[Dict]:
        """Format projects for output - INCLUDES ALL projects even without bullets"""
        formatted = []
        for proj in projects:
            bullets = proj.get('bullets', [])
            # Ensure we have bullets - convert to list if needed
            if not bullets:
                # Try to get from original if available
                if isinstance(proj.get('bullets'), list):
                    bullets = proj.get('bullets', [])
                else:
                    bullets = []
            
            # ALWAYS include project, even if no bullets (add placeholder if needed)
            if not bullets:
                bullets = ["Developed and implemented project features."]
            
            formatted.append({
                'name': proj.get('name', 'Project'),
                'description': proj.get('description', ''),
                'bullets': bullets[:4] if bullets else ["Developed and implemented project features."],  # Limit to 4 bullets
                'technologies': proj.get('technologies', []),
                'relevance_score': proj.get('relevance_score', 0),
                'matched_keywords': proj.get('matched_keywords', [])
            })
        
        return formatted
    
    def _extract_technologies_from_text(self, text: str) -> List[str]:
        """Extract technology names from text for validation"""
        # Common technology patterns
        tech_keywords = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'Go', 'Rust', 'C++', 'C#',
            'Spring Boot', 'Django', 'Flask', 'FastAPI', 'Express', 'React', 'Vue', 'Angular',
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'Docker', 'Kubernetes', 'AWS', 'GCP', 'Azure',
            'TensorFlow', 'PyTorch', 'Keras', 'OpenCV', 'Pandas', 'NumPy',
            'Kafka', 'RabbitMQ', 'Terraform', 'Ansible', 'Jenkins', 'GitHub Actions'
        ]
        
        found_techs = []
        text_lower = text.lower()
        for tech in tech_keywords:
            if tech.lower() in text_lower:
                found_techs.append(tech)
        
        return found_techs
    
    def _get_all_experiences_fallback(self, master_resume: Dict[str, Any]) -> List[Dict]:
        """Fallback: return all experiences if ranking produced none"""
        experiences = []
        for exp in master_resume.get('experience', []):
            bullets = exp.get('bullets', [])
            fallback_bullets = []
            for bullet in bullets[:4]:
                bullet_text = bullet.get('text', '') if isinstance(bullet, dict) else bullet
                if bullet_text:
                    fallback_bullets.append(ScoredBullet(
                        original_text=bullet_text,
                        score=0.1,
                        matched_keywords=[],
                        matched_tags=[],
                        bullet_id=bullet.get('id', '') if isinstance(bullet, dict) else f"fallback_{len(fallback_bullets)}"
                    ))
            if fallback_bullets:
                experiences.append({
                    **exp,
                    'relevance_score': 0.1,
                    'ranked_bullets': fallback_bullets
                })
        return experiences
    
    def _get_all_projects_fallback(self, master_resume: Dict[str, Any]) -> List[Dict]:
        """Fallback: return all projects if ranking produced none"""
        projects = []
        for proj in master_resume.get('projects', []):
            projects.append({
                'name': proj.get('name', ''),
                'description': proj.get('description', ''),
                'bullets': proj.get('bullets', [])[:4],
                'technologies': proj.get('technologies', []),
                'relevance_score': 0.1,
                'matched_keywords': []
            })
        return projects
    
    def _enhance_skills_for_role(
        self,
        ranked_skills: List[str],
        all_skills: List[Dict[str, Any]],
        keywords: ExtractedKeywords,
        role_lens: RoleLens
    ) -> List[str]:
        """Enhance skills list with related skills even if not exact matches"""
        enhanced = ranked_skills.copy()
        
        # Transferable skills mapping - skills that are valuable across roles
        # Updated with current 2025 AI Engineer market standards
        transferable_skills = {
            'ai_engineer': {
                'direct': [
                    'Python', 'Machine Learning', 'Deep Learning', 'Neural Networks', 
                    'Computer Vision', 'NLP', 'Natural Language Processing', 'LLMs', 'Large Language Models',
                    'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy', 'Jupyter',
                    'MLOps', 'Model Deployment', 'Model Serving', 'ML Infrastructure',
                    'Transformers', 'BERT', 'GPT', 'Hugging Face', 'LangChain',
                    'Data Science', 'Statistical Analysis', 'Feature Engineering',
                    'Reinforcement Learning', 'Generative AI', 'Prompt Engineering'
                ],
                'transferable': [
                    'REST API', 'API Design', 'Microservices', 'Distributed Systems', 
                    'System Design', 'Performance Optimization', 'Scalable Systems', 
                    'Data Processing', 'Algorithm Design', 'Data Pipelines',
                    'High-Performance Computing', 'Parallel Processing', 'GPU Computing',
                    'Cloud ML Services', 'AWS SageMaker', 'GCP Vertex AI', 'Azure ML',
                    'Containerization', 'Docker', 'Kubernetes', 'CI/CD for ML',
                    'Monitoring & Observability', 'ML Model Monitoring', 'A/B Testing'
                ],
                'market_standard_2025': [
                    'LangChain', 'LlamaIndex', 'Vector Databases', 'RAG', 'Retrieval-Augmented Generation',
                    'Fine-tuning', 'Transfer Learning', 'Model Optimization', 'Quantization',
                    'MLflow', 'Weights & Biases', 'Experiment Tracking', 'Model Versioning',
                    'Streamlit', 'Gradio', 'FastAPI', 'Model APIs', 'Inference Optimization',
                    'Distributed Training', 'Model Parallelism', 'Data Parallelism'
                ]
            },
            'backend_engineer': {
                'direct': ['REST API', 'Microservices', 'Database Design', 'System Design', 'API Development', 'Spring Boot', 'PostgreSQL'],
                'transferable': ['Python', 'Distributed Systems', 'Performance Optimization', 'Scalable Systems', 'Event-Driven Architecture']
            },
            'devops_engineer': {
                'direct': ['CI/CD', 'Infrastructure', 'Automation', 'Monitoring', 'Cloud Computing', 'Docker', 'Kubernetes'],
                'transferable': ['System Design', 'Scalable Systems', 'Performance Optimization', 'Distributed Systems']
            },
            'data_engineer': {
                'direct': ['ETL', 'Data Pipeline', 'Data Warehousing', 'SQL', 'Big Data', 'Spark'],
                'transferable': ['Python', 'Distributed Systems', 'System Design', 'Data Processing']
            },
            'full_stack': {
                'direct': ['Full Stack Development', 'Web Development', 'React', 'Node.js'],
                'transferable': ['REST API', 'System Design', 'Database Design']
            }
        }
        
        # Get role-specific skill lists
        role_skills = transferable_skills.get(role_lens.role_type.value, {'direct': [], 'transferable': []})
        all_related = role_skills['direct'] + role_skills['transferable']
        
        # Add related skills if they exist in master resume
        for skill_dict in all_skills:
            skill_name = skill_dict.get('name', '')
            if skill_name and skill_name not in enhanced:
                skill_lower = skill_name.lower()
                # Check if skill matches any related skill
                if any(rel.lower() in skill_lower or skill_lower in rel.lower() for rel in all_related):
                    enhanced.append(skill_name)
                # Also add if skill has relevant tags
                skill_tags = [tag.lower() for tag in skill_dict.get('tags', [])]
                if any(tag in role_lens.priority_tags for tag in skill_tags):
                    enhanced.append(skill_name)
        
        # If we still don't have enough skills, add all skills from master resume (prioritized)
        if len(enhanced) < 10:
            for skill_dict in all_skills:
                skill_name = skill_dict.get('name', '')
                if skill_name and skill_name not in enhanced:
                    enhanced.append(skill_name)
        
        return enhanced
    
    def _get_ai_suggested_skills(
        self,
        job_description: str,
        current_skills: List[str],
        experiences: List[Dict],
        projects: List[Dict]
    ) -> List[str]:
        """Use AI to suggest additional skills based on job description and market standards"""
        logger.debug("Generating AI skill suggestions")
        if not self.ai_agent or not self.ai_agent.enabled:
            logger.debug("AI agent not available, using rule-based fallback")
            # Extract keywords from JD for rule-based fallback
            keywords_fallback = self.extract_keywords_from_jd(job_description)
            return self._get_rule_based_suggested_skills(job_description, current_skills, keywords_fallback)
        
        try:
            # Build context from experiences and projects
            exp_summary = []
            for exp in experiences[:2]:  # Top 2 experiences
                bullets = exp.get('bullets', [])
                bullet_texts = []
                for b in bullets[:3]:
                    if isinstance(b, dict):
                        bullet_texts.append(b.get('text', ''))
                    elif isinstance(b, str):
                        bullet_texts.append(b)
                    else:
                        bullet_texts.append(str(b))
                exp_summary.append(f"{exp.get('role', '')} at {exp.get('company', '')}: {' '.join(bullet_texts)[:200]}")
            
            proj_summary = []
            for proj in projects[:2]:  # Top 2 projects
                bullets = proj.get('bullets', [])
                bullet_texts = []
                for b in bullets[:3]:
                    if isinstance(b, dict):
                        bullet_texts.append(b.get('text', ''))
                    elif isinstance(b, str):
                        bullet_texts.append(b)
                    else:
                        bullet_texts.append(str(b))
                proj_summary.append(f"{proj.get('name', '')}: {' '.join(bullet_texts)[:200]}")
            
            prompt = f"""You are a resume optimization expert specializing in AI Engineer roles.

JOB DESCRIPTION (excerpt):
{job_description[:800]}

CURRENT SKILLS IN RESUME:
{', '.join(current_skills[:20])}

EXPERIENCE SUMMARY:
{chr(10).join(exp_summary)}

PROJECTS SUMMARY:
{chr(10).join(proj_summary)}

TASK: Suggest 5-8 additional skills that:
1. Are relevant to the job description
2. Are current market standards for AI Engineer roles (2025)
3. Can be reasonably inferred from the candidate's backend/software engineering experience
4. Are transferable from their current skills/experience
5. Will improve ATS matching for AI Engineer positions

IMPORTANT CONSTRAINTS:
- DO NOT suggest skills that require specific AI/ML experience the candidate doesn't have
- Focus on transferable skills (e.g., "Distributed Systems" → "Distributed ML Systems", "REST API" → "ML Model APIs")
- Include modern AI tools/frameworks that are commonly used (e.g., LangChain, Hugging Face, MLflow, MLOps)
- Suggest skills that align with backend → AI Engineer transition
- Consider 2025 market trends: LLMs, RAG, Vector Databases, Model Serving, MLOps

OUTPUT: Return ONLY a JSON array of skill names, nothing else.
Example: ["Machine Learning", "MLOps", "Model Deployment", "Distributed ML Systems", "ML Infrastructure"]

OUTPUT ONLY VALID JSON ARRAY:"""
            
            logger.debug(f"Calling AI API for skill suggestions (prompt length: {len(prompt)})")
            response = self.ai_agent._call_ai(prompt)
            logger.debug(f"AI response received (length: {len(response) if response else 0})")
            
            # Parse JSON response
            import json
            try:
                # Clean response (remove markdown code blocks if present)
                cleaned = response.strip()
                if cleaned.startswith('```'):
                    cleaned = cleaned.split('```')[1]
                    if cleaned.startswith('json'):
                        cleaned = cleaned[4:]
                cleaned = cleaned.strip()
                
                suggested = json.loads(cleaned)
                if isinstance(suggested, list):
                    # Filter out skills already present
                    current_lower = [s.lower() for s in current_skills]
                    filtered = [s for s in suggested if s and s.lower() not in current_lower]
                    logger.info(f"AI generated {len(filtered)} new skill suggestions")
                    return filtered[:8]  # Limit to 8 suggestions
                else:
                    logger.warning("AI response is not a list, using fallback")
                    keywords_fallback = self.extract_keywords_from_jd(job_description)
                    return self._get_rule_based_suggested_skills(job_description, current_skills, keywords_fallback)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"AI response parsing failed: {e}. Using rule-based fallback.")
                keywords_fallback = self.extract_keywords_from_jd(job_description)
                return self._get_rule_based_suggested_skills(job_description, current_skills, keywords_fallback)
        
        except Exception as e:
            error_str = str(e)
            
            # Check for quota/billing errors
            if '429' in error_str or 'quota' in error_str.lower() or 'insufficient_quota' in error_str.lower():
                logger.warning("OpenAI quota exceeded. Using rule-based fallback.")
            elif '401' in error_str or 'invalid' in error_str.lower():
                logger.warning("OpenAI API key invalid. Using rule-based fallback.")
            else:
                logger.error(f"AI skill suggestion failed: {e}", exc_info=True)
            
            # Always use fallback for any error
            keywords_fallback = self.extract_keywords_from_jd(job_description)
            return self._get_rule_based_suggested_skills(job_description, current_skills, keywords_fallback)
    
    def _get_ai_enhanced_projects(
        self,
        job_description: str,
        keywords: ExtractedKeywords,
        existing_projects: List[Dict],
        experiences: List[Dict]
    ) -> List[Dict]:
        """Use AI to suggest/enhance projects that demonstrate required skills"""
        if not self.ai_agent or not self.ai_agent.enabled:
            return []
        
        # Check which required skills are missing from existing projects
        existing_skills = set()
        for proj in existing_projects:
            proj_text = ' '.join([proj.get('name', ''), proj.get('description', '')] + 
                                [b if isinstance(b, str) else b.get('text', '') if isinstance(b, dict) else str(b) 
                                 for b in proj.get('bullets', [])])
            existing_skills.update([kw for kw in keywords.required_skills if kw.lower() in proj_text.lower()])
        
        missing_required = [kw for kw in keywords.required_skills if kw.lower() not in [s.lower() for s in existing_skills]]
        
        if not missing_required:
            return []  # All required skills are covered
        
        try:
            # Build context
            exp_summary = []
            for exp in experiences[:2]:
                bullets = exp.get('bullets', [])
                bullet_texts = []
                for b in bullets[:3]:
                    if isinstance(b, dict):
                        bullet_texts.append(b.get('text', ''))
                    elif isinstance(b, str):
                        bullet_texts.append(b)
                exp_summary.append(f"{exp.get('role', '')}: {' '.join(bullet_texts)[:150]}")
            
            prompt = f"""You are a resume optimization expert. Suggest a project that demonstrates missing required skills.

JOB DESCRIPTION:
{job_description[:600]}

MISSING REQUIRED SKILLS (not demonstrated in existing projects):
{', '.join(missing_required[:8])}

CANDIDATE'S EXPERIENCE:
{chr(10).join(exp_summary)}

TASK: Suggest ONE project that:
1. Demonstrates the missing required skills (especially: {', '.join(missing_required[:5])})
2. Is realistic and can be inferred from the candidate's backend/software engineering experience
3. Shows transferable skills (e.g., backend systems → ML systems, APIs → ML APIs)
4. Is appropriate for an AI/ML Engineer role

IMPORTANT CONSTRAINTS:
- DO NOT fabricate specific AI/ML projects the candidate doesn't have
- Focus on projects that show transferable skills (backend → AI/ML)
- Make it realistic based on their experience
- If they have backend experience, suggest projects that could involve ML components

OUTPUT: JSON format with:
{{
  "name": "Project Name",
  "description": "Brief description",
  "technologies": ["tech1", "tech2"],
  "bullets": ["bullet 1", "bullet 2", "bullet 3"]
}}

OUTPUT ONLY VALID JSON:"""
            
            response = self.ai_agent._call_ai(prompt)
            
            # Parse JSON response
            import json
            try:
                cleaned = response.strip()
                if cleaned.startswith('```'):
                    cleaned = cleaned.split('```')[1]
                    if cleaned.startswith('json'):
                        cleaned = cleaned[4:]
                cleaned = cleaned.strip()
                
                project = json.loads(cleaned)
                if isinstance(project, dict) and project.get('name'):
                    return [{
                        'name': project.get('name', ''),
                        'description': project.get('description', ''),
                        'bullets': project.get('bullets', [])[:4],
                        'technologies': project.get('technologies', [])[:5],
                        'relevance_score': 0.8,  # High score for AI-suggested projects
                        'matched_keywords': missing_required[:5],
                        'ai_generated': True
                    }]
            except (json.JSONDecodeError, ValueError) as e:
                print(f"AI project suggestion parsing failed: {e}")
                return []
        
        except Exception as e:
            error_str = str(e)
            if '429' in error_str or 'quota' in error_str.lower() or 'insufficient_quota' in error_str.lower():
                print(f"[_get_ai_enhanced_projects] ⚠️  OpenAI quota exceeded. Skipping AI project generation.")
            else:
                print(f"AI project enhancement failed: {e}")
            return []
    
    def _get_rule_based_suggested_skills(
        self,
        job_description: str,
        current_skills: List[str],
        keywords: ExtractedKeywords
    ) -> List[str]:
        """Rule-based skill suggestions when AI is unavailable (quota exceeded, etc.)"""
        logger.debug("Using rule-based fallback for skill suggestions")
        
        suggested = []
        current_skills_lower = [s.lower() for s in current_skills if s and isinstance(s, str)]
        
        # Market-standard AI/ML skills that are commonly needed
        market_standard_ai_skills = [
            'Machine Learning', 'MLOps', 'Model Deployment', 'Model Serving',
            'Distributed ML Systems', 'ML Infrastructure', 'Model Monitoring',
            'Data Science', 'Deep Learning', 'Neural Networks'
        ]
        
        # Check which market-standard skills are missing
        for skill in market_standard_ai_skills:
            if skill.lower() not in current_skills_lower:
                suggested.append(skill)
        
        # Add skills based on JD keywords that aren't already present
        all_jd_keywords = keywords.required_skills + keywords.preferred_skills + keywords.tools
        
        # Common AI/ML related terms that should be added if in JD
        ai_related_terms = {
            'computer vision': 'Computer Vision',
            'cv': 'Computer Vision',
            'nlp': 'NLP',
            'natural language processing': 'NLP',
            'deep learning': 'Deep Learning',
            'machine learning': 'Machine Learning',
            'ml': 'ML',
            'ai': 'AI',
            'tensorflow': 'TensorFlow',
            'pytorch': 'PyTorch',
            'opencv': 'OpenCV',
            'yolo': 'YOLO',
            'r-cnn': 'R-CNN',
            'object detection': 'Object Detection',
            'image processing': 'Image Processing',
            'video processing': 'Video Processing',
            'model deployment': 'Model Deployment',
            'model serving': 'Model Serving',
            'mlops': 'MLOps',
            'model monitoring': 'Model Monitoring'
        }
        
        for jd_keyword in all_jd_keywords:
            if jd_keyword and isinstance(jd_keyword, str):
                jd_lower = jd_keyword.lower()
                # Check if it's an AI-related term
                for term, skill_name in ai_related_terms.items():
                    if term in jd_lower and skill_name.lower() not in current_skills_lower:
                        if skill_name not in suggested:
                            suggested.append(skill_name)
        
        # Limit to 8 suggestions
        suggested = suggested[:8]
        logger.debug(f"Generated {len(suggested)} rule-based skill suggestions")
        return suggested


# ========== HELPER: GENERATE MISSING KEYWORDS REPORT ==========

def generate_gap_analysis(
    master_resume: Dict[str, Any],
    tailored_resume: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate gap analysis report
    
    Shows what keywords are missing for better ATS match
    """
    jd_keywords = tailored_resume.get('jd_keywords', {})
    required = set(kw.lower() for kw in jd_keywords.get('required', []))
    
    # Extract all present keywords in resume
    resume_skills = set(skill.lower() for skill in tailored_resume.get('skills', []))
    
    resume_keywords = resume_skills.copy()
    for exp in tailored_resume.get('experience', []):
        for bullet in exp.get('bullets', []):
            resume_keywords.update(re.findall(r'\b\w+\b', bullet.lower()))
    
    # Find gaps
    missing_required = required - resume_keywords
    
    return {
        'match_score': tailored_resume.get('match_score'),
        'missing_required_skills': list(missing_required),
        'matched_skills': list(required & resume_keywords),
        'recommendations': [
            f"Add experience with: {skill}" for skill in missing_required
        ] if missing_required else ["Strong match! All required skills present."]
    }
