"""
Simplified AutoGen Demo - Interview Platform Product Planning

This is a lightweight version for quick testing and understanding the workflow.
It demonstrates multi-agent collaboration by having each agent generate responses.
"""

from datetime import datetime
from config import Config, WorkflowConfig
import json
import time

# Try to import OpenAI client
try:
    from openai import OpenAI
    # RateLimitError may be in different locations depending on OpenAI version
    try:
        from openai import RateLimitError
    except ImportError:
        try:
            from openai.error import RateLimitError
        except ImportError:
            # Fallback: we'll catch it by checking error type
            RateLimitError = None
except ImportError:
    print("ERROR: OpenAI client is not installed!")
    print("Please run: pip install -r ../requirements.txt")
    exit(1)


class SimpleInterviewPlatformWorkflow:
    """Simplified workflow for interview platform planning"""

    def __init__(self):
        """Initialize the workflow"""
        if not Config.validate_setup():
            print("ERROR: Configuration validation failed!")
            exit(1)

        self.client = OpenAI(api_key=Config.API_KEY, base_url=Config.API_BASE)
        self.outputs = {}
        self.model = Config.OPENAI_MODEL

    def _make_api_call(self, system_prompt: str, user_message: str, max_retries: int = 3):
        """
        Make an API call with rate limit retry logic.
        
        Args:
            system_prompt: System message for the API call
            user_message: User message for the API call
            max_retries: Maximum number of retry attempts
            
        Returns:
            API response object
            
        Raises:
            RateLimitError: If rate limit is exceeded and cannot be retried
            Exception: For other API errors
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    temperature=Config.AGENT_TEMPERATURE,
                    max_tokens=Config.AGENT_MAX_TOKENS,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ]
                )
                return response
            except Exception as e:
                error_str = str(e)
                error_type = type(e).__name__
                
                # Check if it's a rate limit error (by name or message content)
                is_rate_limit = (
                    error_type == "RateLimitError" or 
                    "rate_limit" in error_str.lower() or 
                    "rate limit" in error_str.lower() or
                    "429" in error_str
                )
                
                if is_rate_limit:
                    # Try to extract wait time from error message
                    wait_time = 60  # Default wait time in seconds
                    
                    if "Please try again in" in error_str:
                        # Extract wait time from error message (e.g., "Please try again in 3m23.04s")
                        import re
                        time_match = re.search(r'Please try again in ([\d.]+)([smh])', error_str)
                        if time_match:
                            value = float(time_match.group(1))
                            unit = time_match.group(2)
                            if unit == 's':
                                wait_time = int(value) + 5  # Add 5 second buffer
                            elif unit == 'm':
                                wait_time = int(value * 60) + 10  # Add 10 second buffer
                            elif unit == 'h':
                                wait_time = int(value * 3600) + 60  # Add 1 minute buffer
                    
                    if attempt < max_retries - 1:
                        print(f"\n⚠️  Rate limit reached. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                        print(f"   Error: {error_str[:200]}...")
                        time.sleep(wait_time)
                    else:
                        print(f"\n❌ Rate limit error after {max_retries} attempts:")
                        print(f"   {error_str}")
                        print("\n💡 Solutions:")
                        print("   1. Wait for the rate limit to reset (check error message for wait time)")
                        print("   2. Upgrade your API tier for higher limits")
                        print("   3. Use a different API key if available")
                        if "Groq" in error_str or "groq" in error_str:
                            print("   4. Check Groq console: https://console.groq.com/settings/billing")
                        raise
                else:
                    # For other errors, raise immediately
                    raise

    def run(self):
        """Execute the complete workflow"""
        print("\n" + "="*80)
        print("AUTOGEN INTERVIEW PLATFORM WORKFLOW - SIMPLIFIED DEMO")
        print("="*80)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Model: {self.model}\n")

        # Phase 1: Research
        self.phase_research()

        # Phase 2: Analysis
        self.phase_analysis()

        # Phase 3: Blueprint
        self.phase_blueprint()

        # Phase 4: Technical Architecture
        self.phase_technical()

        # Phase 5: Review
        self.phase_review()

        # Summary
        self.print_summary()

    def phase_research(self):
        """Phase 1: Market Research"""
        print("\n" + "="*80)
        print("PHASE 1: MARKET RESEARCH")
        print("="*80)
        print("[ResearchAgent is analyzing the market...]")

        system_prompt = """You are a market research analyst. Provide a brief analysis of
