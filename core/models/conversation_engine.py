"""
Conversation Engine for Digital Twins
Handles natural language conversation, response generation, and conversational AI
"""

import asyncio
import logging
import random
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

# AI/ML imports
try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    logging.warning("AI/ML libraries not available. Using rule-based fallbacks.")

from ..config import settings

logger = logging.getLogger(__name__)

@dataclass
class ConversationMessage:
    """Individual conversation message"""
    message_id: str
    sender: str
    content: str
    message_type: str  # "text", "question", "command", "greeting"
    timestamp: datetime
    context: Dict[str, Any]
    sentiment: str
    intent: str

@dataclass
class ConversationContext:
    """Conversation context and state"""
    conversation_id: str
    participants: List[str]
    topic: str
    mood: str
    energy_level: float
    conversation_style: str
    start_time: datetime
    last_activity: datetime
    message_count: int

@dataclass
class ResponseTemplate:
    """Response template for different conversation scenarios"""
    template_id: str
    scenario: str
    personality_traits: Dict[str, float]
    response_patterns: List[str]
    context_requirements: Dict[str, Any]
    confidence: float

class ConversationEngine:
    """Manages natural language conversations for digital twins"""
    
    def __init__(self):
        """Initialize the conversation engine"""
        self.conversation_history: List[ConversationMessage] = []
        self.active_conversations: Dict[str, ConversationContext] = {}
        self.response_templates: List[ResponseTemplate] = []
        self.conversation_patterns: Dict[str, List[str]] = {}
        
        # AI/ML components
        self.sentiment_analyzer = None
        self.intent_classifier = None
        self.embedding_model = None
        self.ai_available = AI_AVAILABLE
        
        self.message_types = [
            "text", "question", "command", "emotion", "health_update", "personality_change"
        ]
        
        # Initialize AI models if available
        if self.ai_available:
            try:
                self._initialize_ai_models()
            except Exception as e:
                logger.warning(f"AI model initialization failed: {e}. Using rule-based fallbacks.")
                self.ai_available = False
        
        self.message_types = [
            "text", "question", "command", "greeting", "farewell",
            "compliment", "complaint", "request", "statement", "reaction"
        ]
        
        self.sentiment_types = [
            "positive", "negative", "neutral", "excited", "calm",
            "anxious", "happy", "sad", "angry", "surprised"
        ]
        
        self.intent_types = [
            "greet", "ask_question", "provide_information", "request_action",
            "express_emotion", "socialize", "seek_help", "give_compliment",
            "make_plan", "end_conversation"
        ]
        
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the conversation engine"""
        try:
            # Load conversation configurations
            await self._load_conversation_configs()
            
            # Initialize response templates
            await self._initialize_response_templates()
            
            # Initialize conversation patterns
            await self._initialize_conversation_patterns()
            
            self.is_initialized = True
            logger.info("Conversation Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Conversation Engine: {e}")
            raise
    
    async def _load_conversation_configs(self):
        """Load conversation engine configurations"""
        # This could load from files, databases, or external APIs
        pass
    
    async def _initialize_response_templates(self):
        """Initialize response templates for different scenarios"""
        templates = [
            ResponseTemplate(
                template_id="greeting_morning",
                scenario="morning_greeting",
                personality_traits={"extraversion": 0.7, "agreeableness": 0.8},
                response_patterns=[
                    "Good morning! How are you feeling today?",
                    "Morning! Ready to start the day?",
                    "Good morning! I hope you slept well."
                ],
                context_requirements={"time_of_day": "morning"},
                confidence=0.9
            ),
            ResponseTemplate(
                template_id="work_discussion",
                scenario="work_conversation",
                personality_traits={"conscientiousness": 0.8, "confidence": 0.7},
                response_patterns=[
                    "That sounds like an interesting project. What's your approach?",
                    "I'd be happy to help brainstorm some solutions.",
                    "Let's break this down into manageable steps."
                ],
                context_requirements={"topic": "work", "energy_level": 0.6},
                confidence=0.8
            ),
            ResponseTemplate(
                template_id="emotional_support",
                scenario="emotional_support",
                personality_traits={"empathy": 0.8, "agreeableness": 0.9},
                response_patterns=[
                    "I understand how you're feeling. That must be difficult.",
                    "It's okay to feel that way. Would you like to talk about it?",
                    "I'm here to listen. What's on your mind?"
                ],
                context_requirements={"sentiment": "negative", "energy_level": 0.4},
                confidence=0.8
            ),
            ResponseTemplate(
                template_id="social_engagement",
                scenario="social_interaction",
                personality_traits={"extraversion": 0.8, "openness": 0.7},
                response_patterns=[
                    "That's fascinating! Tell me more about it.",
                    "I love hearing about new experiences. What happened next?",
                    "That sounds like fun! I'd love to join in sometime."
                ],
                context_requirements={"topic": "personal", "sentiment": "positive"},
                confidence=0.7
            )
        ]
        
        self.response_templates.extend(templates)
    
    async def _initialize_conversation_patterns(self):
        """Initialize conversation patterns and flows"""
        self.conversation_patterns = {
            "greeting_flow": [
                "greeting", "response", "question", "answer", "follow_up"
            ],
            "work_discussion": [
                "topic_introduction", "question", "explanation", "clarification", "solution"
            ],
            "emotional_support": [
                "acknowledgment", "validation", "support", "encouragement", "next_steps"
            ],
            "casual_chat": [
                "topic_switch", "sharing", "reaction", "related_story", "connection"
            ]
        }
    
    def _initialize_ai_models(self):
        """Initialize AI/ML models for enhanced analysis"""
        try:
            logger.info("Attempting to initialize AI models...")
            
            # Check if we have enough memory/resources
            if not self._check_system_resources():
                logger.warning("Insufficient system resources for AI models. Using rule-based fallbacks.")
                self.ai_available = False
                return
            
            # Sentiment analysis pipeline - use smaller model
            try:
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    device=-1  # Force CPU to avoid GPU memory issues
                )
                logger.info("Sentiment analyzer initialized")
            except Exception as e:
                logger.warning(f"Sentiment analyzer failed: {e}. Using rule-based fallback.")
                self.sentiment_analyzer = None
            
            # Intent classification pipeline - use smaller model
            try:
                self.intent_classifier = pipeline(
                    "text-classification",
                    model="facebook/bart-large-mnli",
                    device=-1  # Force CPU to avoid GPU memory issues
                )
                logger.info("Intent classifier initialized")
            except Exception as e:
                logger.warning(f"Intent classifier failed: {e}. Using rule-based fallback.")
                self.intent_classifier = None
            
            # Text embedding model - use smaller model
            try:
                self.embedding_model = pipeline(
                    "feature-extraction",
                    model="sentence-transformers/all-MiniLM-L6-v2",
                    device=-1  # Force CPU to avoid GPU memory issues
                )
                logger.info("Embedding model initialized")
            except Exception as e:
                logger.warning(f"Embedding model failed: {e}. Using rule-based fallback.")
                self.embedding_model = None
            
            # Check if any models loaded successfully
            if not any([self.sentiment_analyzer, self.intent_classifier, self.embedding_model]):
                logger.warning("No AI models loaded successfully. Using rule-based fallbacks.")
                self.ai_available = False
            else:
                logger.info("AI models initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize AI models: {e}")
            self.ai_available = False
            # Ensure all models are None
            self.sentiment_analyzer = None
            self.intent_classifier = None
            self.embedding_model = None
    
    def _check_system_resources(self):
        """Check if system has enough resources for AI models"""
        try:
            import psutil
            import os
            
            # Check available memory (need at least 2GB)
            memory = psutil.virtual_memory()
            if memory.available < 2 * 1024 * 1024 * 1024:  # 2GB
                logger.warning(f"Insufficient memory: {memory.available / (1024**3):.1f}GB available")
                return False
            
            # Check if we're on macOS (known compatibility issues)
            if os.uname().sysname == "Darwin":
                logger.info("macOS detected - using conservative AI model loading")
                return True  # Allow but with warnings
            
            return True
            
        except ImportError:
            # psutil not available, assume OK
            return True
        except Exception as e:
            logger.warning(f"Resource check failed: {e}")
            return True  # Assume OK if check fails

    async def process_message(self, message: str, sender: str, conversation_id: str, context: Dict[str, Any]) -> ConversationMessage:
        """Process an incoming message with AI-enhanced analysis"""
        try:
            # Enhanced AI analysis if available
            if self.ai_available:
                sentiment = await self._analyze_sentiment_with_ai(message, context)
                intent = await self._detect_intent_with_ai(message, context)
                emotion = await self._detect_emotion_with_ai(message)
            else:
                sentiment = self._analyze_sentiment_rule_based(message, context)
                intent = self._detect_intent_rule_based(message, context)
                emotion = "neutral"
            
            # Create conversation message
            conversation_message = ConversationMessage(
                message_id=f"msg_{len(self.conversation_history) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                sender=sender,
                content=message,
                message_type=self._classify_message_type(message),
                timestamp=datetime.now(),
                context=context,
                sentiment=sentiment,
                intent=intent
            )
            
            # Add to history
            self.conversation_history.append(conversation_message)
            
            # Update conversation context
            await self._update_conversation_context(conversation_id, conversation_message)
            
            logger.info(f"Processed message from {sender}: {sentiment} - {intent} - {emotion}")
            return conversation_message
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            # Fallback to basic processing
            return await self._fallback_message_processing(message, sender, conversation_id, context)

    async def _analyze_sentiment_with_ai(self, message: str, context: Dict[str, Any]) -> str:
        """Analyze sentiment using HuggingFace models"""
        try:
            if not self.sentiment_analyzer:
                return self._analyze_sentiment_rule_based(message, context)
            
            result = self.sentiment_analyzer(message)
            sentiment = result[0]['label'].lower()
            confidence = result[0]['score']
            
            # Map to our sentiment types with confidence threshold
            if confidence < 0.6:
                return self._analyze_sentiment_rule_based(message, context)
            
            sentiment_mapping = {
                'positive': 'positive',
                'negative': 'negative',
                'neutral': 'neutral'
            }
            
            return sentiment_mapping.get(sentiment, 'neutral')
            
        except Exception as e:
            logger.error(f"AI sentiment analysis failed: {e}")
            return self._analyze_sentiment_rule_based(message, context)

    async def _detect_intent_with_ai(self, message: str, context: Dict[str, Any]) -> str:
        """Detect intent using HuggingFace models"""
        try:
            if not self.intent_classifier:
                return self._detect_intent_rule_based(message, context)
            
            # Define intent candidates
            intent_candidates = [
                "greet", "ask_question", "provide_information", "request_action",
                "express_emotion", "socialize", "seek_help", "give_compliment",
                "make_plan", "end_conversation", "health_inquiry", "personality_discussion"
            ]
            
            # Classify intent
            result = self.intent_classifier(message, candidate_labels=intent_candidates)
            intent = result['labels'][0]
            confidence = result['scores'][0]
            
            # Use AI result if confident, otherwise fallback
            if confidence > 0.5:
                return intent
            else:
                return self._detect_intent_rule_based(message, context)
                
        except Exception as e:
            logger.error(f"AI intent detection failed: {e}")
            return self._detect_intent_rule_based(message, context)

    async def _detect_emotion_with_ai(self, message: str) -> str:
        """Detect emotional state using AI"""
        try:
            if not self.intent_classifier:
                return "neutral"
            
            # Use a more sophisticated emotion detection model
            emotion_candidates = [
                "joy", "sadness", "anger", "fear", "surprise", "disgust", "trust", "anticipation"
            ]
            
            result = self.intent_classifier(message, candidate_labels=emotion_candidates)
            emotion = result['labels'][0]
            confidence = result['scores'][0]
            
            if confidence > 0.4:
                return emotion
            else:
                return "neutral"
                
        except Exception as e:
            logger.error(f"AI emotion detection failed: {e}")
            return "neutral"
    
    def _classify_message_type(self, message: str) -> str:
        """Classify the type of message"""
        message_lower = message.lower().strip()
        
        # Greeting patterns
        if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
            return "greeting"
        
        # Question patterns
        if any(word in message_lower for word in ["what", "how", "why", "when", "where", "who", "?"]):
            return "question"
        
        # Command patterns
        if any(word in message_lower for word in ["please", "can you", "could you", "help me", "show me"]):
            return "command"
        
        # Farewell patterns
        if any(word in message_lower for word in ["goodbye", "bye", "see you", "take care", "farewell"]):
            return "farewell"
        
        # Compliment patterns
        if any(word in message_lower for word in ["great", "awesome", "amazing", "wonderful", "excellent", "good job"]):
            return "compliment"
        
        # Default to text
        return "text"
    
    def _analyze_sentiment(self, message: str, context: Dict[str, Any]) -> str:
        """Analyze the sentiment of a message"""
        message_lower = message.lower()
        
        # Positive sentiment indicators
        positive_words = ["happy", "excited", "great", "awesome", "wonderful", "love", "enjoy", "good", "nice"]
        if any(word in message_lower for word in positive_words):
            return "positive"
        
        # Negative sentiment indicators
        negative_words = ["sad", "angry", "frustrated", "worried", "anxious", "bad", "terrible", "hate", "disappointed"]
        if any(word in message_lower for word in negative_words):
            return "negative"
        
        # Excited sentiment indicators
        excited_words = ["wow", "amazing", "incredible", "fantastic", "brilliant", "outstanding"]
        if any(word in message_lower for word in excited_words):
            return "excited"
        
        # Anxious sentiment indicators
        anxious_words = ["nervous", "scared", "afraid", "worried", "concerned", "stressed"]
        if any(word in message_lower for word in anxious_words):
            return "anxious"
        
        # Context-based sentiment
        if context.get("mood") == "stressed" and "work" in message_lower:
            return "anxious"
        
        # Default to neutral
        return "neutral"
    
    def _detect_intent(self, message: str, context: Dict[str, Any]) -> str:
        """Detect the intent behind a message"""
        message_lower = message.lower()
        
        # Greeting intent
        if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "greet"
        
        # Question intent
        if "?" in message or any(word in message_lower for word in ["what", "how", "why", "when", "where", "who"]):
            return "ask_question"
        
        # Request intent
        if any(word in message_lower for word in ["can you", "could you", "please", "help me", "show me"]):
            return "request_action"
        
        # Information intent
        if any(word in message_lower for word in ["I think", "I believe", "in my opinion", "I know"]):
            return "provide_information"
        
        # Emotional expression
        if any(word in message_lower for word in ["I feel", "I'm feeling", "I am", "I'm so"]):
            return "express_emotion"
        
        # Social intent
        if any(word in message_lower for word in ["let's", "we should", "together", "join"]):
            return "socialize"
        
        # Help seeking
        if any(word in message_lower for word in ["help", "support", "advice", "guidance"]):
            return "seek_help"
        
        # Default intent
        return "socialize"
    
    async def _update_conversation_context(self, conversation_id: str, message: ConversationMessage):
        """Update the conversation context with new message"""
        if conversation_id not in self.active_conversations:
            # Create new conversation context
            context = ConversationContext(
                conversation_id=conversation_id,
                participants=[message.sender],
                topic=self._extract_topic(message.content),
                mood=message.sentiment,
                energy_level=0.7,
                conversation_style="casual",
                start_time=message.timestamp,
                last_activity=message.timestamp,
                message_count=1
            )
            self.active_conversations[conversation_id] = context
        else:
            # Update existing context
            context = self.active_conversations[conversation_id]
            context.last_activity = message.timestamp
            context.message_count += 1
            
            # Update mood if significant change
            if message.sentiment != "neutral":
                context.mood = message.sentiment
    
    def _extract_topic(self, message: str) -> str:
        """Extract the main topic from a message"""
        message_lower = message.lower()
        
        # Work-related topics
        if any(word in message_lower for word in ["work", "project", "meeting", "deadline", "task"]):
            return "work"
        
        # Health-related topics
        if any(word in message_lower for word in ["health", "exercise", "diet", "sleep", "stress"]):
            return "health"
        
        # Social topics
        if any(word in message_lower for word in ["friend", "family", "party", "event", "social"]):
            return "social"
        
        # Personal topics
        if any(word in message_lower for word in ["hobby", "interest", "passion", "goal", "dream"]):
            return "personal"
        
        # Default topic
        return "general"
    
    def generate_response(self, personality_traits: Dict[str, Any], conversation_context: ConversationContext = None, last_message: ConversationMessage = None, message: str = None, sender: str = "user", conversation_id: str = "default", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a contextual response based on personality and conversation context"""
        try:
            # Handle both old and new API calls
            if message is not None:
                # New API call - handle async properly
                try:
                    # Check if we're already in an event loop
                    loop = asyncio.get_running_loop()
                    # We're in an async context, so call the sync version
                    return self._generate_response_sync(message, sender, conversation_id, context or {}, personality_traits)
                except RuntimeError:
                    # No event loop running, safe to use asyncio.run()
                    return asyncio.run(self._generate_response_async(message, sender, conversation_id, context or {}, personality_traits))
            else:
                # Old API call - use existing parameters
                if conversation_context is None or last_message is None:
                    return {"response": "I'm here to help. What would you like to talk about?", "confidence": 0.5}
                
                # Find appropriate response template
                template = self._find_response_template(conversation_context, last_message, personality_traits)
                
                if template:
                    # Select response pattern
                    response = random.choice(template.response_patterns)
                    
                    # Personalize response based on personality
                    response = self._personalize_response(response, personality_traits, conversation_context)
                    
                    logger.info(f"Generated response using template: {template.template_id}")
                    return {"response": response, "confidence": template.confidence}
                else:
                    # Generate fallback response
                    fallback = self._generate_fallback_response(last_message, conversation_context)
                    logger.info("Generated fallback response")
                    return {"response": fallback, "confidence": 0.6}
                    
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return {"response": "I'm here to help. What would you like to talk about?", "confidence": 0.5}
    
    async def _generate_response_async(self, message: str, sender: str, conversation_id: str, context: Dict[str, Any], personality_traits: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response for new API calls with full async processing"""
        try:
            # Process the incoming message
            processed_message = await self.process_message(message, sender, conversation_id, context)
            
            # Get conversation context
            conv_context = self.active_conversations.get(conversation_id)
            if not conv_context:
                # Create default context
                conv_context = ConversationContext(
                    conversation_id=conversation_id,
                    participants=[sender, "digital_twin"],
                    topic=self._extract_topic(message),
                    mood="neutral",
                    energy_level=0.7,
                    conversation_style="casual",
                    start_time=datetime.now(),
                    last_activity=datetime.now(),
                    message_count=1
                )
                self.active_conversations[conversation_id] = conv_context
            
            # Find appropriate response template
            template = self._find_response_template(conv_context, processed_message, personality_traits)
            
            if template:
                # Select response pattern
                response = random.choice(template.response_patterns)
                
                # Personalize response based on personality
                response = self._personalize_response(response, personality_traits, conv_context)
                
                confidence = template.confidence
                logger.info(f"Generated response using template: {template.template_id}")
            else:
                # Generate contextual fallback response
                response = self._generate_contextual_fallback(processed_message, conv_context, personality_traits)
                confidence = 0.7
                logger.info("Generated contextual fallback response")
            
            # Update conversation context with response
            conv_context.last_activity = datetime.now()
            conv_context.message_count += 1
            
            return {
                "response": response,
                "confidence": confidence,
                "processing_time": int(time.time() * 1000) % 1000,  # Mock processing time
                "message_type": processed_message.message_type,
                "sentiment": processed_message.sentiment,
                "intent": processed_message.intent,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            logger.error(f"Failed to generate async response: {e}")
            return {
                "response": "I'm sorry, I'm having trouble processing that right now. Could you try again?",
                "confidence": 0.3,
                "error": str(e)
            }
    
    def _find_response_template(self, context: ConversationContext, message: ConversationMessage, personality_traits: Dict[str, Any]) -> Optional[ResponseTemplate]:
        """Find the most appropriate response template"""
        best_template = None
        best_score = 0.0
        
        for template in self.response_templates:
            score = 0.0
            
            # Scenario matching
            if self._matches_scenario(template, context, message):
                score += 0.4
            
            # Personality trait matching
            personality_match = self._calculate_personality_match(template, personality_traits)
            score += personality_match * 0.3
            
            # Context requirements matching
            context_match = self._calculate_context_match(template, context, message)
            score += context_match * 0.3
            
            if score > best_score:
                best_score = score
                best_template = template
        
        return best_template if best_score > 0.5 else None
    
    def _matches_scenario(self, template: ResponseTemplate, context: ConversationContext, message: ConversationMessage) -> bool:
        """Check if template matches the current scenario"""
        if template.scenario == "morning_greeting" and context.topic == "greeting":
            return True
        elif template.scenario == "work_conversation" and context.topic == "work":
            return True
        elif template.scenario == "emotional_support" and message.sentiment in ["negative", "anxious"]:
            return True
        elif template.scenario == "social_interaction" and context.topic in ["social", "personal"]:
            return True
        
        return False
    
    def _calculate_personality_match(self, template: ResponseTemplate, personality_traits: Dict[str, Any]) -> float:
        """Calculate how well template matches personality traits"""
        if not template.personality_traits:
            return 0.5
        
        total_match = 0.0
        trait_count = 0
        
        for trait, value in template.personality_traits.items():
            if trait in personality_traits:
                # Calculate similarity (1.0 = perfect match, 0.0 = opposite)
                similarity = 1.0 - abs(personality_traits[trait] - value)
                total_match += similarity
                trait_count += 1
        
        return total_match / trait_count if trait_count > 0 else 0.5
    
    def _calculate_context_match(self, template: ResponseTemplate, context: ConversationContext, message: ConversationMessage) -> float:
        """Calculate how well template matches conversation context"""
        if not template.context_requirements:
            return 0.5
        
        total_match = 0.0
        requirement_count = 0
        
        for requirement, expected_value in template.context_requirements.items():
            if requirement == "time_of_day":
                current_hour = datetime.now().hour
                if expected_value == "morning" and 6 <= current_hour <= 11:
                    total_match += 1.0
                elif expected_value == "afternoon" and 12 <= current_hour <= 17:
                    total_match += 1.0
                elif expected_value == "evening" and 18 <= current_hour <= 21:
                    total_match += 1.0
                elif expected_value == "night" and (22 <= current_hour or current_hour <= 5):
                    total_match += 1.0
                requirement_count += 1
            
            elif requirement == "topic" and context.topic == expected_value:
                total_match += 1.0
                requirement_count += 1
            
            elif requirement == "sentiment" and message.sentiment == expected_value:
                total_match += 1.0
                requirement_count += 1
            
            elif requirement == "energy_level":
                if abs(context.energy_level - expected_value) < 0.2:
                    total_match += 1.0
                requirement_count += 1
        
        return total_match / requirement_count if requirement_count > 0 else 0.5
    
    def _personalize_response(self, response: str, personality_traits: Dict[str, Any], context: ConversationContext) -> str:
        """Personalize response based on personality traits"""
        personalized = response
        
        # Add personality-based modifiers
        if personality_traits.get("extraversion", 0.5) > 0.7:
            # More enthusiastic responses
            if "!" not in response:
                personalized = personalized.replace(".", "!")
        
        if personality_traits.get("empathy", 0.5) > 0.7:
            # More empathetic responses
            if "I understand" not in response and "I'm here" not in response:
                personalized = "I understand. " + personalized
        
        if personality_traits.get("conscientiousness", 0.5) > 0.7:
            # More structured responses
            if "Let's" in response and "step" not in response:
                personalized = personalized.replace("Let's", "Let's break this down into steps. ")
        
        return personalized
    
    def _generate_fallback_response(self, message: ConversationMessage, context: ConversationContext) -> str:
        """Generate a fallback response when no template matches"""
        fallback_responses = [
            "That's interesting. Tell me more about it.",
            "I see what you mean. How do you feel about that?",
            "That's a good point. What are your thoughts on it?",
            "I understand. What would you like to explore next?",
            "That sounds important. How can I help you with that?"
        ]
        
        return random.choice(fallback_responses)
    
    def get_conversation_summary(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of a conversation"""
        if conversation_id not in self.active_conversations:
            return None
        
        context = self.active_conversations[conversation_id]
        messages = [msg for msg in self.conversation_history if msg.sender != "system"]
        
        return {
            "conversation_id": conversation_id,
            "participants": context.participants,
            "topic": context.topic,
            "mood": context.mood,
            "start_time": context.start_time.isoformat(),
            "last_activity": context.last_activity.isoformat(),
            "message_count": context.message_count,
            "duration_minutes": int((context.last_activity - context.start_time).total_seconds() / 60),
            "sentiment_distribution": self._calculate_sentiment_distribution(messages),
            "intent_distribution": self._calculate_intent_distribution(messages)
        }
    
    def _calculate_sentiment_distribution(self, messages: List[ConversationMessage]) -> Dict[str, int]:
        """Calculate distribution of sentiments in messages"""
        distribution = {}
        for message in messages:
            sentiment = message.sentiment
            distribution[sentiment] = distribution.get(sentiment, 0) + 1
        return distribution
    
    def _calculate_intent_distribution(self, messages: List[ConversationMessage]) -> Dict[str, int]:
        """Calculate distribution of intents in messages"""
        distribution = {}
        for message in messages:
            intent = message.intent
            distribution[intent] = distribution.get(intent, 0) + 1
        return distribution
    
    def _analyze_sentiment_rule_based(self, message: str, context: Dict[str, Any]) -> str:
        """Analyze sentiment using rule-based approach"""
        message_lower = message.lower()
        
        # Positive indicators
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "happy", "joy", "love", "like", "enjoy"]
        if any(word in message_lower for word in positive_words):
            return "positive"
        
        # Negative indicators
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "sad", "angry", "frustrated", "upset"]
        if any(word in message_lower for word in negative_words):
            return "negative"
        
        # Question indicators
        if "?" in message or any(word in message_lower for word in ["what", "how", "why", "when", "where", "who"]):
            return "neutral"
        
        # Default to neutral
        return "neutral"
    
    def _detect_intent_rule_based(self, message: str, context: Dict[str, Any]) -> str:
        """Detect intent using rule-based approach"""
        message_lower = message.lower()
        
        # Greeting
        if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "greet"
        
        # Question
        if "?" in message or any(word in message_lower for word in ["what", "how", "why", "when", "where", "who"]):
            return "ask_question"
        
        # Request
        if any(word in message_lower for word in ["can you", "please", "help", "need", "want"]):
            return "request_action"
        
        # Statement
        if any(word in message_lower for word in ["is", "are", "was", "were", "will", "going to"]):
            return "provide_information"
        
        # Default
        return "socialize"
    
    async def _fallback_message_processing(self, message: str, sender: str, conversation_id: str, context: Dict[str, Any]) -> ConversationMessage:
        """Fallback message processing when AI models fail"""
        try:
            # Create a basic conversation message
            conversation_message = ConversationMessage(
                message_id=f"fallback_{int(time.time())}",
                sender=sender,
                content=message,
                message_type="text",
                timestamp=datetime.now(),
                context=context,
                sentiment=self._analyze_sentiment_rule_based(message, context),
                intent=self._detect_intent_rule_based(message, context)
            )
            
            # Add to history
            self.conversation_history.append(conversation_message)
            
            # Update conversation context
            await self._update_conversation_context(conversation_id, conversation_message)
            
            return conversation_message
            
        except Exception as e:
            logger.error(f"Fallback message processing failed: {e}")
            # Return a minimal message
            return ConversationMessage(
                message_id=f"error_{int(time.time())}",
                sender=sender,
                content=message,
                message_type="text",
                timestamp=datetime.now(),
                context=context,
                sentiment="neutral",
                intent="socialize"
            )
    
    def _generate_contextual_fallback(self, message: ConversationMessage, context: ConversationContext, personality_traits: Dict[str, Any]) -> str:
        """Generate a contextual fallback response based on message and context"""
        # Customize response based on message type and sentiment
        if message.message_type == "question":
            return "That's an interesting question. Let me think about that..."
        elif message.message_type == "greeting":
            return "Hello! It's great to hear from you. How are you doing today?"
        elif message.sentiment == "negative":
            return "I understand you might be going through something difficult. I'm here to listen."
        elif message.sentiment == "positive":
            return "That's wonderful! I love hearing positive news. Tell me more about it!"
        elif message.intent == "request_action":
            return "I'd be happy to help you with that. What specifically would you like me to do?"
        elif message.intent == "seek_help":
            return "Of course, I'm here to support you. What do you need help with?"
        else:
            # Default contextual responses based on personality
            if personality_traits.get("empathy", 0.5) > 0.7:
                return "I'm really interested in what you're sharing. Could you tell me more?"
            elif personality_traits.get("extraversion", 0.5) > 0.7:
                return "That sounds fascinating! I'd love to dive deeper into this topic with you."
            else:
                return "I appreciate you sharing that with me. What's on your mind?"
    
    def _generate_response_sync(self, message: str, sender: str, conversation_id: str, context: Dict[str, Any], personality_traits: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response synchronously for cases where we're already in an event loop"""
        try:
            # Process the message synchronously using rule-based methods
            message_type = self._classify_message_type(message)
            sentiment = self._analyze_sentiment_rule_based(message, context)
            intent = self._detect_intent_rule_based(message, context)
            
            # Create a simplified conversation message object
            processed_message = ConversationMessage(
                message_id=f"sync_{int(time.time())}",
                sender=sender,
                content=message,
                message_type=message_type,
                timestamp=datetime.now(),
                context=context,
                sentiment=sentiment,
                intent=intent
            )
            
            # Get or create conversation context
            conv_context = self.active_conversations.get(conversation_id)
            if not conv_context:
                conv_context = ConversationContext(
                    conversation_id=conversation_id,
                    participants=[sender, "digital_twin"],
                    topic=self._extract_topic(message),
                    mood="neutral",
                    energy_level=0.7,
                    conversation_style="casual",
                    start_time=datetime.now(),
                    last_activity=datetime.now(),
                    message_count=1
                )
                self.active_conversations[conversation_id] = conv_context
            
            # Find appropriate response template
            template = self._find_response_template(conv_context, processed_message, personality_traits)
            
            if template:
                # Select response pattern
                response = random.choice(template.response_patterns)
                
                # Personalize response based on personality
                response = self._personalize_response(response, personality_traits, conv_context)
                
                confidence = template.confidence
                logger.info(f"Generated sync response using template: {template.template_id}")
            else:
                # Generate contextual fallback response
                response = self._generate_contextual_fallback(processed_message, conv_context, personality_traits)
                confidence = 0.7
                logger.info("Generated sync contextual fallback response")
            
            # Update conversation context
            conv_context.last_activity = datetime.now()
            conv_context.message_count += 1
            
            # Add to history
            self.conversation_history.append(processed_message)
            
            return {
                "response": response,
                "confidence": confidence,
                "processing_time": int(time.time() * 1000) % 1000,
                "message_type": message_type,
                "sentiment": sentiment,
                "intent": intent,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            logger.error(f"Failed to generate sync response: {e}")
            return {
                "response": "I'm sorry, I'm having trouble processing that right now. Could you try again?",
                "confidence": 0.3,
                "error": str(e)
            }
    
    async def shutdown(self):
        """Shutdown the conversation engine"""
        self.is_initialized = False
        logger.info("Conversation Engine shutdown complete")
