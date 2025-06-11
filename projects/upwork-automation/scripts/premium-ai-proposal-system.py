#!/usr/bin/env python3
"""
Premium Multi-Model AI Proposal System for Upwork
Combines GPT-4, Claude 3 Opus, and specialized models for best-in-class results
Author: Timothy Poulton - Automation Specialist
"""

import os
import json
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from openai import OpenAI
import anthropic
import cohere
from datetime import datetime

# Initialize AI clients
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
claude_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
cohere_client = cohere.Client(os.getenv('COHERE_API_KEY'))

@dataclass
class ProposalRequest:
    job_title: str
    job_description: str
    budget: str
    client_history: Optional[str] = None
    required_skills: Optional[List[str]] = None
    job_url: Optional[str] = None

class PremiumProposalGenerator:
    """
    Multi-model approach:
    1. GPT-4: Main proposal generation and reasoning
    2. Claude 3 Opus: Tone refinement and personalization
    3. Cohere: Semantic analysis and keyword optimization
    4. GPT-4 Vision: Screenshot analysis if provided
    """
    
    def __init__(self):
        self.proposal_history = []
        self.success_patterns = self.load_success_patterns()
        
    async def generate_premium_proposal(self, request: ProposalRequest) -> Dict:
        """Generate a proposal using multiple AI models for best results"""
        
        # Step 1: Deep job analysis with Cohere
        job_insights = await self.analyze_job_with_cohere(request)
        
        # Step 2: Generate base proposal with GPT-4
        base_proposal = await self.generate_with_gpt4(request, job_insights)
        
        # Step 3: Refine tone and personalization with Claude
        refined_proposal = await self.refine_with_claude(base_proposal, request, job_insights)
        
        # Step 4: Optimize for Upwork algorithm
        optimized_proposal = await self.optimize_for_platform(refined_proposal, job_insights)
        
        # Step 5: Generate multiple variations
        variations = await self.create_variations(optimized_proposal, request)
        
        # Step 6: Score and select best version
        best_proposal = await self.select_best_proposal(variations, request)
        
        return {
            "primary_proposal": best_proposal,
            "variations": variations,
            "insights": job_insights,
            "optimization_score": self.calculate_score(best_proposal, job_insights),
            "personalization_tips": self.get_personalization_tips(request, job_insights)
        }
    
    async def analyze_job_with_cohere(self, request: ProposalRequest) -> Dict:
        """Use Cohere for deep semantic analysis of the job posting"""
        
        analysis_prompt = f"""
        Analyze this Upwork job posting for hidden insights:
        
        Title: {request.job_title}
        Description: {request.job_description}
        Budget: {request.budget}
        
        Extract:
        1. Client's unstated needs and pain points
        2. Industry-specific terminology and jargon
        3. Urgency indicators
        4. Budget flexibility signals
        5. Red flags or concerns
        6. Ideal freelancer profile
        """
        
        response = cohere_client.generate(
            model='command-xlarge-nightly',
            prompt=analysis_prompt,
            max_tokens=500,
            temperature=0.3
        )
        
        # Parse insights
        insights = self.parse_cohere_insights(response.generations[0].text)
        
        # Add semantic similarity search from successful proposals
        similar_wins = await self.find_similar_successful_jobs(request.job_description)
        insights['similar_successful_proposals'] = similar_wins
        
        return insights
    
    async def generate_with_gpt4(self, request: ProposalRequest, insights: Dict) -> str:
        """Generate base proposal with GPT-4 using advanced prompting"""
        
        system_prompt = """You are Timothy Poulton, a 20-year automation specialist who has transformed 500+ businesses.
        
        Your expertise:
        - Deep knowledge of Zapier, Make.com, n8n, and custom APIs
        - Specific experience in nightlife, hospitality, and entertainment tech
        - Focus on ROI and measurable business outcomes
        - Personal, consultative approach that builds trust
        
        Writing principles:
        1. Start with empathy - show you understand their specific pain
        2. Use "I" statements to build personal connection
        3. Share relevant metrics from similar projects
        4. Be specific about your approach without overwhelming
        5. End with a soft but clear call to action
        
        NEVER:
        - Use generic phrases like "I'm the perfect fit"
        - List all your skills unless directly relevant
        - Sound desperate or overly sales-y
        - Write more than 150 words
        """
        
        user_prompt = f"""
        Create a winning Upwork proposal for this job:
        
        Job Details:
        {json.dumps(request.__dict__, indent=2)}
        
        Key Insights from Analysis:
        {json.dumps(insights, indent=2)}
        
        Similar Successful Proposals:
        {insights.get('similar_successful_proposals', 'None found')}
        
        Proposal Requirements:
        1. Hook that mirrors their exact pain point
        2. Credibility statement with relevant metric
        3. 3-step solution approach
        4. Specific result from similar project
        5. Soft call to action
        
        Write the proposal now:
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    async def refine_with_claude(self, base_proposal: str, request: ProposalRequest, insights: Dict) -> str:
        """Use Claude 3 Opus to refine tone and add sophisticated personalization"""
        
        refinement_prompt = f"""
        You are an expert at crafting personalized, high-converting Upwork proposals.
        
        Original proposal:
        {base_proposal}
        
        Job context:
        - Title: {request.job_title}
        - Key pain points: {insights.get('pain_points', [])}
        - Client communication style: {insights.get('communication_style', 'professional')}
        - Industry: {insights.get('industry', 'general')}
        
        Refine this proposal to:
        1. Match the client's exact communication style
        2. Use their specific terminology and phrases
        3. Add subtle psychological triggers (urgency, social proof, authority)
        4. Ensure it sounds natural and conversational
        5. Optimize opening line for maximum impact
        
        Keep the core message but make it irresistible.
        """
        
        response = claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            temperature=0.5,
            messages=[
                {"role": "user", "content": refinement_prompt}
            ]
        )
        
        return response.content[0].text
    
    async def optimize_for_platform(self, proposal: str, insights: Dict) -> str:
        """Optimize for Upwork's algorithm and best practices"""
        
        optimization_prompt = f"""
        Optimize this Upwork proposal for maximum visibility and response rate:
        
        Current proposal:
        {proposal}
        
        Optimization goals:
        1. Include relevant keywords naturally: {insights.get('keywords', [])}
        2. Ensure mobile-friendly formatting (short paragraphs)
        3. Add subtle urgency without being pushy
        4. Include a specific question to encourage response
        5. Optimize length for Upwork's algorithm (100-150 words ideal)
        
        Return the optimized version:
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an Upwork optimization expert."},
                {"role": "user", "content": optimization_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    async def create_variations(self, proposal: str, request: ProposalRequest) -> List[Dict]:
        """Generate multiple variations for A/B testing"""
        
        variations = []
        
        # Variation 1: More casual/friendly
        casual_prompt = f"Make this proposal more casual and friendly while keeping it professional:\n\n{proposal}"
        
        # Variation 2: More data-driven
        data_prompt = f"Add more specific metrics and data points to this proposal:\n\n{proposal}"
        
        # Variation 3: Story-based
        story_prompt = f"Rewrite this proposal to start with a brief success story:\n\n{proposal}"
        
        # Generate all variations in parallel
        tasks = [
            self.generate_variation("casual", casual_prompt),
            self.generate_variation("data_driven", data_prompt),
            self.generate_variation("story_based", story_prompt)
        ]
        
        variations = await asyncio.gather(*tasks)
        variations.append({"type": "original", "content": proposal, "score": 0})
        
        return variations
    
    async def generate_variation(self, variation_type: str, prompt: str) -> Dict:
        """Generate a single proposal variation"""
        
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert proposal writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=500
        )
        
        return {
            "type": variation_type,
            "content": response.choices[0].message.content,
            "score": 0
        }
    
    async def select_best_proposal(self, variations: List[Dict], request: ProposalRequest) -> str:
        """Use AI to score and select the best proposal variation"""
        
        # Score each variation
        for variation in variations:
            variation['score'] = await self.score_proposal(variation['content'], request)
        
        # Sort by score and return best
        best = max(variations, key=lambda x: x['score'])
        return best['content']
    
    async def score_proposal(self, proposal: str, request: ProposalRequest) -> float:
        """Score a proposal based on multiple criteria"""
        
        scoring_prompt = f"""
        Score this Upwork proposal from 0-100 based on these criteria:
        
        Proposal:
        {proposal}
        
        Job Title: {request.job_title}
        
        Scoring Criteria (weight):
        1. Personalization and relevance (30%)
        2. Clear value proposition (25%)
        3. Credibility and social proof (20%)
        4. Call to action effectiveness (15%)
        5. Overall persuasiveness (10%)
        
        Return only the numerical score.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert at evaluating Upwork proposals."},
                {"role": "user", "content": scoring_prompt}
            ],
            temperature=0,
            max_tokens=10
        )
        
        try:
            score = float(response.choices[0].message.content.strip())
            return score
        except:
            return 75.0  # Default score if parsing fails
    
    def calculate_score(self, proposal: str, insights: Dict) -> Dict:
        """Calculate detailed scoring metrics"""
        
        return {
            "overall_score": 0,
            "personalization_score": 0,
            "keyword_density": 0,
            "readability_score": 0,
            "psychological_triggers": 0,
            "mobile_optimization": 0
        }
    
    def get_personalization_tips(self, request: ProposalRequest, insights: Dict) -> List[str]:
        """Generate specific tips for further personalization"""
        
        tips = []
        
        if insights.get('urgency_level', 0) > 7:
            tips.append("Mention your immediate availability in the first line")
        
        if insights.get('technical_level', 'medium') == 'beginner':
            tips.append("Offer a free 15-minute consultation to explain the process")
        
        if 'previous_bad_experience' in insights:
            tips.append("Address their past frustrations subtly: 'I understand you've had challenges with...'")
        
        return tips
    
    def load_success_patterns(self) -> Dict:
        """Load patterns from successful proposals"""
        
        # This would load from a database of successful proposals
        return {
            "opening_hooks": [
                "I noticed you're struggling with {pain_point}...",
                "Your {specific_challenge} caught my attention because...",
                "{Industry} automation is my specialty, and your {need} is exactly..."
            ],
            "credibility_statements": [
                "Last month, I helped {similar_business} achieve {metric}",
                "I've automated {number}+ {industry} businesses, including...",
                "My {tool} workflows have saved clients {metric} on average"
            ]
        }
    
    async def find_similar_successful_jobs(self, job_description: str) -> List[Dict]:
        """Find similar successful proposals using semantic search"""
        
        # This would use vector embeddings to find similar successful proposals
        # For now, returning mock data
        return [
            {
                "similarity_score": 0.92,
                "job_title": "Zapier Expert for Restaurant Chain",
                "winning_approach": "Focused on ROI and time savings",
                "result": "Won at $5,000, delivered in 2 weeks"
            }
        ]
    
    def parse_cohere_insights(self, analysis_text: str) -> Dict:
        """Parse Cohere's analysis into structured insights"""
        
        # This would use NLP to extract structured data
        # For now, returning mock structured data
        return {
            "pain_points": ["manual processes", "scaling issues", "integration needs"],
            "urgency_level": 8,
            "budget_flexibility": "high",
            "communication_style": "casual but professional",
            "industry": "restaurant/hospitality",
            "keywords": ["zapier", "automation", "integration", "workflow"],
            "red_flags": [],
            "ideal_freelancer": "experienced, industry knowledge, consultative approach"
        }


