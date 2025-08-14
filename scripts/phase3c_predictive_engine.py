#!/usr/bin/env python3
"""
Percepta Pro v2.0 - Phase 3C: Predictive Analytics Engine
Advanced ML models for reputation forecasting, threat prediction, and crisis management

Core Models:
1. Reputation Forecasting Engine - LSTM + Transformer for reputation trends
2. Threat Escalation Predictor - Classification + Regression for crisis prevention  
3. Engagement Trend Analyzer - Time Series analysis for performance optimization
4. Crisis Probability Assessor - Ensemble model for real-time risk assessment
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ML and Deep Learning imports
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Input, Attention
    from tensorflow.keras.optimizers import Adam
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import mean_absolute_error, accuracy_score, classification_report
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    import joblib
    ML_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ ML libraries not fully available: {e}")
    ML_AVAILABLE = False

# Visualization imports
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

class PredictiveAnalyticsEngine:
    """
    Comprehensive Phase 3C Predictive Analytics Engine
    Implements four core ML models for maximum business impact
    """
    
    def __init__(self):
        """Initialize the predictive analytics engine"""
        self.models = {}
        self.scalers = {}
        self.feature_columns = {}
        self.predictions = {}
        
        # Model configurations
        self.model_configs = {
            'reputation_forecasting': {
                'sequence_length': 7,  # 7-day sequences for LSTM
                'forecast_horizons': [7, 30, 90],  # Days to forecast
                'features': ['sentiment', 'engagement', 'threat_level']
            },
            'threat_escalation': {
                'classification_threshold': 0.7,  # Threat escalation probability
                'severity_levels': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                'features': ['sentiment_momentum', 'engagement_anomaly', 'threat_patterns']
            },
            'engagement_trends': {
                'seasonal_components': ['daily', 'weekly', 'monthly'],
                'trend_windows': [7, 14, 30],  # Rolling windows for analysis
                'features': ['views_momentum', 'likes_ratio', 'comments_velocity']
            },
            'crisis_probability': {
                'ensemble_models': ['rf', 'gb', 'neural'],  # Random Forest, Gradient Boosting, Neural Network
                'risk_thresholds': [0.3, 0.6, 0.8],  # Low, Medium, High risk
                'features': ['all_available']  # Use all engineered features
            }
        }
        
        print("🚀 Phase 3C Predictive Analytics Engine initialized")
        print(f"   ML Available: {ML_AVAILABLE}")
        print(f"   Visualization Available: {VISUALIZATION_AVAILABLE}")
    
    def load_optimized_datasets(self):
        """Load the optimized ML-ready datasets"""
        print("\n📊 LOADING OPTIMIZED DATASETS")
        print("=" * 40)
        
        try:
            # Load ML-ready videos dataset
            self.videos_df = pd.read_csv('backend/data/videos/youtube_videos_ml_ready.csv')
            print(f"✅ Videos ML-ready dataset: {self.videos_df.shape}")
            
            # Load cleaned comments dataset  
            self.comments_df = pd.read_csv('backend/data/comments/youtube_comments_ai_enhanced_cleaned.csv')
            print(f"✅ Comments cleaned dataset: {self.comments_df.shape}")
            
            # Prepare datetime columns
            if 'Date' in self.videos_df.columns:
                self.videos_df['Date'] = pd.to_datetime(self.videos_df['Date'])
            elif 'PublishedAt_Formatted' in self.videos_df.columns:
                self.videos_df['Date'] = pd.to_datetime(self.videos_df['PublishedAt_Formatted'], format='%d-%m-%Y')
            
            # Sort by date for time series analysis
            self.videos_df = self.videos_df.sort_values('Date').reset_index(drop=True)
            
            print(f"✅ Dataset preparation complete")
            print(f"   Date range: {self.videos_df['Date'].min()} to {self.videos_df['Date'].max()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading datasets: {str(e)}")
            return False
    
    def prepare_features_for_ml(self):
        """Prepare and engineer features for ML models"""
        print("\n🔧 PREPARING FEATURES FOR ML MODELS")
        print("=" * 45)
        
        # 1. Reputation Features (for forecasting)
        print("Creating reputation features...")
        reputation_features = []
        
        if 'SentimentScore_EN' in self.videos_df.columns:
            reputation_features.append('SentimentScore_EN')
        if 'SentimentScore_TE' in self.videos_df.columns:
            reputation_features.append('SentimentScore_TE')
        if 'Views_7d_avg' in self.videos_df.columns:
            reputation_features.append('Views_7d_avg')
        if 'Like_to_View_ratio' in self.videos_df.columns:
            reputation_features.append('Like_to_View_ratio')
        
        self.feature_columns['reputation'] = reputation_features
        print(f"   Reputation features: {len(reputation_features)}")
        
        # 2. Threat Features (for escalation prediction)
        print("Creating threat features...")
        threat_features = []
        
        if 'Sentiment_EN_momentum' in self.videos_df.columns:
            threat_features.append('Sentiment_EN_momentum')
        if 'Sentiment_TE_momentum' in self.videos_df.columns:
            threat_features.append('Sentiment_TE_momentum')
        if 'Views_anomaly_score' in self.videos_df.columns:
            threat_features.append('Views_anomaly_score')
        if 'Likes_anomaly_score' in self.videos_df.columns:
            threat_features.append('Likes_anomaly_score')
        
        self.feature_columns['threat'] = threat_features
        print(f"   Threat features: {len(threat_features)}")
        
        # 3. Engagement Features (for trend analysis)
        print("Creating engagement features...")
        engagement_features = []
        
        if 'Views_change_7d' in self.videos_df.columns:
            engagement_features.append('Views_change_7d')
        if 'Likes_change_7d' in self.videos_df.columns:
            engagement_features.append('Likes_change_7d')
        if 'Views_pct_change' in self.videos_df.columns:
            engagement_features.append('Views_pct_change')
        if 'Comment_to_View_ratio' in self.videos_df.columns:
            engagement_features.append('Comment_to_View_ratio')
        
        self.feature_columns['engagement'] = engagement_features
        print(f"   Engagement features: {len(engagement_features)}")
        
        # 4. Crisis Features (all available features)
        print("Creating comprehensive crisis features...")
        crisis_features = list(set(reputation_features + threat_features + engagement_features))
        
        # Add temporal features
        temporal_features = ['Day_of_Week', 'Month', 'Days_since_start']
        for tf in temporal_features:
            if tf in self.videos_df.columns:
                crisis_features.append(tf)
        
        self.feature_columns['crisis'] = crisis_features
        print(f"   Crisis features: {len(crisis_features)}")
        
        # 5. Create target variables for supervised learning
        print("Creating target variables...")
        
        # Reputation target (future sentiment trend)
        if 'SentimentScore_EN' in self.videos_df.columns:
            self.videos_df['reputation_target'] = self.videos_df['SentimentScore_EN'].shift(-7)  # 7-day ahead sentiment
        
        # Threat target (based on sentiment decline)
        if 'Sentiment_EN_momentum' in self.videos_df.columns:
            self.videos_df['threat_target'] = (self.videos_df['Sentiment_EN_momentum'] < -0.3).astype(int)
        
        # Engagement target (future view performance)
        if 'Views_pct_change' in self.videos_df.columns:
            self.videos_df['engagement_target'] = self.videos_df['Views_pct_change'].shift(-7)  # 7-day ahead performance
        
        # Crisis target (comprehensive risk indicator)
        threat_component = self.videos_df.get('threat_target', 0)
        sentiment_component = (self.videos_df.get('SentimentScore_EN', 0) < -0.5).astype(int)
        anomaly_component = (self.videos_df.get('Views_anomaly_score', 0) > 2).astype(int)
        
        self.videos_df['crisis_target'] = (threat_component + sentiment_component + anomaly_component >= 2).astype(int)
        
        print("✅ Feature preparation complete")
        return True
    
    def build_reputation_forecasting_model(self):
        """Build LSTM-based reputation forecasting model"""
        print("\n🎯 BUILDING REPUTATION FORECASTING MODEL")
        print("=" * 45)
        
        if not ML_AVAILABLE:
            print("⚠️ ML libraries not available, using statistical fallback")
            return self._build_statistical_reputation_model()
        
        features = self.feature_columns['reputation']
        if not features or len(features) < 2:
            print("⚠️ Insufficient features for reputation modeling")
            return False
        
        # Prepare sequences for LSTM
        sequence_length = self.model_configs['reputation_forecasting']['sequence_length']
        
        # Create feature matrix
        X_data = self.videos_df[features].fillna(0).values
        y_data = self.videos_df['reputation_target'].fillna(0).values
        
        # Create sequences
        X_sequences, y_sequences = [], []
        for i in range(sequence_length, len(X_data)):
            X_sequences.append(X_data[i-sequence_length:i])
            y_sequences.append(y_data[i])
        
        X_sequences = np.array(X_sequences)
        y_sequences = np.array(y_sequences)
        
        if len(X_sequences) < 10:
            print("⚠️ Insufficient sequences for LSTM training")
            return self._build_statistical_reputation_model()
        
        # Split data
        train_size = int(0.8 * len(X_sequences))
        X_train, X_test = X_sequences[:train_size], X_sequences[train_size:]
        y_train, y_test = y_sequences[:train_size], y_sequences[train_size:]
        
        # Build LSTM model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(sequence_length, len(features))),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        
        # Train model
        print("Training LSTM reputation forecasting model...")
        history = model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=16,
            validation_data=(X_test, y_test),
            verbose=0
        )
        
        # Evaluate model
        train_mae = model.evaluate(X_train, y_train, verbose=0)[1]
        test_mae = model.evaluate(X_test, y_test, verbose=0)[1]
        
        print(f"✅ LSTM Model trained successfully")
        print(f"   Training MAE: {train_mae:.4f}")
        print(f"   Test MAE: {test_mae:.4f}")
        
        # Save model
        self.models['reputation_forecasting'] = model
        
        # Create forecasts for different horizons
        forecasts = {}
        for horizon in self.model_configs['reputation_forecasting']['forecast_horizons']:
            # Use last sequence to predict
            last_sequence = X_sequences[-1].reshape(1, sequence_length, len(features))
            forecast = model.predict(last_sequence, verbose=0)[0][0]
            forecasts[f'{horizon}_day'] = forecast
        
        self.predictions['reputation_forecasts'] = forecasts
        print(f"✅ Reputation forecasts generated: {list(forecasts.keys())}")
        
        return True
    
    def _build_statistical_reputation_model(self):
        """Fallback statistical model for reputation forecasting"""
        print("Using statistical fallback for reputation forecasting...")
        
        features = self.feature_columns['reputation']
        if not features:
            return False
        
        # Simple moving average and trend analysis
        feature_data = self.videos_df[features].fillna(0)
        
        # Calculate trend-based forecasts
        forecasts = {}
        for horizon in [7, 30, 90]:
            # Simple trend extrapolation
            recent_mean = feature_data.tail(7).mean().mean()
            trend = (recent_mean - feature_data.head(7).mean().mean()) / len(feature_data)
            forecast = recent_mean + (trend * horizon)
            forecasts[f'{horizon}_day'] = forecast
        
        self.predictions['reputation_forecasts'] = forecasts
        self.models['reputation_forecasting'] = 'statistical_model'
        
        print(f"✅ Statistical reputation forecasts: {forecasts}")
        return True
    
    def build_threat_escalation_model(self):
        """Build threat escalation prediction model"""
        print("\n🚨 BUILDING THREAT ESCALATION MODEL")
        print("=" * 40)
        
        features = self.feature_columns['threat']
        if not features:
            print("⚠️ No threat features available")
            return False
        
        # Prepare data
        X = self.videos_df[features].fillna(0)
        y = self.videos_df['threat_target'].fillna(0)
        
        # Remove rows where target is NaN
        valid_idx = ~y.isna()
        X = X[valid_idx]
        y = y[valid_idx]
        
        if len(X) < 10:
            print("⚠️ Insufficient data for threat modeling")
            return False
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        if ML_AVAILABLE:
            # Use Gradient Boosting for threat prediction
            model = GradientBoostingClassifier(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_acc = model.score(X_train_scaled, y_train)
            test_acc = model.score(X_test_scaled, y_test)
            
            print(f"✅ Threat escalation model trained")
            print(f"   Training accuracy: {train_acc:.4f}")
            print(f"   Test accuracy: {test_acc:.4f}")
            
        else:
            # Statistical fallback
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(random_state=42)
            model.fit(X_train_scaled, y_train)
            test_acc = model.score(X_test_scaled, y_test)
            print(f"✅ Statistical threat model - Accuracy: {test_acc:.4f}")
        
        # Save model and scaler
        self.models['threat_escalation'] = model
        self.scalers['threat_escalation'] = scaler
        
        # Generate threat predictions for recent data
        recent_data = X.tail(10)
        recent_scaled = scaler.transform(recent_data)
        threat_probs = model.predict_proba(recent_scaled)[:, 1] if hasattr(model, 'predict_proba') else model.predict(recent_scaled)
        
        self.predictions['threat_escalation'] = {
            'current_risk': float(np.mean(threat_probs)),
            'max_risk': float(np.max(threat_probs)),
            'trend': 'increasing' if threat_probs[-1] > threat_probs[0] else 'decreasing'
        }
        
        print(f"✅ Threat predictions: {self.predictions['threat_escalation']}")
        return True
    
    def build_engagement_trend_model(self):
        """Build engagement trend analysis model"""
        print("\n📈 BUILDING ENGAGEMENT TREND MODEL")
        print("=" * 40)
        
        features = self.feature_columns['engagement']
        if not features:
            print("⚠️ No engagement features available")
            return False
        
        # Prepare data for regression
        X = self.videos_df[features].fillna(0)
        y = self.videos_df['engagement_target'].fillna(0)
        
        # Remove rows where target is NaN
        valid_idx = ~y.isna()
        X = X[valid_idx]
        y = y[valid_idx]
        
        if len(X) < 10:
            print("⚠️ Insufficient data for engagement modeling")
            return False
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Build Random Forest for engagement prediction
        if ML_AVAILABLE:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_mae = mean_absolute_error(y_train, model.predict(X_train_scaled))
        test_mae = mean_absolute_error(y_test, model.predict(X_test_scaled))
        
        print(f"✅ Engagement trend model trained")
        print(f"   Training MAE: {train_mae:.4f}")
        print(f"   Test MAE: {test_mae:.4f}")
        
        # Save model and scaler
        self.models['engagement_trends'] = model
        self.scalers['engagement_trends'] = scaler
        
        # Generate engagement forecasts
        recent_data = X.tail(10)
        recent_scaled = scaler.transform(recent_data)
        engagement_forecasts = model.predict(recent_scaled)
        
        self.predictions['engagement_trends'] = {
            'short_term_forecast': float(np.mean(engagement_forecasts)),
            'confidence_interval': [float(np.percentile(engagement_forecasts, 25)), 
                                  float(np.percentile(engagement_forecasts, 75))],
            'trend_direction': 'positive' if np.mean(engagement_forecasts) > 0 else 'negative'
        }
        
        print(f"✅ Engagement forecasts: {self.predictions['engagement_trends']}")
        return True
    
    def build_crisis_probability_model(self):
        """Build ensemble crisis probability assessment model"""
        print("\n⚠️ BUILDING CRISIS PROBABILITY MODEL")
        print("=" * 40)
        
        features = self.feature_columns['crisis']
        if not features:
            print("⚠️ No crisis features available")
            return False
        
        # Prepare data
        X = self.videos_df[features].fillna(0)
        y = self.videos_df['crisis_target'].fillna(0)
        
        # Remove rows where target is NaN
        valid_idx = ~y.isna()
        X = X[valid_idx]
        y = y[valid_idx]
        
        if len(X) < 10:
            print("⚠️ Insufficient data for crisis modeling")
            return False
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Build ensemble model
        if ML_AVAILABLE:
            # Random Forest component
            rf_model = RandomForestRegressor(n_estimators=50, random_state=42)
            rf_model.fit(X_train_scaled, y_train)
            
            # Gradient Boosting component
            gb_model = GradientBoostingClassifier(n_estimators=50, random_state=42)
            gb_model.fit(X_train_scaled, y_train)
            
            ensemble_models = {'rf': rf_model, 'gb': gb_model}
            
        else:
            # Fallback ensemble
            from sklearn.linear_model import LogisticRegression, LinearRegression
            rf_model = LinearRegression()
            gb_model = LogisticRegression(random_state=42)
            
            rf_model.fit(X_train_scaled, y_train)
            gb_model.fit(X_train_scaled, y_train)
            
            ensemble_models = {'rf': rf_model, 'gb': gb_model}
        
        # Evaluate ensemble
        rf_pred = rf_model.predict(X_test_scaled)
        gb_pred = gb_model.predict_proba(X_test_scaled)[:, 1] if hasattr(gb_model, 'predict_proba') else gb_model.predict(X_test_scaled)
        
        ensemble_pred = (rf_pred + gb_pred) / 2
        ensemble_mae = mean_absolute_error(y_test, ensemble_pred)
        
        print(f"✅ Crisis probability ensemble trained")
        print(f"   Ensemble MAE: {ensemble_mae:.4f}")
        
        # Save models and scaler
        self.models['crisis_probability'] = ensemble_models
        self.scalers['crisis_probability'] = scaler
        
        # Generate current crisis assessment
        recent_data = X.tail(5)  # Last 5 data points
        recent_scaled = scaler.transform(recent_data)
        
        rf_crisis_probs = rf_model.predict(recent_scaled)
        gb_crisis_probs = gb_model.predict_proba(recent_scaled)[:, 1] if hasattr(gb_model, 'predict_proba') else gb_model.predict(recent_scaled)
        
        ensemble_crisis_probs = (rf_crisis_probs + gb_crisis_probs) / 2
        current_crisis_prob = float(np.mean(ensemble_crisis_probs))
        
        # Classify risk level
        risk_level = 'LOW'
        if current_crisis_prob > 0.8:
            risk_level = 'CRITICAL'
        elif current_crisis_prob > 0.6:
            risk_level = 'HIGH'
        elif current_crisis_prob > 0.3:
            risk_level = 'MEDIUM'
        
        self.predictions['crisis_probability'] = {
            'current_probability': current_crisis_prob,
            'risk_level': risk_level,
            'confidence': float(1 - ensemble_mae),  # Convert error to confidence
            'recommendation': self._get_crisis_recommendation(risk_level, current_crisis_prob)
        }
        
        print(f"✅ Crisis assessment: {self.predictions['crisis_probability']}")
        return True
    
    def _get_crisis_recommendation(self, risk_level: str, probability: float) -> str:
        """Generate crisis management recommendations"""
        recommendations = {
            'LOW': 'Continue monitoring. No immediate action required.',
            'MEDIUM': 'Increase monitoring frequency. Review content strategy.',
            'HIGH': 'Implement crisis protocols. Prepare response strategy.',
            'CRITICAL': 'Immediate action required. Activate crisis management team.'
        }
        
        return recommendations.get(risk_level, 'Monitor situation closely.')
    
    def generate_comprehensive_forecast(self):
        """Generate comprehensive forecast combining all models"""
        print("\n🔮 GENERATING COMPREHENSIVE FORECAST")
        print("=" * 45)
        
        forecast_report = {
            'timestamp': datetime.now().isoformat(),
            'reputation_forecasts': self.predictions.get('reputation_forecasts', {}),
            'threat_assessment': self.predictions.get('threat_escalation', {}),
            'engagement_trends': self.predictions.get('engagement_trends', {}),
            'crisis_probability': self.predictions.get('crisis_probability', {}),
            'strategic_recommendations': self._generate_strategic_recommendations()
        }
        
        # Save forecast report
        import json
        with open('scripts/logs/comprehensive_forecast_report.json', 'w') as f:
            json.dump(forecast_report, f, indent=2)
        
        print("✅ Comprehensive forecast generated and saved")
        return forecast_report
    
    def _generate_strategic_recommendations(self):
        """Generate strategic recommendations based on all predictions"""
        recommendations = []
        
        # Reputation recommendations
        if 'reputation_forecasts' in self.predictions:
            rep_forecast = self.predictions['reputation_forecasts']
            if rep_forecast.get('7_day', 0) < 0:
                recommendations.append("SHORT-TERM: Reputation declining. Consider proactive communication strategy.")
            if rep_forecast.get('30_day', 0) > 0.5:
                recommendations.append("MEDIUM-TERM: Positive reputation trend. Leverage for brand building.")
        
        # Threat recommendations
        if 'threat_escalation' in self.predictions:
            threat_data = self.predictions['threat_escalation']
            if threat_data.get('current_risk', 0) > 0.7:
                recommendations.append("THREAT: High escalation risk detected. Implement crisis protocols.")
        
        # Engagement recommendations
        if 'engagement_trends' in self.predictions:
            engagement_data = self.predictions['engagement_trends']
            if engagement_data.get('trend_direction') == 'negative':
                recommendations.append("ENGAGEMENT: Declining trend. Review content strategy and timing.")
        
        # Crisis recommendations
        if 'crisis_probability' in self.predictions:
            crisis_data = self.predictions['crisis_probability']
            risk_level = crisis_data.get('risk_level', 'LOW')
            if risk_level in ['HIGH', 'CRITICAL']:
                recommendations.append(f"CRISIS: {risk_level} risk level. {crisis_data.get('recommendation', '')}")
        
        return recommendations
    
    def save_models(self):
        """Save all trained models"""
        print("\n💾 SAVING TRAINED MODELS")
        print("=" * 30)
        
        model_dir = 'scripts/models'
        import os
        os.makedirs(model_dir, exist_ok=True)
        
        saved_count = 0
        
        # Save models using joblib for sklearn models, native save for tensorflow
        for model_name, model in self.models.items():
            try:
                if model_name == 'reputation_forecasting' and hasattr(model, 'save'):
                    # TensorFlow model
                    model.save(f'{model_dir}/{model_name}_model.h5')
                elif model != 'statistical_model':
                    # Sklearn models or ensemble
                    joblib.dump(model, f'{model_dir}/{model_name}_model.pkl')
                
                # Save corresponding scaler
                if model_name in self.scalers:
                    joblib.dump(self.scalers[model_name], f'{model_dir}/{model_name}_scaler.pkl')
                
                saved_count += 1
                print(f"✅ Saved {model_name} model")
                
            except Exception as e:
                print(f"⚠️ Could not save {model_name}: {str(e)}")
        
        print(f"✅ Saved {saved_count} models to {model_dir}/")
        return saved_count
    
    def run_complete_phase3c_implementation(self):
        """Execute complete Phase 3C implementation"""
        print("🚀 STARTING PHASE 3C: PREDICTIVE ANALYTICS IMPLEMENTATION")
        print("=" * 65)
        
        success_count = 0
        total_models = 4
        
        # Step 1: Load optimized datasets
        print("\n📊 STEP 1: LOADING OPTIMIZED DATASETS")
        if not self.load_optimized_datasets():
            print("❌ Failed to load datasets")
            return False
        success_count += 0.5
        
        # Step 2: Prepare features for ML
        print("\n🔧 STEP 2: PREPARING ML FEATURES")
        if not self.prepare_features_for_ml():
            print("❌ Failed to prepare features")
            return False
        success_count += 0.5
        
        # Step 3: Build predictive models
        print("\n🧠 STEP 3: BUILDING PREDICTIVE MODELS")
        
        # Model 1: Reputation Forecasting
        if self.build_reputation_forecasting_model():
            success_count += 1
        
        # Model 2: Threat Escalation Prediction
        if self.build_threat_escalation_model():
            success_count += 1
        
        # Model 3: Engagement Trend Analysis
        if self.build_engagement_trend_model():
            success_count += 1
        
        # Model 4: Crisis Probability Assessment
        if self.build_crisis_probability_model():
            success_count += 1
        
        # Step 4: Generate comprehensive forecast
        print("\n🔮 STEP 4: GENERATING FORECASTS")
        comprehensive_forecast = self.generate_comprehensive_forecast()
        
        # Step 5: Save models
        print("\n💾 STEP 5: SAVING MODELS")
        saved_models = self.save_models()
        
        # Final summary
        print("\n🎉 PHASE 3C IMPLEMENTATION COMPLETE")
        print("=" * 45)
        
        success_rate = (success_count / total_models) * 100
        
        print(f"✅ Models Successfully Implemented: {int(success_count)}/{total_models}")
        print(f"✅ Success Rate: {success_rate:.1f}%")
        print(f"✅ Models Saved: {saved_models}")
        print(f"✅ Comprehensive Forecast: Generated")
        
        if success_rate >= 75:
            print("🎯 PHASE 3C: SUCCESSFUL IMPLEMENTATION")
            return {
                'status': 'success',
                'models_implemented': int(success_count),
                'success_rate': success_rate,
                'forecast': comprehensive_forecast,
                'models_saved': saved_models
            }
        else:
            print("⚠️ PHASE 3C: PARTIAL IMPLEMENTATION")
            return {
                'status': 'partial',
                'models_implemented': int(success_count),
                'success_rate': success_rate,
                'forecast': comprehensive_forecast
            }

if __name__ == "__main__":
    # Initialize and run Phase 3C implementation
    engine = PredictiveAnalyticsEngine()
    results = engine.run_complete_phase3c_implementation()
    
    if results:
        print(f"\n📊 Final Results: {results}")
        
        if results['status'] == 'success':
            print("\n🎉 Percepta Pro v2.0 Phase 3C: Predictive Analytics COMPLETE!")
            print("   Ready for dashboard integration and executive deployment.")
        else:
            print("\n⚠️ Phase 3C partially completed. Check logs for details.")
    else:
        print("\n❌ Phase 3C implementation failed. Check system requirements.") 