3 competitors in AI interview platforms (HireVue, Pymetrics, Codility).
List their key features and identify market gaps in 150 words."""

        user_message = "Analyze the current market for AI-powered interview platforms."

        response = self._make_api_call(system_prompt, user_message)
        self.outputs["research"] = response.choices[0].message.content
        print("\n[ResearchAgent Output]")
        print(self.outputs["research"])

    def phase_analysis(self):
        """Phase 2: Opportunity Analysis"""
        print("\n" + "="*80)
        print("PHASE 2: OPPORTUNITY ANALYSIS")
        print("="*80)
        print("[AnalysisAgent is identifying opportunities...]")

        system_prompt = """You are a product analyst. Based on the market research provided,
identify 3 key market opportunities or gaps for a new AI interview platform.
Be concise in 150 words."""

        user_message = f"""Market research findings:
{self.outputs['research']}

Now identify market opportunities and gaps."""

        response = self._make_api_call(system_prompt, user_message)
        self.outputs["analysis"] = response.choices[0].message.content
        print("\n[AnalysisAgent Output]")
        print(self.outputs["analysis"])

    def phase_blueprint(self):
        """Phase 3: Product Blueprint"""
        print("\n" + "="*80)
        print("PHASE 3: PRODUCT BLUEPRINT")
        print("="*80)
        print("[BlueprintAgent is designing the product...]")

        system_prompt = """You are a product designer. Based on the market analysis and opportunities,
create a brief product blueprint including:
- Key features (3-5)
- User journey (2-3 steps)
Keep it concise - 150 words."""

        user_message = f"""Market Analysis:
{self.outputs['analysis']}

Create a product blueprint for our platform."""

        response = self._make_api_call(system_prompt, user_message)
        self.outputs["blueprint"] = response.choices[0].message.content
        print("\n[BlueprintAgent Output]")
        print(self.outputs["blueprint"])

    def phase_technical(self):
        """Phase 4: Technical Architecture"""
        print("\n" + "="*80)
        print("PHASE 4: TECHNICAL ARCHITECTURE")
        print("="*80)
        print("[TechnicalArchitectAgent is designing the architecture...]")

        system_prompt = """You are a technical architect. Based on the product blueprint provided,
design a technical architecture including:
- Technology stack (frontend, backend, database)
- Key technical components and services
- Scalability and performance considerations
Keep it concise - 150 words."""

        user_message = f"""Product Blueprint:
{self.outputs['blueprint']}

Design the technical architecture for this platform."""

        response = self._make_api_call(system_prompt, user_message)
        self.outputs["technical"] = response.choices[0].message.content
        print("\n[TechnicalArchitectAgent Output]")
        print(self.outputs["technical"])

    def phase_review(self):
        """Phase 5: Strategic Review"""
        print("\n" + "="*80)
        print("PHASE 5: STRATEGIC REVIEW")
        print("="*80)
        print("[ReviewerAgent is providing recommendations...]")

        system_prompt = """You are a product reviewer and strategist. Review the product blueprint
and technical architecture, then provide 3 strategic recommendations for success.
Be concise - 150 words."""

        user_message = f"""Product Blueprint:
{self.outputs['blueprint']}

Technical Architecture:
{self.outputs['technical']}

Provide strategic review and recommendations."""

        response = self._make_api_call(system_prompt, user_message)
        self.outputs["review"] = response.choices[0].message.content
        print("\n[ReviewerAgent Output]")
        print(self.outputs["review"])

    def print_summary(self):
        """Print final summary"""
        print("\n" + "="*80)
        print("FINAL SUMMARY")
        print("="*80)

        print("""
This workflow demonstrated a 5-agent collaboration:
1. ResearchAgent - Analyzed the market
2. AnalysisAgent - Identified opportunities
3. BlueprintAgent - Designed the product
4. TechnicalArchitectAgent - Designed technical architecture
5. ReviewerAgent - Provided strategic recommendations

