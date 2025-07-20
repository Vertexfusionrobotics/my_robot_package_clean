    def generate_response(self, user_input, context={}, sentiment=None):
        """Generate response using neural models with rich context awareness"""
        if not TF_AVAILABLE:
            return None
            
        try:
            # Preprocess input
            input_sequence = self.tokenize_input(user_input)
            
            # Get rich context features 
            context_features = np.zeros((10,))
            
            # Process immediate context
            if context.get('immediate_context'):
                context_features[0] = 1  # Immediate context available
                # Extract key topics/entities
                topics = self.extract_topics(context['immediate_context'])
                for i, topic in enumerate(topics[:3]):  # Top 3 topics
                    context_features[i+1] = 1
            
            # Process conversation history
            if context.get('conversation_history'):
                context_features[4] = 1  # History available
                recent_interactions = context['conversation_history'][-3:]  # Last 3 interactions
                sentiment_scores = [self.get_sentiment_score(interaction) for interaction in recent_interactions]
                context_features[5] = np.mean(sentiment_scores) if sentiment_scores else 0
            
            # Process learned patterns
            if context.get('learned_patterns'):
                context_features[6] = 1  # Patterns available
                pattern_relevance = self.calculate_pattern_relevance(user_input, context['learned_patterns'])
                context_features[7] = pattern_relevance
            
            # Current sentiment
            if sentiment:
                context_features[8] = 1 if sentiment == 'positive' else -1 if sentiment == 'negative' else 0
            
            # User profile context if available
            if context.get('user_profile'):
                context_features[9] = 1
            
            # Generate response using model with rich context
            if 'response_generator' in self.models:
                model_input = {
                    'input_sequence': np.array([input_sequence]),
                    'context_input': np.array([context_features])
                }
                
                # Get multiple predictions for diversity
                num_candidates = 3
                predictions = []
                for _ in range(num_candidates):
                    pred = self.models['response_generator'].predict(model_input, verbose=0)
                    predictions.append(pred[0])
                
                # Select best response based on context
                response = self.select_best_response(predictions, context)
                
                # Update context memory with rich interaction data
                if self.context_memory:
                    interaction_data = {
                        'user_input': user_input,
                        'response': response,
                        'sentiment': sentiment,
                        'context_features': context_features.tolist(),
                        'topics': topics if 'topics' in locals() else [],
                        'timestamp': datetime.now().isoformat()
                    }
                    self.context_memory.store_interaction(user_input, response, sentiment, metadata=interaction_data)
                
                return response
                
        except Exception as e:
            print(f"Error in advanced response generation: {e}")
            return None
            
    def extract_topics(self, context):
        """Extract key topics from context"""
        # Simple keyword extraction for now
        common_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'])
        words = ' '.join(str(context).lower().split())
        topics = [w for w in words.split() if w not in common_words and len(w) > 3]
        return list(set(topics))[:5]  # Return up to 5 unique topics
        
    def get_sentiment_score(self, interaction):
        """Convert interaction sentiment to numerical score"""
        if isinstance(interaction, dict):
            sentiment = interaction.get('sentiment', 'neutral')
        else:
            sentiment = 'neutral'
        return 1 if sentiment == 'positive' else -1 if sentiment == 'negative' else 0
        
    def calculate_pattern_relevance(self, input_text, patterns):
        """Calculate how relevant learned patterns are to input"""
        if not patterns:
            return 0
        
        relevance_scores = []
        input_words = set(input_text.lower().split())
        
        for pattern in patterns:
            if isinstance(pattern, dict):
                pattern_text = ' '.join([
                    str(pattern.get('trigger', '')),
                    str(pattern.get('response', ''))
                ]).lower()
                pattern_words = set(pattern_text.split())
                
                # Calculate word overlap
                overlap = len(input_words & pattern_words)
                if len(pattern_words) > 0:
                    relevance = overlap / len(pattern_words)
                    relevance_scores.append(relevance)
        
        return np.mean(relevance_scores) if relevance_scores else 0
        
    def select_best_response(self, candidates, context):
        """Select best response from candidates based on context"""
        if not candidates:
            return None
            
        # Convert responses to text
        responses = [self.decode_response(pred) for pred in candidates]
        
        # Score responses
        scores = []
        for response in responses:
            score = 0
            
            # Length score - prefer medium length responses
            length = len(response.split())
            if 5 <= length <= 20:
                score += 1
            
            # Context relevance
            if context.get('immediate_context'):
                topics = self.extract_topics(context['immediate_context'])
                topic_overlap = len(set(response.lower().split()) & set(topics))
                score += topic_overlap * 0.5
            
            # Sentiment alignment
            if context.get('current_sentiment'):
                sentiment_score = self.get_sentiment_score({'sentiment': context['current_sentiment']})
                if sentiment_score != 0:  # If not neutral
                    response_sentiment = self.get_sentiment_score({'sentiment': self.analyze_sentiment(response)})
                    if sentiment_score * response_sentiment > 0:  # Same polarity
                        score += 1
            
            scores.append(score)
        
        # Return response with highest score
        return responses[np.argmax(scores)]
        
    def analyze_sentiment(self, text):
        """Simple sentiment analysis of text"""
        positive_words = {'good', 'great', 'awesome', 'excellent', 'happy', 'wonderful'}
        negative_words = {'bad', 'poor', 'terrible', 'awful', 'sad', 'unhappy'}
        
        words = set(text.lower().split())
        pos_count = len(words & positive_words)
        neg_count = len(words & negative_words)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        return 'neutral'
            
    def tokenize_input(self, text):
        """Tokenize input text for model"""
        if 'main' not in self.tokenizers:
            print("⚠️ No tokenizer available")
            return np.zeros((self.max_sequence_length,))
            
        tokenizer = self.tokenizers['main']
        sequence = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequence, maxlen=self.max_sequence_length, padding='post')
        
        return padded[0]
        
    def decode_response(self, prediction):
        """Convert model prediction back to text"""
        if 'main' not in self.tokenizers:
            print("⚠️ No tokenizer available")
            return ""
            
        tokenizer = self.tokenizers['main']
        
        # Get indices of highest probability tokens
        token_indices = np.argmax(prediction, axis=-1)
        
        # Convert to words using tokenizer's index_word mapping
        words = []
        for idx in token_indices:
            if idx > 0 and idx in tokenizer.index_word:
                word = tokenizer.index_word[idx]
                if word != '<OOV>':
                    words.append(word)
                    
        return ' '.join(words)