# Advanced Features for Premium System

class ProposalLearningSystem:
    """
    Machine learning system that improves proposals based on outcomes
    """
    
    def __init__(self):
        self.proposal_database = []
        self.success_metrics = {}
    
    async def track_proposal_outcome(self, proposal_id: str, outcome: str, client_response: Optional[str] = None):
        """Track whether proposals succeeded or failed"""
        
        # Store outcome data
        outcome_data = {
            "proposal_id": proposal_id,
            "outcome": outcome,  # "won", "lost", "no_response"
            "client_response": client_response,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update learning model
        await self.update_success_patterns(outcome_data)
    
    async def update_success_patterns(self, outcome_data: Dict):
        """Update our understanding of what works"""
        
        # This would use ML to identify patterns in successful proposals
        pass


class ProposalPersonalizationEngine:
    """
    Advanced personalization based on client analysis
    """
    
    async def analyze_client_profile(self, client_info: Dict) -> Dict:
        """Deep analysis of client from their Upwork profile"""
        
        profile_insights = {
            "spending_history": self.analyze_spending_patterns(client_info),
            "communication_preferences": self.detect_communication_style(client_info),
            "project_success_factors": self.identify_success_patterns(client_info),
            "red_flags": self.detect_potential_issues(client_info)
        }
        
        return profile_insights
    
    def analyze_spending_patterns(self, client_info: Dict) -> Dict:
        """Analyze how this client typically spends"""
        
        return {
            "average_project_value": 0,
            "payment_speed": "fast",
            "bonus_likelihood": "high",
            "long_term_potential": True
        }
    
    def detect_communication_style(self, client_info: Dict) -> str:
        """Detect client's preferred communication style"""
        
        # Analyze their job postings, feedback, etc.
        return "professional_but_friendly"
    
    def identify_success_patterns(self, client_info: Dict) -> List[str]:
        """What makes projects successful with this client"""
        
        return [
            "Clear communication",
            "Regular updates",
            "Exceeding deadlines"
        ]
    
    def detect_potential_issues(self, client_info: Dict) -> List[str]:
        """Identify potential red flags"""
        
        return []


# Main execution
async def main():
    """Example usage of the premium proposal system"""
    
    generator = PremiumProposalGenerator()
    
    # Example job
    request = ProposalRequest(
        job_title="Zapier Expert Needed for Restaurant Automation",
        job_description="We need help automating our order management...",
        budget="$1,000 - $5,000",
        required_skills=["Zapier", "API Integration", "Restaurant Systems"]
    )
    
    # Generate premium proposal
    result = await generator.generate_premium_proposal(request)
    
    print("🎯 Premium Proposal Generated!")
    print(f"Primary Proposal:\n{result['primary_proposal']}\n")
    print(f"Optimization Score: {result['optimization_score']}")
    print(f"Personalization Tips: {result['personalization_tips']}")
    
    # Show variations
    print("\n📊 A/B Test Variations:")
    for variation in result['variations']:
        print(f"\n{variation['type'].upper()} (Score: {variation['score']}):")
        print(variation['content'][:100] + "...")


if __name__ == "__main__":
    asyncio.run(main()) 