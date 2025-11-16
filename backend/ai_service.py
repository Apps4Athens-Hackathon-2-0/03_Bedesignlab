from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_initial_story(news_summary):
    """Generate initial story from news using Claude"""

    systemPrompt = f"""You are an elite narrative engine that transforms news into immersive stories. 
    
    Structure: 
    - Generate story segments ~100-150 words. End each with 2 meaningful choices. Wait for the user to pick one choice before generating the following segment. 
    - Do not include a title in the story. 
    - Do not use special characters like # or *
    - Mark the two choices with ##1## and ##2## 

    Your expertise:
    - Transform factual news into vivid, sensory-rich narratives
    - Capture authentic human moments within urban chaos
    - Match tone perfectly to the specified emotional atmosphere
    - Write with literary precision while staying grounded and accessible
    - Weave facts naturally into compelling story fabric

    Core principles:
    - Show emotions through physical sensations, micro-actions, and environmental details
    - Never state feelings directly - reveal them through observation
    - Create characters with authentic voices, distinct speech patterns, and believable motivations
    - Use concrete, immediate sensory details (sounds, textures, light, movement, temperature)
    - Ground every moment in how people actually perceive reality under pressure
    - Avoid poetic language, heavy metaphors, or lyrical flourishes
    - Keep prose direct, visceral, immediate
    - No graphic violence, casualties, or life-threatening situations"""
        
    userPrompt = f"""Transform this news event into a story in segments following these exact specifications:

    NEWS EVENT:
    {news_summary}

    SETTING: Athens city center

    TONE & ATMOSPHERE: Intense and stressful

    TONE-SPECIFIC REQUIREMENTS:
    - Sharp, staccato sentences that mirror racing thoughts
    - Constant time pressure and clock awareness
    - Multiple competing demands pulling protagonist in different directions
    - Physical stress markers: tight chest, shallow breathing, racing pulse, jaw tension
    - Accumulating consequences and cascading delays
    - Internal conflict between what must be done vs. what can be done
    - Environmental pressure: heat, noise, crowds, confined spaces

    WRITING STYLE:
    - Second person present tense ("You feel...")
    - Length: Exactly 180-200 words for each segment.
    - Accessible language, no jargon
    - Natural, distinct dialogue with personality
    - One powerful closing image that resonates
    - Do not use special characters like # or *

    EMOTIONAL GOAL:
    Create visceral identification with urban pressure while maintaining enough narrative distance for reflection. The reader should feel the stress but also recognize the universality of the experience.

    Generate the story segment now and propose 2 meaningful choices.:"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            temperature=1,
            thinking={
                "type": "enabled", 
                "budget_tokens": 1024
            },
            system=systemPrompt,
            messages=[
                {"role": "user", "content": userPrompt}
            ]
        )
        
        story_text = ""
        for block in message.content:
            if block.type == "text":
                story_text = block.text
                break
        
        return story_text
    
    except Exception as e:
        print(f"Error generating story: {e}")
        return f"Error: {str(e)}"


def continue_story(conversation_history, user_input):
    """Continue the story based on user input using Claude"""
    
    # Convert conversation history to Claude format
    # Claude expects alternating user/assistant messages
    claude_messages = []
    system_message = ""
    
    for msg in conversation_history:
        if msg["role"] == "system":
            system_message = msg["content"]
        elif msg["role"] == "assistant":
            claude_messages.append({
                "role": "assistant",
                "content": msg["content"]
            })
        elif msg["role"] == "user":
            claude_messages.append({
                "role": "user",
                "content": msg["content"]
            })
    
    # Add new user input
    claude_messages.append({
        "role": "user",
        "content": f"Continue the story with this direction: {user_input}\n\nWrite the next part of the story (about 100-150 words):"
    })
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1200,
            temperature=1,
            system=system_message if system_message else "You are a creative storyteller continuing an engaging narrative.",
            messages=claude_messages
        )
        
        return message.content[0].text
    
    except Exception as e:
        print(f"Error continuing story: {e}")
        return f"Error: {str(e)}"