Each agent received context from the previous agent's output,
demonstrating the sequential workflow pattern of AutoGen.
""")

        # Print full results
        print("\n" + "="*80)
        print("FULL RESULTS - ALL PHASES")
        print("="*80)
        
        print("\n" + "-"*80)
        print("PHASE 1: MARKET RESEARCH (Full Output)")
        print("-"*80)
        print(self.outputs["research"])
        
        print("\n" + "-"*80)
        print("PHASE 2: OPPORTUNITY ANALYSIS (Full Output)")
        print("-"*80)
        print(self.outputs["analysis"])
        
        print("\n" + "-"*80)
        print("PHASE 3: PRODUCT BLUEPRINT (Full Output)")
        print("-"*80)
        print(self.outputs["blueprint"])
        
        print("\n" + "-"*80)
        print("PHASE 4: TECHNICAL ARCHITECTURE (Full Output)")
        print("-"*80)
        print(self.outputs["technical"])
        
        print("\n" + "-"*80)
        print("PHASE 5: STRATEGIC REVIEW (Full Output)")
        print("-"*80)
        print(self.outputs["review"])

        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"workflow_outputs_{timestamp}.txt"
        with open(output_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("AUTOGEN INTERVIEW PLATFORM WORKFLOW - FULL RESULTS\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {self.model}\n\n")
            
            f.write("\n" + "-"*80 + "\n")
            f.write("PHASE 1: MARKET RESEARCH\n")
            f.write("-"*80 + "\n")
            f.write(self.outputs["research"] + "\n")
            
            f.write("\n" + "-"*80 + "\n")
            f.write("PHASE 2: OPPORTUNITY ANALYSIS\n")
            f.write("-"*80 + "\n")
            f.write(self.outputs["analysis"] + "\n")
            
            f.write("\n" + "-"*80 + "\n")
            f.write("PHASE 3: PRODUCT BLUEPRINT\n")
            f.write("-"*80 + "\n")
            f.write(self.outputs["blueprint"] + "\n")
            
            f.write("\n" + "-"*80 + "\n")
            f.write("PHASE 4: TECHNICAL ARCHITECTURE\n")
            f.write("-"*80 + "\n")
            f.write(self.outputs["technical"] + "\n")
            
            f.write("\n" + "-"*80 + "\n")
            f.write("PHASE 5: STRATEGIC REVIEW\n")
            f.write("-"*80 + "\n")
            f.write(self.outputs["review"] + "\n")
        
        print(f"\n💾 Full results saved to: {output_file}")

        print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)


if __name__ == "__main__":
    try:
        workflow = SimpleInterviewPlatformWorkflow()
        workflow.run()
        print("\n✅ Workflow completed successfully!")
    except Exception as e:
        error_str = str(e)
        error_type = type(e).__name__
        
        # Check if it's a rate limit error
        is_rate_limit = (
            error_type == "RateLimitError" or 
            "rate_limit" in error_str.lower() or 
            "rate limit" in error_str.lower() or
            "429" in error_str
        )
        
        if is_rate_limit:
            print(f"\n❌ Rate Limit Error: {error_str[:300]}")
            print("\n💡 Rate Limit Solutions:")
            print("   1. Wait for the rate limit to reset (check error message for wait time)")
            print("   2. Upgrade your API tier for higher limits")
            print("   3. Use a different API key if available")
            if "Groq" in error_str or "groq" in error_str:
                print("   4. Check Groq console: https://console.groq.com/settings/billing")
                print("   5. Groq free tier has daily token limits - wait until reset")
            print("\n📝 Note: The workflow will automatically retry on rate limits")
            print("   but you may need to wait for your daily limit to reset.")
        else:
            print(f"\n❌ Error during workflow execution: {error_str}")
            print("\nTroubleshooting:")
            print("1. Verify OPENAI_API_KEY is set in parent directory .env (../.env)")
            print("2. Check your API key has sufficient credits")
            print("3. Verify internet connection")
            print("4. Ensure config.py can access shared_config from parent directory")
            print("5. Check API status:")
            if "groq" in error_str.lower():
                print("   - Groq: https://status.groq.com")
            else:
                print("   - OpenAI: https://status.openai.com")
        
        import traceback
        traceback.print_exc()
